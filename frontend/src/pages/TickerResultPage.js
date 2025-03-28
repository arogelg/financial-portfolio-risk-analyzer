import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

function TickerResultPage() {
  const { ticker } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  // Here is just a simulation with results, we just need to replace this with the results of our actual model
  useEffect(() => {
    setTimeout(() => {
      setResult({
        risk: 'Moderate',
        diversification: 'Consider adding bonds to balance your portfolio.',
        analysisDate: new Date().toLocaleDateString(),
      });
      setLoading(false);
    }, 1500);
  }, [ticker]);

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.heading}>Analysis for {ticker}</h1>
        {loading ? (
          <p>Loading results...</p>
        ) : (
          <div style={styles.results}>
            <p><strong>Risk Level:</strong> {result.risk}</p>
            <p><strong>Diversification Suggestion:</strong> {result.diversification}</p>
            <p><strong>Analysis Date:</strong> {result.analysisDate}</p>
          </div>
        )}
        <Link to="/" style={styles.link}>Back</Link>
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
  results: {
    textAlign: 'left',
    marginBottom: '20px',
    color: '#555',
  },
  link: {
    textDecoration: 'none',
    color: '#1890ff',
    fontWeight: 'bold',
  },
};

export default TickerResultPage;
