import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function TickerInputPage() {
  const [ticker, setTicker] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedTicker = ticker.trim().toUpperCase();
    if (trimmedTicker) {
      try {
        const response = await fetch('http://localhost:8000/api/store-stocks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([trimmedTicker]) 
        });
        const data = await response.json();

        if (response.ok) {
          const analysis = data.results[0].analysis;
          navigate(`/results/${trimmedTicker}`, { state: { analysis } });
        } else {
          console.error('Error storing ticker:', data);
        }
      } catch (error) {
        console.error('Request failed:', error);
      }
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
      <h1 style={styles.heading}>Financial Portfolio Risk Analyzer</h1>
      <p style={styles.subheading}>Get a quick risk snapshot of any stock.</p>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Enter Ticker" 
            value={ticker} 
            onChange={(e) => setTicker(e.target.value)}
            style={styles.input}
          />
          <small style={styles.helper}>Example: AAPL, TSLA, MSFT</small>
          <button type="submit" style={styles.button}>Analyze</button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#1E2A38',
  },
  card: {
    background: '#2a3c4d',
    padding: '70px',
    borderRadius: '16px',
    boxShadow: '0 8px 20px rgba(0,0,0,0.3)',
    textAlign: 'center',
    maxWidth: '500px',
    width: '100%',
  },
  heading: {
    marginBottom: '32px',
    fontSize: '30px',
    color: '#C6CDFF',
    fontWeight: '700',
  },
  subheading: {
    fontSize: '16px',
    color: '#C6CDFF',
    marginBottom: '20px',
  },
  input: {
    width: '100%',
    padding: '12px',
    marginBottom: '20px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    fontSize: '16px',
  },
  button: {
    width: '100%',
    padding: '12px',
    borderRadius: '8px',
    border: 'none',
    background: '#248BD6',
    color: '#fff',
    fontSize: '18px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background 0.3s ease',
  },
  helper: {
    color: '#C6CDFF',
    fontSize: '14px',
    display: 'block',
    marginBottom: '15px',
  }
};

export default TickerInputPage;