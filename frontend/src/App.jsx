import React, { useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Scatter
} from 'recharts';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [columns, setColumns] = useState([]);
  const [edaStats, setEdaStats] = useState(null);
  
  const [anomalyData, setAnomalyData] = useState(null);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [nlgInsight, setNlgInsight] = useState('');
  
  const [chatQuery, setChatQuery] = useState('');
  const [chatLog, setChatLog] = useState([{role: 'bot', text: 'Hello! I am the Intelligent Assistant.'}]);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const uploadRes = await axios.post('http://localhost:8000/upload', formData);
      const numColumns = uploadRes.data.columns;
      setColumns(numColumns);
      if(numColumns.length > 0) setSelectedColumn(numColumns[0]);

      const edaRes = await axios.post('http://localhost:8000/analyze/eda', formData);
      setEdaStats(edaRes.data.descriptive_statistics);
    } catch (err) {
        console.error(err);
        alert("Failed to process data.");
    } finally {
      setLoading(false);
    }
  };

  const runAnomalyDetection = async () => {
    if (!file || !selectedColumn) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`http://localhost:8000/analyze/anomalies/${selectedColumn}`, formData);
      
      const rawValues = res.data.values;
      const trendValues = res.data.trend.moving_average;
      const anomalyIndices = res.data.anomalies.anomaly_indices;
      
      const chartData = rawValues.map((val, idx) => ({
        index: idx,
        value: val,
        trend: trendValues[idx] || null,
        anomaly: anomalyIndices.includes(idx) ? val : null
      }));

      setAnomalyData(chartData);
      setNlgInsight(res.data.insight);
    } catch (err) {
       console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async () => {
    if(!chatQuery) return;
    const newLog = [...chatLog, {role: 'user', text: chatQuery}];
    setChatLog(newLog);
    setChatQuery('');
    
    try {
      const res = await axios.post('http://localhost:8000/chat', {query: chatQuery});
      setChatLog([...newLog, {role: 'bot', text: res.data.reply}]);
    } catch (err) {
      console.error(err);
    }
  };

  const downloadReport = async () => {
    if(!nlgInsight) {
      alert("Generate some insights first!");
      return;
    }
    try {
      const form = new FormData();
      form.append("insights", nlgInsight);
      const res = await axios.post('http://localhost:8000/report/download', form);
      alert(`Report generated! Path: ${res.data.mock_url}\n\nContent Preview:\n${res.data.raw_text}`);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="dashboard-container" style={{display: 'flex', gap: '2rem'}}>
      
      <div style={{flex: 3}}>
        <header className="header">
          <h1>Nexus Analytics AI</h1>
          <div>Phase 2 Active</div>
        </header>

        <section className="upload-section">
          <h2>Ingest Knowledge</h2>
          <form onSubmit={handleFileUpload} style={{marginTop: '2rem'}}>
            <div className="file-input-wrapper">
              <button className="btn-upload" type="button">
                {file ? file.name : 'Select CSV Data Source'}
              </button>
              <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
            </div>
            {file && (
              <div style={{marginTop: '1rem'}}>
                <button type="submit" className="btn-upload" style={{backgroundColor: 'var(--success)'}} disabled={loading}>
                  {loading ? <span className="loader"></span> : 'Run Intelligence Pipeline'}
                </button>
              </div>
            )}
          </form>
        </section>

        {edaStats && (
          <section>
            <div className="kpi-grid">
              {Object.keys(edaStats).slice(0, 3).map(col => (
                <div className="kpi-card" key={col}>
                  <h3>{col} (Mean)</h3>
                  <div className="value">{edaStats[col].mean.toFixed(2)}</div>
                </div>
              ))}
            </div>

            <div className="chart-container" style={{marginBottom: '2rem'}}>
              <h2>Advanced Anomaly Detection</h2>
              <div style={{display: 'flex', gap: '1rem', marginBottom: '1rem'}}>
                <select value={selectedColumn} onChange={e => setSelectedColumn(e.target.value)} style={{padding: '0.5rem', background: 'var(--panel-bg)', color: 'white', border: '1px solid var(--border-color)'}}>
                  {columns.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
                <button className="btn-upload" onClick={runAnomalyDetection} disabled={loading}>Detect Anomalies</button>
              </div>

              {nlgInsight && (
                <div style={{padding: '1rem', backgroundColor: 'rgba(99, 102, 241, 0.1)', borderLeft: '4px solid var(--accent-color)', marginBottom: '1rem'}}>
                  <strong>AI Generated Insight:</strong> {nlgInsight}
                </div>
              )}

              {anomalyData && (
                <>
                  <div style={{height: 350, marginTop: '2rem'}}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={anomalyData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#2d3142" />
                        <XAxis dataKey="index" stroke="#a0a4b8" />
                        <YAxis stroke="#a0a4b8" />
                        <Tooltip contentStyle={{backgroundColor: '#1e2130', border: '1px solid #2d3142'}} />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke="#6366f1" dot={false} strokeWidth={2} name="Raw Metric" />
                        <Line type="monotone" dataKey="trend" stroke="#10b981" dot={false} strokeWidth={2} strokeDasharray="5 5" name="Trend" />
                        <Scatter dataKey="anomaly" fill="#ef4444" name="Anomalies" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  <button className="btn-upload" style={{marginTop: '1rem', backgroundColor: '#ec4899'}} onClick={downloadReport}>
                    Export PDF Report
                  </button>
                </>
              )}
            </div>
          </section>
        )}
      </div>

      <div style={{flex: 1, backgroundColor: 'var(--panel-bg)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column'}}>
        <h3 style={{marginTop: 0}}>AI Chat Assistant</h3>
        <div style={{flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
          {chatLog.map((chat, i) => (
             <div key={i} style={{alignSelf: chat.role === 'user' ? 'flex-end' : 'flex-start', background: chat.role === 'user' ? 'var(--accent-color)' : '#2d3142', padding: '0.8rem', borderRadius: '8px', maxWidth: '85%'}}>
               {chat.text}
             </div>
          ))}
        </div>
        <div style={{display: 'flex', gap: '0.5rem', marginTop: '1rem'}}>
          <input 
             type="text" 
             value={chatQuery} 
             onChange={e => setChatQuery(e.target.value)}
             onKeyPress={e => e.key === 'Enter' ? handleChat() : null}
             style={{flex: 1, padding: '0.5rem', borderRadius: '4px', background: '#2d3142', border: 'none', color: 'white'}}
             placeholder="Ask a question..."
          />
          <button onClick={handleChat} style={{padding: '0.5rem', background: 'var(--accent-color)', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>&gt;</button>
        </div>
      </div>

    </div>
  );
}

export default App;
