// Import React library for creating components
import React from 'react';
// Import the main ChessBoard component that contains the entire game
import ChessBoard from './components/ChessBoard';
// Import the CSS file for styling this component
import './App.css';

// App component is the root component of the React application
function App() {
  // Render the main application structure
  return (
    // Main container div with "App" class for styling
    <div className="App">
      {/* Render the ChessBoard component which contains the entire chess game */}
      <ChessBoard />
    </div>
  );
}

// Export the App component so it can be used as the entry point
export default App;
