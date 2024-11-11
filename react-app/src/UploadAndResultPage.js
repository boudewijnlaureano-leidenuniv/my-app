import React, { useState } from 'react';
import NNLogo from '../src/NN_Logo.png';
import Loader from './Loader';
import { IoIosArrowBack } from "react-icons/io";
import './App.css';

function UploadAndResultPage() {
  const [loading, setLoading] = useState(false);
  const [outputText, setOutputText] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        console.error(`Fetch error: ${response.status} - ${response.statusText}`);
        setLoading(false);
        return;
      }

      const data = await response.json();
      if (data.output) {
        setTimeout(() => {
          setLoading(false);
          setOutputText(data.output);
        }, 2000);
      } else {
        console.error("Error received from server:", data.error);
        alert('Error: ' + data.error);
        setLoading(false);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setLoading(false);
    }
  };

  const resetPage = () => {
    setLoading(false);
    setOutputText('');
  };

  return (
    <header className="App-header">
      <div
        className={`upload-box ${
          loading ? 'loading' : outputText ? 'expanded' : ''
        }`}
      >
        <div className="top-flex-container">
          {outputText && (
            <button onClick={resetPage} className="reset-button">
              <IoIosArrowBack size={22} />
            </button>
          )}
        </div>

        {(!loading && !outputText) && (
          <div className="header-content">
            <img src={NNLogo} alt="NN Logo" className="logo" />
            <h2>Upload your .txt File</h2>
          </div>
        )}

        {!loading && !outputText ? (
          <>
            <label htmlFor="file-upload" className="custom-file-upload">
              Choose File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".txt"
              className="file-input"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </>
        ) : loading ? (
          <Loader />
        ) : (
          <div className="result-text">
            <p>{outputText}</p>
          </div>
        )}
      </div>
    </header>
  );
}

export default UploadAndResultPage;
