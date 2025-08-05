# Import Flask framework for creating web API
from flask import Flask, request, jsonify
# Import CORS to allow frontend to make requests from different port
from flask_cors import CORS
# Import the Board class from your original chess logic
from chess_board import Board
# Import utility functions for converting chess notation
from utils import algebraic_to_index, index_to_algebraic
# Import JSON for data handling
import json

# Create a new Flask web application instance
app = Flask(__name__)
# Enable CORS to allow React frontend to communicate with this API
CORS(app)

# Global variables to store the current game state across all requests
game_board = Board()  # Your chess board instance
current_turn = "w"    # Track whose turn it is ("w" for white, "b" for black)
game_history = []     # Store all moves made in the game

# API endpoint to start a new game
@app.route('/api/new-game', methods=['POST'])
def new_game():
    # Access global variables to modify them
    global game_board, current_turn, game_history
    # Create a fresh board with pieces in starting positions
    game_board = Board()
    # Reset turn to white (white always goes first in chess)
    current_turn = "w"
    # Clear the move history
    game_history = []
    # Return the new game state to the frontend
    return jsonify({
        'board': get_board_state(),  # Current board layout
        'turn': current_turn,        # Whose turn it is
        'message': 'New game started' # Success message
    })

# API endpoint to get the current board state
@app.route('/api/board', methods=['GET'])
def get_board():
    # Return current game state including check/checkmate status
    return jsonify({
        'board': get_board_state(),  # Current board layout
        'turn': current_turn,        # Whose turn it is
        # Check if the player whose turn it is NOT is in check
        'in_check': game_board.is_in_check("b" if current_turn == "w" else "w"),
        # Check if the player whose turn it is NOT is in checkmate
        'checkmate': game_board.is_checkmate("b" if current_turn == "w" else "w")
    })

# API endpoint to make a move
@app.route('/api/move', methods=['POST'])
def make_move():
    # Access global variables to modify them
    global current_turn, game_history
    
    # Get the move data from the frontend request
    data = request.get_json()
    start_pos = data.get('start')  # Starting position (e.g., "e2")
    end_pos = data.get('end')      # Ending position (e.g., "e4")
    
    # Validate that both positions were provided
    if not start_pos or not end_pos:
        return jsonify({'error': 'Invalid move data'}), 400
    
    try:
        # Convert chess notation to board coordinates
        start = algebraic_to_index(start_pos)  # e.g., "e2" -> (6, 4)
        end = algebraic_to_index(end_pos)      # e.g., "e4" -> (4, 4)
    except:
        # Return error if the notation is invalid
        return jsonify({'error': 'Invalid algebraic notation'}), 400
    
    # Get the piece at the starting position
    piece = game_board.board[start[0]][start[1]]
    # Check if there's actually a piece there
    if not piece:
        return jsonify({'error': 'No piece at that position'}), 400
    
    # Check if it's the correct player's turn
    if piece.color != current_turn:
        return jsonify({'error': 'Not your turn'}), 400
    
    # Check if the move is legal according to chess rules
    if not game_board.is_legal_move(start, end):
        return jsonify({'error': 'Illegal move'}), 400
    
    # Store the piece that might be captured (if any)
    captured_piece = game_board.board[end[0]][end[1]]
    # Execute the move on the board
    game_board.move_piece(start, end)
    
    # Create a record of this move for history
    move_record = {
        'start': start_pos,                                    # Starting position
        'end': end_pos,                                       # Ending position
        'piece': piece.__class__.__name__,                    # Type of piece moved
        'color': piece.color,                                 # Color of piece
        'captured': captured_piece.__class__.__name__ if captured_piece else None  # Captured piece (if any)
    }
    # Add this move to the game history
    game_history.append(move_record)
    
    # Determine whose turn it will be next
    next_turn = "b" if current_turn == "w" else "w"
    # Check if the next player is in checkmate
    is_checkmate = game_board.is_checkmate(next_turn)
    # Check if the next player is in check
    is_in_check = game_board.is_in_check(next_turn)
    
    # Switch to the next player's turn
    current_turn = next_turn
    
    # Return the updated game state to the frontend
    return jsonify({
        'board': get_board_state(),  # Updated board layout
        'turn': current_turn,        # New current turn
        'move': move_record,         # Details of the move made
        'in_check': is_in_check,     # Whether next player is in check
        'checkmate': is_checkmate,   # Whether next player is in checkmate
        'message': 'Move successful' # Success message
    })

# API endpoint to get valid moves for a selected piece (currently unused by frontend)
@app.route('/api/valid-moves', methods=['POST'])
def get_valid_moves():
    # Get the position from the frontend request
    data = request.get_json()
    position = data.get('position')
    
    # Validate that a position was provided
    if not position:
        return jsonify({'error': 'Position required'}), 400
    
    try:
        # Convert chess notation to board coordinates
        pos = algebraic_to_index(position)
    except:
        # Return error if the notation is invalid
        return jsonify({'error': 'Invalid position'}), 400
    
    # Get the piece at the specified position
    piece = game_board.board[pos[0]][pos[1]]
    # If there's no piece there, return empty moves list
    if not piece:
        return jsonify({'moves': []})
    
    # If it's not the current player's piece, return empty moves list
    if piece.color != current_turn:
        return jsonify({'moves': []})
    
    try:
        # Get all legal moves for this piece according to chess rules
        legal_moves = piece.get_legal_moves(game_board.board, pos)
        # Filter out moves that would put own king in check
        valid_moves = []
        for move in legal_moves:
            # Temporarily make the move to test if it puts own king in check
            captured = game_board.board[move[0]][move[1]]
            game_board.board[move[0]][move[1]] = piece
            game_board.board[pos[0]][pos[1]] = None
            # Check if this move puts the moving player's king in check
            in_check = game_board.is_in_check(piece.color)
            # Undo the temporary move
            game_board.board[pos[0]][pos[1]] = piece
            game_board.board[move[0]][move[1]] = captured
            # If the move doesn't put own king in check, it's valid
            if not in_check:
                valid_moves.append(index_to_algebraic(move[0], move[1]))
        
        # Return the list of valid moves in chess notation
        return jsonify({'moves': valid_moves})
    except:
        # Return empty list if there's any error
        return jsonify({'moves': []})

# API endpoint to get the game move history
@app.route('/api/history', methods=['GET'])
def get_history():
    # Return all moves made in the current game
    return jsonify({'history': game_history})

# Helper function to convert the board state to a format the frontend can understand
def get_board_state():
    """Convert board to frontend-friendly format"""
    board_state = []
    # Loop through each row of the board
    for row in range(8):
        board_row = []
        # Loop through each column of the board
        for col in range(8):
            # Get the piece at this position (if any)
            piece = game_board.board[row][col]
            if piece:
                # If there's a piece, create an object with its details
                board_row.append({
                    'type': piece.__class__.__name__,  # Type of piece (Pawn, Rook, etc.)
                    'color': piece.color,               # Color of piece (w or b)
                    'position': index_to_algebraic(row, col)  # Position in chess notation
                })
            else:
                # If there's no piece, add None
                board_row.append(None)
        # Add this row to the board state
        board_state.append(board_row)
    # Return the complete board state
    return board_state

# Only run the server if this file is executed directly (not imported)
if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, port=5001)  # Debug mode for development, port 5001 