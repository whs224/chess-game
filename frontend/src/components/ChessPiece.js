// Import React library for creating components
import React from 'react';
// Import the CSS file for styling this component
import './ChessPiece.css';

// ChessPiece component renders a single chess piece using Unicode symbols
// Props: piece (object with type and color properties)
const ChessPiece = ({ piece }) => {
  // Function to get the Unicode symbol for this piece
  const getPieceSymbol = () => {
    // Extract the piece type and color from the piece object
    const { type, color } = piece;
    // Determine if this is a white piece
    const isWhite = color === 'w';
    
    // Object mapping piece types to Unicode symbols
    // Different symbols for white vs black pieces
    const symbols = {
      'King': isWhite ? '♔' : '♚',      // White king vs black king
      'Queen': isWhite ? '♕' : '♛',     // White queen vs black queen
      'Rook': isWhite ? '♖' : '♜',      // White rook vs black rook
      'Bishop': isWhite ? '♗' : '♝',    // White bishop vs black bishop
      'Knight': isWhite ? '♘' : '♞',    // White knight vs black knight
      'Pawn': isWhite ? '♙' : '♟'       // White pawn vs black pawn
    };
    
    // Return the appropriate symbol, or '?' if piece type is unknown
    return symbols[type] || '?';
  };

  // Render the piece as a div with appropriate CSS classes
  return (
    <div className={`chess-piece ${piece.color === 'w' ? 'white' : 'black'}`}>
      {/* Display the Unicode symbol for this piece */}
      {getPieceSymbol()}
    </div>
  );
};

// Export the component so it can be imported by other files
export default ChessPiece; 