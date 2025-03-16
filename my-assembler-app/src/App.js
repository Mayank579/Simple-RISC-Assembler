import React from 'react';
import './App.css';
import CodeRunner from './CodeRunner';
import BinaryRain from './BinaryRain';

function App() {
  return (
    <div className="App">
      <div className="background-animation">
        <BinaryRain />
      </div>
      <div className="content-wrapper">
        <header className="app-header">
          <div className="header-content">
            <h1 className="app-title">RISC Assembler</h1>
            <div className="app-subtitle">Simple RISC Architecture IDE</div>
          </div>
        </header>
        <div className="container">
          <CodeRunner />
        </div>
      </div>
    </div>
  );
}

export default App;
