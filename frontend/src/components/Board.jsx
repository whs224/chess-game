import React, { useState } from "react";

export default function Board({ board, onMove }) {
  const [selected, setSelected] = useState(null);

  const handleClick = (r, c) => {
    const pos = `${"abcdefgh"[c]}${8 - r}`;
    if (!selected) {
      setSelected(pos);
    } else {
      onMove(selected + pos);
      setSelected(null);
    }
  };

  return (
    <div className="border-4 border-gray-700">
      {board.map((row, r) => (
        <div key={r} className="grid grid-cols-8">
          {row.map((cell, c) => {
            const isLight = (r + c) % 2 === 0;
            const bg = isLight ? "bg-gray-200" : "bg-green-700";
            const selectedStyle =
              selected === `${"abcdefgh"[c]}${8 - r}` ? "ring-4 ring-yellow-400" : "";

            return (
              <div
                key={`${r}-${c}`}
                onClick={() => handleClick(r, c)}
                className={`${bg} ${selectedStyle} w-14 h-14 flex items-center justify-center text-2xl font-bold cursor-pointer`}
              >
                {cell !== "." ? cell : ""}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
