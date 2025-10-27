from flask import Flask, request, jsonify
from flask_cors import CORS
from chess.chess_board import Board
import os

if os.environ.get("RENDER") == "true":
    from waitress import serve

app = Flask(__name__)
CORS(app)

board = Board()

@app.route("/api/board")
def get_board():
    try:
        return jsonify({
            "board": board.board,
            "turn": board.turn
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/move", methods=["POST"])
def make_move():
    try:
        data = request.get_json()
        move_str = data.get("move")

        if not move_str or len(move_str) < 4:
            return jsonify({
                "board": board_as_simple_chars(board),
                "turn": board.turn,
                "success": False,
                "message": "Invalid move"
            }), 200

        m = board.parse_move_str(move_str)
        if not m:
            return jsonify({
                "board": board_as_simple_chars(board),
                "turn": board.turn,
                "success": False,
                "message": "Illegal move"
            }), 200

        board.make_move(m)
        success = True

        message = None
        if board.is_checkmate():
            message = f"Checkmate! {'White' if board.turn == 'b' else 'Black'} wins."
        elif board.is_stalemate():
            message = "Stalemate! It's a draw."
        elif board.is_in_check(board.turn):
            message = f"Check! {'White' if board.turn == 'w' else 'Black'} is in check."

        return jsonify({
            "board": board_as_simple_chars(board),
            "turn": board.turn,
            "success": success,
            "message": message
        }), 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "error": str(e),
            "board": board_as_simple_chars(board),
            "turn": board.turn
        }), 500


@app.route("/api/reset", methods=["POST"])
def reset_game():
    global board
    board = Board()
    return jsonify({"message": "Game reset!"})


def board_as_simple_chars(board):
    grid = []
    for r in range(8):
        row = []
        for c in range(8):
            p = board.board[r][c]
            row.append(p.symbol() if p else ".")
        grid.append(row)
    return grid


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if os.environ.get("RENDER") == "true":
        serve(app, host="0.0.0.0", port=port)
    else:
        app.run(host="0.0.0.0", port=port, debug=True)
