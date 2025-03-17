import React, { useEffect, useState } from 'react';

function BinaryRain() {
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    const createRainColumn = () => ({
      left: `${Math.random() * 100}%`,
      animationDuration: `${8 + Math.random() * 15}s`,  // Slower animation
      digits: Array(10).fill(0).map(() => Math.random() < 0.5 ? '0' : '1'),  // Reduced digits
      delays: Array(10).fill(0).map(() => Math.random() * 3)
    });

    // Reduce number of columns
    const columnCount = Math.floor(window.innerWidth / 50);  // Fewer columns
    const initialColumns = Array(columnCount).fill(0).map(createRainColumn);
    setColumns(initialColumns);

    // Slower update interval
    const interval = setInterval(() => {
      setColumns(cols => {
        const newCols = [...cols];
        const randomIndex = Math.floor(Math.random() * cols.length);
        newCols[randomIndex] = createRainColumn();
        return newCols;
      });
    }, 500);  // Increased interval

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="binary-rain">
      {columns.map((column, i) => (
        <div
          key={i}
          className="rain-column"
          style={{
            left: column.left,
            animationDuration: column.animationDuration
          }}
        >
          {column.digits.map((digit, j) => (
            <span
              key={j}
              className="rain-digit"
              style={{
                animationDelay: `${column.delays[j]}s`
              }}
            >
              {digit}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
}

export default BinaryRain;
