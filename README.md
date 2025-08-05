# Chess Web Application

A beautiful chess game built with React.js frontend and Python Flask backend, using your existing chess engine.

## Features

- 🎮 Full chess game functionality
- ♟️ Beautiful chess board with Unicode pieces
- 🎯 Move validation and legal move highlighting
- ⚡ Real-time game state updates
- 📱 Responsive design for mobile devices
- 🏆 Check and checkmate detection
- 🔄 New game functionality

## Project Structure

```
chess-web/
├── backend/           # Python Flask API server
│   ├── app.py        # Flask application
│   ├── chess_board.py # Your chess board logic
│   ├── chess_engine.py # Your chess piece classes
│   ├── utils.py      # Utility functions
│   └── requirements.txt
└── frontend/         # React.js application
    ├── src/
    │   ├── components/
    │   │   ├── ChessBoard.js
    │   │   ├── ChessSquare.js
    │   │   ├── ChessPiece.js
    │   │   └── *.css files
    │   ├── App.js
    │   └── App.css
    └── package.json
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd chess-web/backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd chess-web/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

## How to Play

1. Open your browser and go to `http://localhost:3000`
2. The game starts with White's turn
3. Click on a piece to select it (valid moves will be highlighted in green)
4. Click on a highlighted square to make your move
5. The game will automatically detect check, checkmate, and illegal moves
6. Click "New Game" to start a fresh game

## API Endpoints

The Flask backend provides the following API endpoints:

- `GET /api/board` - Get current board state
- `POST /api/move` - Make a move (requires start and end positions)
- `POST /api/valid-moves` - Get valid moves for a piece
- `POST /api/new-game` - Start a new game
- `GET /api/history` - Get move history

## Deployment

### Backend Deployment

For production deployment, you can use:
- Heroku
- PythonAnywhere
- AWS EC2
- Google Cloud Platform

Make sure to:
1. Set `FLASK_ENV=production`
2. Use a production WSGI server like Gunicorn
3. Configure CORS for your domain

### Frontend Deployment

For production deployment, you can use:
- Netlify
- Vercel
- GitHub Pages
- AWS S3

1. Build the production version:
   ```bash
   npm run build
   ```

2. Deploy the `build` folder to your hosting service

## Technologies Used

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: React.js, CSS3
- **Chess Engine**: Your custom Python chess implementation

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the UI/UX
- Fixing bugs
- Adding tests

## License

This project is open source and available under the MIT License. 