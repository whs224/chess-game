// Import React library for creating components
import React from 'react';
// Import the ChessPiece component to render pieces on this square
import ChessPiece from './ChessPiece';
// Import the CSS file for styling this component
import './ChessSquare.css';

// ChessSquare component represents one square on the chess board
// Props: position (chess notation), piece (piece object or null), 
// isLight (boolean for square color), isSelected (boolean for selection), 
// onClick (function to handle clicks)
const ChessSquare = ({ position, piece, isLight, isSelected, onClick }) => {
  // Function to determine the CSS class names for this square
  const getSquareClass = () => {
    // Start with the base class name
    let className = 'chess-square';
    // Add 'light' or 'dark' class based on square color
    className += isLight ? ' light' : ' dark';
    // Add 'selected' class if this square is currently selected
    if (isSelected) className += ' selected';
    // Return the complete class name string
    return className;
  };

  // Render the square as a clickable div
  return (
    <div 
      className={getSquareClass()}  // Apply the calculated CSS classes
      onClick={onClick}             // Handle click events
      data-position={position}      // Store position as data attribute for debugging
    >
      {/* Only render a ChessPiece component if there's a piece on this square */}
      {piece && <ChessPiece piece={piece} />}
    </div>
  );
};

// Export the component so it can be imported by other files
export default ChessSquare; 