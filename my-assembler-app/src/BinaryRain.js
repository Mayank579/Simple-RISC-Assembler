import React, { useEffect, useState } from 'react';

function BinaryRain() {
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    const createRainColumn = () => {
      const column = {
        left: `${Math.random() * 100}%`,
        animationDuration: `${5 + Math.random() * 10}s`,
        digits: Array(20).fill(0).map(() => Math.random() < 0.5 ? '0' : '1'),
        delays: Array(20).fill(0).map(() => Math.random() * 2)
      };
      return column;
    };

    const columnCount = Math.floor(window.innerWidth / 20);
    const initialColumns = Array(columnCount).fill(0).map(createRainColumn);
    setColumns(initialColumns);

    const interval = setInterval(() => {
      setColumns(cols => {
        const newCols = [...cols];
        const randomIndex = Math.floor(Math.random() * cols.length);
        newCols[randomIndex] = createRainColumn();
        return newCols;
      });
    }, 100);

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
