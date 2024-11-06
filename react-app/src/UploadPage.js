import React, { useState } from 'react';
import NNLogo from '../src/NN_Logo.png';
import Loader from './Loader';
import './App.css';

function UploadPage() {
  const [loading, setLoading] = useState(false);
  const [outputText, setOutputText] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:3001/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.output) {
        // Delay to show the loader for 'x' seconds
        setTimeout(() => {
          setOutputText(data.output);
          setLoading(false);
        }, 2000); // Adjust delay here (2000 ms = 2 seconds)
      } else {
        alert('Error: ' + data.error);
        setLoading(false);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setLoading(false);
    }
  };

  return (
    <header className="App-header">
      <div className="upload-box">
        {!outputText && (
          <>
            <div className="header-content">
              <img src={NNLogo} alt="NN Logo" className="logo" />
              <h2>Upload your .txt File</h2>
            </div>
            <label htmlFor="file-upload" className="custom-file-upload">
              Choose File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".txt"
              className="file-input"
              onChange={handleFileChange}
              style={{ display: 'none' }} // Hide the default file input
            />
          </>
        )}
        {loading && <Loader />}
        {outputText && (
          <div className="result-text">
            <p>{outputText}</p>
          </div>
        )}
      </div>
    </header>
  );
}

export default UploadPage;
