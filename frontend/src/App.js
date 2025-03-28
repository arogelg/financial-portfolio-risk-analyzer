import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TickerInputPage from './pages/TickerInputPage';
import TickerResultPage from './pages/TickerResultPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TickerInputPage />} />
        <Route path="/results/:ticker" element={<TickerResultPage />} />
      </Routes>
    </Router>
  );
}

export default App;
