import React, { useState, useEffect } from 'react';

function RegisterDisplay({ registers, format }) {
  const [prevRegisters, setPrevRegisters] = useState(registers);
  const [changed, setChanged] = useState(new Set());

  useEffect(() => {
    console.log("Registers updated:", registers);
    // Detect changed values
    const changedIndexes = new Set();
    registers.forEach((value, idx) => {
      if (value !== prevRegisters[idx]) {
        changedIndexes.add(idx);
        console.log(`Register ${idx} changed: ${prevRegisters[idx]} -> ${value}`);
      }
    });
    setChanged(changedIndexes);
    setPrevRegisters([...registers]);

    // Clear highlights after animation
    if (changedIndexes.size > 0) {
      setTimeout(() => setChanged(new Set()), 1000);
    }
  }, [registers]);

  const formatValue = (value) => {
    const numValue = Number(value);
    try {
      switch(format) {
        case 'hex':
          // Only show necessary digits for hex, minimum 1 digit
          return '0x' + numValue.toString(16).toUpperCase();
        case 'decimal':
          // Show decimal numbers normally without padding
          return numValue.toString(10);
        case 'binary':
          // Group binary in 4-bit chunks, remove leading zeros if possible
          const binStr = numValue.toString(2);
          const padded = binStr.padStart(Math.ceil(binStr.length / 4) * 4, '0');
          return padded.replace(/(.{4})/g, '$1 ').trim();
        default:
          return numValue.toString();
      }
    } catch (error) {
      return "ERROR";
    }
  };

  return (
    <div className="register-panel">
      <div className="panel-header">
        <h2>Registers</h2>
      </div>
      <div className="registers-grid">
        {registers.map((value, index) => (
          <div 
            key={index} 
            className="register-item"
          >
            <span className="register-name">
              R{index.toString().padStart(2, '0')}
            </span>
            <span className={`register-value ${changed.has(index) ? 'register-value-changed' : ''}`}>
              {formatValue(value)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RegisterDisplay;
