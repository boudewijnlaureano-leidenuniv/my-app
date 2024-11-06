import React from 'react';
import NNLogo from '../src/NN_Logo.png';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="upload-box">
          <div className="header-content">
            <img src={NNLogo} alt="NN Logo" className="logo" />
            <h2>Upload your Zip File</h2>
          </div>
          {/* Custom upload button */}
          <label htmlFor="file-upload" className="custom-file-upload">
            Choose Zip File
          </label>
          <input id="file-upload" type="file" accept=".zip" className="file-input" />
        </div>
      </header>
    </div>
  );
}

export default App;
