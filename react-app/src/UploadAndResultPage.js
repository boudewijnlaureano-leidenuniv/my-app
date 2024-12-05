import React, { useState } from 'react';
import NNLogo from '../src/NN_Logo.png';
import Loader from './Loader';
import { IoIosArrowBack } from "react-icons/io";
import './App.css';

function UploadAndResultPage() {
  const [loading, setLoading] = useState(false);
  const [outputJson, setOutputJson] = useState(null); // Store JSON response

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    console.log(file)
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        console.error(`Error pointer: Fetch error: ${response.status} - ${response.statusText}`);
        setLoading(false);
        return;
      }

      const data = await response.json();
      if (data.output) {
        setTimeout(() => {
          setLoading(false);
          setOutputJson(data.output); // Store raw JSON
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
    setOutputJson(null);
  };

  return (
    <header className="App-header">
      <div
        className={`upload-box ${
          loading ? 'loading' : outputJson ? 'expanded' : ''
        }`}
      >
        <div className="top-flex-container">
          {outputJson && (
            <button onClick={resetPage} className="reset-button">
              <IoIosArrowBack size={22} />
            </button>
          )}
        </div>

        {(!loading && !outputJson) && (
          <div className="header-content">
            <img src={NNLogo} alt="NN Logo" className="logo" />
            <h2>Upload your .zip</h2>
          </div>
        )}

        {!loading && !outputJson ? (
          <>
            <label htmlFor="file-upload" className="custom-file-upload">
              Choose File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".txt,.zip" // Allow .txt and .zip
              className="file-input"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </>
        ) : loading ? (
          <Loader />
        ) : (
          <div className="result-json">
            <h3>Analysis Result (Raw JSON):</h3>
            <pre style={{ textAlign: 'left', backgroundColor: '#f4f4f4', padding: '10px', borderRadius: '5px' }}>
              {JSON.stringify(outputJson, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </header>
  );
}

export default UploadAndResultPage;
