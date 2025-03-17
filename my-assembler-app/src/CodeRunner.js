import React, { useState } from "react";
import RegisterDisplay from "./RegisterDisplay";
import "./CodeRunner.css";

function CodeRunner() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [format, setFormat] = useState("binary");
  const [registers, setRegisters] = useState(Array(16).fill(0));

  const handleCompile = async () => {
    try {
      setOutput("Compiling...");

      const response = await fetch(
        "https://simple-risc-assembler.onrender.com/run-code",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code }),
        }
      );

      const data = await response.json();

      if (data.registers) {
        console.log("Updating registers:", data.registers);
        setRegisters(data.registers); // Update register state
      }

      setOutput(data.output || "Compilation completed");
    } catch (error) {
      setOutput("Error: " + error.message);
    }
  };

  const convertNumber = (binaryStr) => {
    const num = parseInt(binaryStr, 2);
    switch (format) {
      case "hex":
        return "0x" + num.toString(16).toUpperCase().padStart(8, "0");
      case "decimal":
        return num.toString(10);
      default:
        return binaryStr;
    }
  };

  const formatOutput = (output) => {
    if (!output) return "Output will appear here...";
    return output
      .split("\n")
      .map((line) =>
        line.trim().match(/^[01]{32}$/) ? convertNumber(line) : line
      )
      .join("\n");
  };

  return (
    <div className="code-container">
      <div className="left-panel">
        <div className="editor-panel">
          <div className="panel-header">
            <h2>Code Editor</h2>
            <button className="compile-button" onClick={handleCompile}>
              <span className="compile-icon">⚙</span> Compile
            </button>
          </div>
          <textarea
            className="code-editor"
            placeholder="Enter your Simple RISC code here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            spellCheck="false"
          />
        </div>
      </div>
      <div className="right-panel">
        <div className="output-panel">
          <div className="panel-header">
            <h2>Output</h2>
            <div className="format-buttons">
              <button
                className={`format-button ${
                  format === "binary" ? "active" : ""
                }`}
                onClick={() => setFormat("binary")}
              >
                Binary
              </button>
              <button
                className={`format-button ${format === "hex" ? "active" : ""}`}
                onClick={() => setFormat("hex")}
              >
                Hex
              </button>
              <button
                className={`format-button ${
                  format === "decimal" ? "active" : ""
                }`}
                onClick={() => setFormat("decimal")}
              >
                Decimal
              </button>
            </div>
          </div>
          <pre className="output-display">{formatOutput(output)}</pre>
        </div>
        <RegisterDisplay registers={registers} format={format} />
      </div>
    </div>
  );
}

export default CodeRunner;
