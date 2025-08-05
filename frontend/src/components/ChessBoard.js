// Import React and its hooks for state management and side effects
import React, { useState, useEffect } from 'react';
// Import the ChessSquare component to render individual squares
import ChessSquare from './ChessSquare';
// Import the CSS file for styling this component
import './ChessBoard.css';

// Main chess board component that handles the entire game interface
const ChessBoard = () => {
  // State to store the current board layout (8x8 array of pieces)
  const [board, setBoard] = useState([]);
  // State to track whose turn it is ('w' for white, 'b' for black)
  const [turn, setTurn] = useState('w');
  // State to track which square is currently selected (null if none)
  const [selectedSquare, setSelectedSquare] = useState(null);
  // State to track if a player is in check
  const [inCheck, setInCheck] = useState(false);
  // State to track if a player is in checkmate
  const [checkmate, setCheckmate] = useState(false);
  // State to store the game move history (currently unused)
  const [gameHistory, setGameHistory] = useState([]);
  // State to display messages to the user (errors, check notifications, etc.)
  const [message, setMessage] = useState('');

  // Base URL for the Flask API server
  const API_BASE = 'http://localhost:5001/api';

  // useEffect hook runs when component mounts (empty dependency array [])
  useEffect(() => {
    // Fetch the initial board state when the component loads
    fetchBoard();
  }, []);

  // Function to fetch the current board state from the backend API
  const fetchBoard = async () => {
    try {
      // Make HTTP GET request to the board endpoint
      const response = await fetch(`${API_BASE}/board`);
      // Parse the JSON response from the server
      const data = await response.json();
      // Update the board state with the server's board layout
      setBoard(data.board);
      // Update whose turn it is
      setTurn(data.turn);
      // Update check status
      setInCheck(data.in_check);
      // Update checkmate status
      setCheckmate(data.checkmate);
    } catch (error) {
      // Log any errors that occur during the API call
      console.error('Error fetching board:', error);
    }
  };

  // Function to handle when a user clicks on a chess square
  const handleSquareClick = async (position) => {
    // If the game is in checkmate, ignore all clicks
    if (checkmate) return;

    // If no square is currently selected
    if (selectedSquare === null) {
      // First click - try to select a piece
      // Convert chess notation to board coordinates
      const [row, col] = positionToCoords(position);
      // Get the piece at this position
      const piece = board[row][col];
      
      // If there's a piece here and it's the current player's piece
      if (piece && piece.color === turn) {
        // Select this square
        setSelectedSquare(position);
      }
    } else {
      // Second click - try to make a move
      // Only make a move if clicking on a different square
      if (selectedSquare !== position) {
        // Attempt to move from selected square to clicked square
        await makeMove(selectedSquare, position);
      }
      // Clear the selection regardless of whether move was made
      setSelectedSquare(null);
    }
  };

  // Function to make a move by sending request to the backend API
  const makeMove = async (start, end) => {
    try {
      // Make HTTP POST request to the move endpoint
      const response = await fetch(`${API_BASE}/move`, {
        method: 'POST',  // HTTP method
        headers: { 'Content-Type': 'application/json' },  // Tell server we're sending JSON
        body: JSON.stringify({ start, end })  // Send the move data as JSON
      });
      
      // Parse the JSON response from the server
      const data = await response.json();
      
      // If the request was successful (HTTP 200)
      if (response.ok) {
        // Update the board with the new state
        setBoard(data.board);
        // Update whose turn it is
        setTurn(data.turn);
        // Update check status
        setInCheck(data.in_check);
        // Update checkmate status
        setCheckmate(data.checkmate);
        // Set the success message
        setMessage(data.message);
        
        // If the game is in checkmate, show winner
        if (data.checkmate) {
          setMessage(`Checkmate! ${data.turn === 'w' ? 'Black' : 'White'} wins!`);
        } else if (data.in_check) {
          // If a player is in check, show which player
          setMessage(`${data.turn === 'b' ? 'Black' : 'White'} is in check!`);
        }
      } else {
        // If the request failed, show the error message
        setMessage(data.error);
      }
    } catch (error) {
      // Log any errors that occur during the API call
      console.error('Error making move:', error);
      // Show a generic error message to the user
      setMessage('Error making move');
    }
  };

  // Function to start a new game
  const newGame = async () => {
    try {
      // Make HTTP POST request to the new-game endpoint
      const response = await fetch(`${API_BASE}/new-game`, {
        method: 'POST'
      });
      // Parse the JSON response
      const data = await response.json();
      // Reset all game state to initial values
      setBoard(data.board);
      setTurn(data.turn);
      setInCheck(false);
      setCheckmate(false);
      setSelectedSquare(null);
      setMessage(data.message);
    } catch (error) {
      // Log any errors that occur during the API call
      console.error('Error starting new game:', error);
    }
  };

  // Helper function to convert chess notation to board coordinates
  const positionToCoords = (position) => {
    // Convert file (a-h) to column index (0-7)
    // 'a' has ASCII code 97, so 'a' - 97 = 0, 'b' - 97 = 1, etc.
    const file = position.charCodeAt(0) - 97;
    // Convert rank (1-8) to row index (0-7)
    // Rank 8 becomes row 0, rank 7 becomes row 1, etc.
    const rank = 8 - parseInt(position[1]);
    // Return [row, col] coordinates
    return [rank, file];
  };

  // Helper function to check if a square is currently selected
  const isSquareSelected = (position) => {
    return selectedSquare === position;
  };

  // Function to render the 8x8 chess board grid
  const renderBoard = () => {
    const squares = [];
    // Loop through each row of the board
    for (let row = 0; row < 8; row++) {
      // Loop through each column of the board
      for (let col = 0; col < 8; col++) {
        // Convert board coordinates to chess notation (e.g., 0,0 -> "a8")
        const position = String.fromCharCode(97 + col) + (8 - row);
        // Get the piece at this position (if any)
        const piece = board[row]?.[col];
        // Determine if this square should be light or dark
        // Light squares are where row + col is even
        const isLight = (row + col) % 2 === 0;
        
        // Create a ChessSquare component for this position
        squares.push(
          <ChessSquare
            key={position}  // React needs a unique key for each element in array
            position={position}  // Chess notation (e.g., "e4")
            piece={piece}  // Piece object or null
            isLight={isLight}  // Whether square is light or dark
            isSelected={isSquareSelected(position)}  // Whether this square is selected
            onClick={() => handleSquareClick(position)}  // Click handler
          />
        );
      }
    }
    // Return array of all 64 square components
    return squares;
  };

  // Render the complete chess interface
  return (
    <div className="chess-container">
      {/* Header section with game info and controls */}
      <div className="chess-header">
        <h1>Chess Game</h1>
        <div className="game-info">
          {/* Show whose turn it is with color coding */}
          <span className={`turn-indicator ${turn === 'w' ? 'white' : 'black'}`}>
            {turn === 'w' ? 'White' : 'Black'}'s turn
          </span>
          {/* Show check indicator if a player is in check */}
          {inCheck && <span className="check-indicator">CHECK!</span>}
          {/* Show checkmate indicator if game is over */}
          {checkmate && <span className="checkmate-indicator">CHECKMATE!</span>}
        </div>
        {/* Button to start a new game */}
        <button className="new-game-btn" onClick={newGame}>
          New Game
        </button>
      </div>
      
      {/* Display any game messages (errors, check notifications, etc.) */}
      {message && (
        <div className="message">
          {message}
        </div>
      )}
      
      {/* Main board container with coordinates */}
      <div className="board-container">
        {/* Rank labels (1-8) on the left side */}
        <div className="rank-labels">
          {[8, 7, 6, 5, 4, 3, 2, 1].map(rank => (
            <div key={rank} className="rank-label">{rank}</div>
          ))}
        </div>
        
        {/* Board and file labels container */}
        <div className="board-with-labels">
          {/* The actual 8x8 chess board grid */}
          <div className="chess-board">
            {renderBoard()}
          </div>
          
          {/* File labels (a-h) on the bottom */}
          <div className="file-labels">
            {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(file => (
              <div key={file} className="file-label">{file}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Export the component so it can be imported by other files
export default ChessBoard; 