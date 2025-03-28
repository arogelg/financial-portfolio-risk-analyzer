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
          navigate(`/results/${trimmedTicker}`);
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
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Enter Ticker (e.g. AAPL)" 
            value={ticker} 
            onChange={(e) => setTicker(e.target.value)}
            style={styles.input}
          />
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
    background: '#f0f2f5',
  },
  card: {
    background: '#fff',
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
    textAlign: 'center',
    maxWidth: '400px',
    width: '100%',
  },
  heading: {
    marginBottom: '20px',
    fontSize: '24px',
    color: '#333',
  },
  input: {
    width: 'calc(100% - 20px)',
    padding: '10px',
    marginBottom: '20px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '16px',
  },
  button: {
    width: '100%',
    padding: '10px',
    borderRadius: '4px',
    border: 'none',
    background: '#1890ff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
  },
};

export default TickerInputPage;