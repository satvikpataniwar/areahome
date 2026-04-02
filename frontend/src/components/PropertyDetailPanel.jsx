import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import { Radar } from 'react-chartjs-2'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

export default function PropertyDetailPanel({ property }) {
  if (!property) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'gray' }}>
        Click a property to see details
      </div>
    )
  }

  const { address, rent_monthly, score, bedrooms, bathrooms, sqft, society_type, score_breakdown, match_reason, weather_details } = property

  const data = {
    labels: ["Water Supply", "Safety", "IT Hub", "Schools", "Transport", "Greenness", "Weather"],
    datasets: [
      {
        label: 'Area Score',
        data: score_breakdown ? [
          score_breakdown["Water Supply"],
          score_breakdown["Safety"],
          score_breakdown["IT Hub"],
          score_breakdown["Schools"],
          score_breakdown["Transport"],
          score_breakdown["Greenness"],
          score_breakdown["Weather"]
        ] : [6,6,6,6,6,6,6],
        backgroundColor: 'rgba(124, 58, 237, 0.12)',
        borderColor: '#7c3aed',
        pointBackgroundColor: '#7c3aed',
        pointBorderColor: 'white',
        pointBorderWidth: 2,
      },
    ],
  }

  const options = {
    scales: {
      r: {
        min: 0, max: 10,
        ticks: { display: false },
        grid: { color: 'rgba(124, 58, 237, 0.1)' },
        pointLabels: { font: { size: 11 }, color: '#6b7280' }
      }
    },
    plugins: { legend: { display: false } }
  }

  return (
    <div style={{ padding: '16px', height: '100%', background: 'white' }}>
      <h3 style={{ margin: '0 0 8px 0', fontSize: '15px', color: '#1a1a2e', fontWeight: 'bold' }}>{address}</h3>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#1a1a2e' }}>₹{rent_monthly.toLocaleString('en-IN')}/mo</span>
        <span style={{ 
          background: score >= 70 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444', 
          color: 'white', padding: '4px 10px', borderRadius: '50px', fontSize: '12px', fontWeight: 'bold' 
        }}>
          Score: {(score/10).toFixed(1)}/10
        </span>
      </div>
      <div style={{ color: '#6b7280', fontSize: '13px', marginBottom: '8px' }}>
        {bedrooms}bd / {bathrooms}ba · {sqft} sqft
      </div>
      {society_type && (
        <span style={{ display: 'inline-block', background: '#f3f4f6', color: '#374151', padding: '2px 8px', borderRadius: '10px', fontSize: '11px', textTransform: 'capitalize' }}>
          {society_type === 'family' ? 'Family Society' : society_type === 'bachelor' ? 'Bachelor Friendly' : 'Mixed Society'}
        </span>
      )}

      <hr style={{ border: 'none', borderTop: '1px solid #f0eeff', margin: '20px 0' }} />

      <div style={{ height: '200px', display: 'flex', justifyContent: 'center' }}>
        <Radar data={data} options={options} />
      </div>

      <hr style={{ border: 'none', borderTop: '1px solid #f0eeff', margin: '20px 0' }} />

      <div style={{ marginBottom: '20px' }}>
        <div style={{ fontSize: '11px', fontWeight: 'bold', color: '#9ca3af', marginBottom: '8px' }}>AI ANALYSIS</div>
        <p style={{ margin: 0, fontSize: '13px', color: '#374151', lineHeight: '1.5' }}>{match_reason}</p>
      </div>

      <hr style={{ border: 'none', borderTop: '1px solid #f0eeff', margin: '20px 0' }} />

      <div style={{ marginBottom: '20px' }}>
        <div style={{ fontSize: '11px', fontWeight: 'bold', color: '#9ca3af', marginBottom: '12px' }}>SCORE BREAKDOWN</div>
        {score_breakdown && Object.entries(score_breakdown).map(([label, val]) => (
          <div key={label} style={{ display: 'flex', alignItems: 'center', marginBottom: '8px', gap: '12px' }}>
            <span style={{ fontSize: '13px', color: '#6b7280', flexShrink: 0, width: '90px' }}>{label}</span>
            <div style={{ flex: 1, background: '#f3f4f6', height: '6px', borderRadius: '3px', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${val*10}%`, background: val >= 7 ? '#a78bfa' : '#60a5fa' }}></div>
            </div>
            <span style={{ fontSize: '13px', color: '#1a1a2e', fontWeight: 'bold', flexShrink: 0, width: '30px', textAlign: 'right' }}>{val}</span>
          </div>
        ))}
      </div>

      {weather_details && (
        <>
          <hr style={{ border: 'none', borderTop: '1px solid #f0eeff', margin: '20px 0' }} />
          <div>
            <div style={{ fontSize: '11px', fontWeight: 'bold', color: '#9ca3af', marginBottom: '12px' }}>LIVE WEATHER</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div style={{ background: '#f8f9fa', padding: '10px', borderRadius: '10px', textAlign: 'center' }}>
                <div style={{ fontSize: '18px', marginBottom: '4px' }}>🌡️</div>
                <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#1a1a2e' }}>{weather_details.temperature}</div>
              </div>
              <div style={{ background: '#f8f9fa', padding: '10px', borderRadius: '10px', textAlign: 'center' }}>
                <div style={{ fontSize: '18px', marginBottom: '4px' }}>💧</div>
                <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#1a1a2e' }}>{weather_details.humidity}</div>
              </div>
              <div style={{ background: '#f8f9fa', padding: '10px', borderRadius: '10px', textAlign: 'center' }}>
                <div style={{ fontSize: '18px', marginBottom: '4px' }}>☀️</div>
                <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#1a1a2e' }}>UV {weather_details.uv_index}</div>
              </div>
              <div style={{ background: '#f8f9fa', padding: '10px', borderRadius: '10px', textAlign: 'center' }}>
                <div style={{ fontSize: '18px', marginBottom: '4px' }}>🌧️</div>
                <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#1a1a2e' }}>{weather_details.rainfall}</div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
