import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Map from 'react-map-gl/maplibre'
import 'maplibre-gl/dist/maplibre-gl.css'

const MAPTILER_KEY = 'TWAYFYtw6Xxb0TPZm5B4'

export default function HomePage() {
  const [query, setQuery] = useState('')
  const [focused, setFocused] = useState(false)
  const navigate = useNavigate()

  const handleSearch = () => {
    if (query) navigate('/results', { state: { query } })
  }

  const handleChipClick = (chipQuery) => {
    setQuery(chipQuery)
    navigate('/results', { state: { query: chipQuery } })
  }

  return (
    <>
      <Map
        initialViewState={{ longitude: 78.4867, latitude: 17.3850, zoom: 13, pitch: 50, bearing: -10 }}
        style={{ width: '100vw', height: '100vh', position: 'fixed', top: 0, left: 0 }}
        mapStyle={`https://api.maptiler.com/maps/dataviz-light/style.json?key=${MAPTILER_KEY}`}
      />
      <div style={{
        position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
        background: 'rgba(255, 255, 255, 0.88)', backdropFilter: 'blur(24px)',
        borderRadius: '28px', padding: '40px 44px 36px', width: 'min(560px, 90vw)',
        border: '1px solid rgba(255,255,255,0.9)',
        boxShadow: '0 32px 80px rgba(0,0,0,0.14), 0 0 0 1px rgba(255,255,255,0.5)'
      }}>
        <h1 style={{ fontSize: '42px', fontWeight: 800, color: '#1a1a2e', letterSpacing: '-1.5px', textAlign: 'center', marginBottom: '6px' }}>AreaHome</h1>
        <p style={{ fontSize: '15px', color: '#6b7280', textAlign: 'center', marginBottom: '28px' }}>Find your perfect home in Hyderabad</p>
        
        <div style={{
          background: '#f8f7ff', borderRadius: '16px', padding: '4px 4px 4px 18px',
          display: 'flex', alignItems: 'center', border: `2px solid ${focused ? '#7c3aed' : '#e5e7eb'}`, transition: 'border 200ms'
        }}>
          <input
            autoFocus
            type="text"
            placeholder="e.g. 2BHK in ECIL under ₹20k, girl-friendly safe area..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            style={{ flex: 1, border: 'none', background: 'transparent', outline: 'none', fontSize: '16px', color: '#1a1a2e' }}
          />
          <button 
            onClick={handleSearch}
            style={{
              background: 'linear-gradient(135deg, #7c3aed, #6d28d9)', color: 'white', border: 'none',
              borderRadius: '12px', padding: '12px 20px', cursor: 'pointer', fontSize: '14px', fontWeight: 600,
              margin: '4px', whiteSpace: 'nowrap'
            }}
          >
            Search →
          </button>
        </div>

        <div style={{ marginTop: '20px', display: 'flex', flexWrap: 'wrap', gap: '8px', justifyContent: 'center' }}>
          {["👩 2BHK ECIL under ₹20k, girl-friendly", "💼 3BHK Gachibowli under ₹30k, bachelors ok", "🏠 Family home Kompally under ₹18k"].map(chip => (
            <button key={chip} onClick={() => handleChipClick(chip.substring(2))} style={{
              background: 'white', border: '1.5px solid #e5e7eb', borderRadius: '50px', padding: '8px 16px',
              fontSize: '13px', cursor: 'pointer', color: '#374151', transition: 'all 0.2s'
            }}
            onMouseOver={(e) => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.color = '#7c3aed'; }}
            onMouseOut={(e) => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.color = '#374151'; }}
            >
              {chip}
            </button>
          ))}
        </div>
      </div>
    </>
  )
}
