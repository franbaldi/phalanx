import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [anomalies, setAnomalies] = useState<string[]>([]);

  useEffect(() => {
    const fetchAnomalies = async () => {
      try {
        const response = await fetch('http://localhost:8000/anomalies');
        const data = await response.json();
        setAnomalies(data.anomalies || []);
      } catch (error) {
        console.error('Error fetching anomalies:', error);
      }
    };

    const interval = setInterval(fetchAnomalies, 5000); // Fetch every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Phalanx.ai Security Dashboard</h1>
      </header>
      <main>
        <h2>Detected Anomalies</h2>
        <div className="anomalies-list">
          {anomalies.length > 0 ? (
            <ul>
              {anomalies.map((anomaly, index) => (
                <li key={index}>{anomaly}</li>
              ))}
            </ul>
          ) : (
            <p>No anomalies detected yet.</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;