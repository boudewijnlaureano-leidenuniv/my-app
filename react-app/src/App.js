import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadAndResultPage from './UploadAndResultPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadAndResultPage />} />
      </Routes>
    </Router>
  );
}

export default App;