import React from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';

function ResultPage() {
  const location = useLocation();
  const outputText = location.state?.output || 'No output available';

  return (
    <header className="App-header">
      <div className="result-box expanded">
        <p>{outputText}</p>
      </div>
    </header>
  );
}

export default ResultPage;
