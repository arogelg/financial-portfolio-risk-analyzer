import React from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';

function TickerResultPage() {
  const { state } = useLocation();
  const { ticker } = useParams();
  const analysis = state?.analysis;

  if (!analysis) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2>No analysis available for <span style={{ color: '#1890ff' }}>{ticker}</span></h2>
          <p>Try searching again.</p>
          <Link to="/" style={styles.link}>← Back to Search</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.heading}>Risk Analysis for {analysis.ticker}</h2>
        <div style={styles.results}>
          <p><strong>📊 Risk Level:</strong> {analysis.predicted_risk_level}</p>
          <p><strong>🎯 Confidence:</strong> {analysis.confidence_score}</p>
          <p><strong>✅ Model Accuracy:</strong> {analysis.model_accuracy}</p>
          <p><strong>💰 Latest Close:</strong> ${analysis.latest_close}</p>
          <p><strong>⚠️ VaR (95%):</strong> {analysis.latest_VaR_95}</p>
          <p><strong>📉 Volatility (5d):</strong> {analysis.latest_volatility}</p>
        </div>
        <Link to="/" style={styles.link}>← Analyze another ticker</Link>
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
    maxWidth: '500px',
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
