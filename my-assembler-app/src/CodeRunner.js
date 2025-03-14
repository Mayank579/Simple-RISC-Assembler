import React, { useState } from 'react';

function CodeRunner() {
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');

  const handleRunCode = async () => {
    try {
      setOutput("Running code...");
      const response = await fetch("http://127.0.0.1:5000/run-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
      });
      const data = await response.json();
      setOutput(data.output);
    } catch (error) {
      setOutput("Error: " + error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Simple RISC Assembler</h2>
      <textarea
        rows="10"
        cols="50"
        placeholder="Enter your Simple RISC code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
        style={{ display: 'block', marginBottom: '10px' }}
      ></textarea>
      <button onClick={handleRunCode}>Run</button>
      <h3>Output:</h3>
      <pre style={{ background: '#f4f4f4', padding: '10px' }}>{output}</pre>
    </div>
  );
}

export default CodeRunner;
