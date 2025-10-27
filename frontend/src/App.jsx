import React, { useState, useEffect } from "react";
import Board from "./components/Board";

export default function App() {
  const [board, setBoard] = useState([]);
  const [turn, setTurn] = useState("w");
  const [message, setMessage] = useState(""); // 🧩 New: for check/checkmate messages

  // Fetch the board from backend
  const fetchBoard = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/board");
      const data = await res.json();
      setBoard(data.board);
      setTurn(data.turn);
      setMessage(data.message || ""); // optional message
    } catch (err) {
      console.error("Failed to fetch board:", err);
    }
  };

  // Make a move
  const handleMove = async (moveStr) => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ move: moveStr }),
      });
      const data = await res.json();
      setBoard(data.board);
      setTurn(data.turn);
      setMessage(data.message || ""); // 🧠 show check/checkmate info
    } catch (err) {
      console.error("Move failed:", err);
      setMessage("Move failed. Try again.");
    }
  };

  // Reset the game
  const resetGame = async () => {
    try {
      await fetch("http://127.0.0.1:5000/api/reset", { method: "POST" });
      setMessage("");
      fetchBoard();
    } catch (err) {
      console.error("Reset failed:", err);
      setMessage("Reset failed. Try again.");
    }
  };

  useEffect(() => {
    fetchBoard();
  }, []);

  // 🟢 Style the message by its content
  const messageColor = message.includes("Checkmate")
    ? "text-green-400"
    : message.includes("Stalemate")
    ? "text-yellow-400"
    : message.includes("Check")
    ? "text-red-400"
    : "text-gray-300";

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-6">Python Chess</h1>

      {message && (
        <div className={`mb-3 text-lg font-semibold ${messageColor}`}>
          {message}
        </div>
      )}

      {Array.isArray(board) && board.length > 0 ? (
        <Board board={board} onMove={handleMove} />
      ) : (
        <p>Loading board...</p>
      )}

      <div className="mt-4 text-lg">Turn: {turn === "w" ? "White" : "Black"}</div>

      <button
        onClick={resetGame}
        className="mt-4 px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
      >
        Reset Game
      </button>
    </div>
  );
}
