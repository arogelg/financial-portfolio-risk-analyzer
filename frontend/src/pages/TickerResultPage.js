import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useEffect, useState } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';

function TickerResultPage() {
  const { state } = useLocation();
  const { ticker } = useParams();
  const analysis = state?.analysis;

  const [priceHistory, setPriceHistory] = useState([]);

  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/history/${ticker}`);
        const data = await res.json();
        setPriceHistory(data);
      } catch (error) {
        console.error("Failed to fetch price history:", error);
      }
    };
    fetchHistory();
  }, [ticker]);

  if (!analysis) {
    return <div style={styles.container}>No analysis available for {ticker}</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>{ticker}</h1>
        <h2 style={styles.subtitle}>Risk Analysis Summary</h2>
        
        <table style={styles.table}>
          <tbody>
          <TableRow label="Risk Level" value={analysis.predicted_risk_level} />
          <TableRow label="Confidence" value={analysis.confidence_score} />
          <TableRow label="Model Accuracy" value={analysis.model_accuracy} />
          <TableRow label="Latest Closing Price" value={`$${analysis.latest_close}`} />
          <TableRow label="Value at Risk (95%)" value={analysis.latest_VaR_95} />
          <TableRow label="5-Day Volatility" value={analysis.latest_volatility} />
          </tbody>
        </table>

        <div style={styles.graphContainer}>
      <h3 style={styles.graphTitle}>Recent Price Trend (30 days)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={priceHistory}>
          <XAxis dataKey="date" tick={{ fill: '#C6CDFF', fontSize: 12 }} />
          <YAxis tick={{ fill: '#C6CDFF', fontSize: 12 }} />
          <Tooltip />
          <Line type="monotone" dataKey="close" stroke="#83B8FF" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>

    <button onClick={() => setShowHelp(prev => !prev)} style={styles.helpButton}>
  {showHelp ? 'Hide Help' : 'Understand This Analysis'}
</button>

{showHelp && (
  <div style={styles.helpSection}>
    <h3 style={styles.helpTitle}>Quick Guide</h3>
    <ul style={styles.helpText}>
      <li><strong>Risk Level</strong>: High = risky but might reward big. Low = safer but slower returns.</li>
      <li><strong>Confidence</strong>: 1 = the model is very sure. Closer to 0.5 = not so confident.</li>
      <li><strong>Model Accuracy</strong>: Accuracy when tested. 0.90+ = very good, below 0.7 = caution.</li>
      <li><strong>Value at Risk (VaR)</strong>: Expected daily loss in bad scenarios. Closer to 0 is better.</li>
      <li><strong>Volatility</strong>: How much prices bounce around.
        <br />— 0.01 or less = stable
        <br />— 0.02 to 0.04 = moderate
        <br />— 0.05+ = very volatile</li>
    </ul>
    <p style={styles.helpText}>
      Long-term investors may prefer lower risk and volatility.<br />
      Short-term or high-reward seekers may tolerate more risk.
    </p>
  </div>
)}

    <Link to="/" style={styles.link}>← Analyze another ticker</Link>
  </div>
  <div>
    
  </div>
</div>
    
  );
}

function TableRow({ label, value }) {
  return (
    <tr>
      <td style={styles.cellLabel}><strong>{label}</strong></td>
      <td style={styles.cellValue}>{value}</td>
    </tr>
  );
}

const styles = {
  container: {
    backgroundColor: '#1E2A38',
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontFamily: 'Arial, sans-serif',
    color: '#ffffff',
    padding: '20px',
  },
  card: {
    background: '#1E2A38',
    padding: '40px',
    borderRadius: '16px',
    boxShadow: '0 8px 16px rgba(0,0,0,0.3)',
    maxWidth: '800px', 
    width: '100%',
    color: '#C6CDFF',
  },
  title: {
    color: '#248BD6',
    fontSize: '32px',
    marginBottom: '10px',
    textAlign: 'center',
  },
  subtitle: {
    color: '#C6CDFF',
    fontSize: '20px',
    marginBottom: '30px',
    textAlign: 'center',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginBottom: '30px',
  },
  cellLabel: {
    textAlign: 'left',
    padding: '12px',
    borderBottom: '1px solid #3f4f63',
    width: '70%',
  },
  cellValue: {
    textAlign: 'right',
    padding: '12px',
    borderBottom: '1px solid #3f4f63',
    fontWeight: 'bold',
    color: '#83B8FF',
  },
  explainer: {
    fontSize: '12px',
    color: '#C6CDFF',
    display: 'block',
    marginTop: '4px',
  },
  link: {
    color: '#83B8FF',
    textAlign: 'center',
    display: 'block',
    textDecoration: 'none',
    marginTop: '10px',
  },
  graphContainer: {
    marginTop: '30px'
  },
  graphTitle: {
    color: '#C6CDFF',
    marginBottom: '1rem',
    textAlign: 'center',
  },
  helpSection: {
    marginTop: '30px',
    backgroundColor: '#2a3c4d',
    padding: '20px',
    borderRadius: '12px',
  },
  helpTitle: {
    color: '#83B8FF',
    marginBottom: '12px',
  },
  helpText: {
    fontSize: '14px',
    lineHeight: '1.6',
    color: '#C6CDFF'
  },
  helpButton: {
    backgroundColor: '#248BD6',
    color: '#fff',
    padding: '10px 16px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    marginBottom: '20px',
    fontSize: '14px',
    fontWeight: 'bold',
    transition: 'background 0.3s ease',
    display: 'block',
    margin: '20px auto',
  },
};

export default TickerResultPage;
