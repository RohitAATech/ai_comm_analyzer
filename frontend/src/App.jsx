import { useState } from 'react'
import axios from 'axios'
import './index.css'
 
const API = 'http://localhost:8000'
 
// Color maps for badges
const urgencyColors = { critical:'#dc2626', high:'#ea580c', medium:'#d97706', low:'#16a34a' }
const sentimentColors = { very_negative:'#991b1b', negative:'#dc2626', neutral:'#6b7280', positive:'#16a34a' }
const riskColors = { high:'#dc2626', medium:'#d97706', low:'#2563eb', none:'#16a34a' }
const channelIcons = { whatsapp:'💬', email:'📧', sms:'📱', phone_call:'📞' }
 
function Badge({ label, color }) {
  return (
    <span style={{
      background: color + '20', color, border: `1px solid ${color}`,
      borderRadius: '4px', padding: '2px 10px', fontSize: '12px', fontWeight: 700
    }}>
      {label.replace(/_/g, ' ').toUpperCase()}
    </span>
  )
}
 
export default function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
 
  const samples = [
    'My credit card was charged twice for Rs 4500. Please refund immediately!',
    'I have not received my bank statement for 3 months. Please send it.',
    'Suspicious transaction of Rs 89000 on my account I did not authorize.',
    'I want to update my registered mobile number. Current: 9876543210.',
  ]
 
  async function analyze() {
    if (!text.trim()) return
    setLoading(true); setError(null); setResult(null)
    try {
      const res = await axios.post(`${API}/analyze`, { communication: text })
      setResult(res.data.analysis)
    } catch (e) {
      setError('Error: ' + (e.response?.data?.detail || e.message))
    } finally { setLoading(false) }
  }
 
  return (
    <div style={{ maxWidth:900, margin:'0 auto', padding:24, fontFamily:'Arial, sans-serif' }}>
      {/* Header */}
      <div style={{ background:'#1F3864', color:'white', padding:24, borderRadius:8, marginBottom:24 }}>
        <h1 style={{ margin:0, fontSize:22 }}>🤖 AI-Powered CCM Analyzer</h1>
        <p style={{ margin:'8px 0 0', color:'#93C5FD', fontSize:13 }}>
          GenAI POC — LLaMA 3 + LangChain + ChromaDB (RAG) • Rohit Tiwari
        </p>
      </div>
 
      {/* Sample buttons */}
      <div style={{ marginBottom:12 }}>
        <p style={{ fontSize:13, color:'#666', margin:'0 0 8px' }}>Quick sample communications:</p>
        <div style={{ display:'flex', flexWrap:'wrap', gap:8 }}>
          {samples.map((s, i) => (
            <button key={i} onClick={() => setText(s)}
              style={{ fontSize:12, padding:'6px 12px', cursor:'pointer', background:'#EFF6FF',
                       border:'1px solid #93C5FD', borderRadius:4, color:'#1e40af' }}>
              Sample {i+1}
            </button>
          ))}
        </div>
      </div>
 
      {/* Input */}
      <textarea value={text} onChange={e => setText(e.target.value)}
        placeholder='Paste or type a customer communication here...'
        rows={5} style={{ width:'100%', fontSize:14, padding:12, borderRadius:6,
          border:'2px solid #93C5FD', boxSizing:'border-box', resize:'vertical' }} />
 
      <button onClick={analyze} disabled={loading || !text.trim()}
        style={{ marginTop:12, width:'100%', padding:14, fontSize:16, fontWeight:700,
          background: loading ? '#94a3b8' : '#1F3864', color:'white', border:'none',
          borderRadius:6, cursor: loading ? 'not-allowed' : 'pointer' }}>
        {loading ? '⏳ Analyzing with LLaMA 3...' : '🔍 Analyze Communication'}
      </button>
 
      {error && <div style={{ marginTop:16, padding:12, background:'#FEE2E2',
        color:'#991B1B', borderRadius:6 }}>{error}</div>}
 
      {/* Results */}
      {result && (
        <div style={{ marginTop:24 }}>
          <h2 style={{ color:'#1F3864', borderBottom:'3px solid #2E75B6', paddingBottom:8 }}>
            Analysis Results
          </h2>
          {/* Badges row */}
          <div style={{ display:'flex', gap:12, flexWrap:'wrap', marginBottom:20 }}>
            <Badge label={result.classification} color='#2563eb' />
            <Badge label={`Urgency: ${result.urgency}`} color={urgencyColors[result.urgency]} />
            <Badge label={`Sentiment: ${result.sentiment}`} color={sentimentColors[result.sentiment]} />
            <Badge label={`Risk: ${result.compliance_risk}`} color={riskColors[result.compliance_risk]} />
            <Badge label={`Confidence: ${Math.round(result.confidence_score * 100)}%`} color='#7c3aed' />
          </div>
          {/* Cards */}
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
            <div style={{ background:'#F0FDF4', border:'1px solid #86EFAC', borderRadius:8, padding:16 }}>
              <h3 style={{ margin:'0 0 8px', color:'#166534', fontSize:14 }}>
                {channelIcons[result.channel_recommendation]} Recommended Channel
              </h3>
              <p style={{ margin:0, fontWeight:700, textTransform:'uppercase', color:'#166534' }}>
                {result.channel_recommendation.replace('_', ' ')}
              </p>
              <p style={{ margin:'6px 0 0', fontSize:13, color:'#4B5563' }}>{result.channel_reason}</p>
            </div>
            {result.compliance_risk !== 'none' && (
              <div style={{ background:'#FFF7ED', border:'1px solid #FCA5A5', borderRadius:8, padding:16 }}>
                <h3 style={{ margin:'0 0 8px', color:'#9A3412', fontSize:14 }}>⚠️ Compliance Risk</h3>
                <Badge label={result.compliance_risk} color={riskColors[result.compliance_risk]} />
                <p style={{ margin:'6px 0 0', fontSize:13, color:'#4B5563' }}>{result.risk_reason}</p>
              </div>
            )}
          </div>
          {/* Draft response */}
          <div style={{ marginTop:16, background:'#F8FAFC', border:'1px solid #CBD5E1',
            borderRadius:8, padding:16 }}>
            <h3 style={{ margin:'0 0 8px', color:'#1F3864', fontSize:14 }}>📝 AI-Generated Draft Response</h3>
            <p style={{ margin:0, lineHeight:1.7, color:'#374151', fontSize:14 }}>{result.draft_response}</p>
          </div>
        </div>
      )}
    </div>
  )
}
