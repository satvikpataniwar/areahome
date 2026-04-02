import { useState, useEffect } from 'react'

export default function LoadingOverlay() {
  const [step, setStep] = useState(0)

  const steps = [
    "Searching properties",
    "Checking water supply data",
    "Analyzing safety scores",
    "Assessing climate & weather",
    "Finding nearby amenities",
    "Comparing valuations",
    "Generating recommendations"
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setStep(s => {
        if (s >= steps.length) {
          clearInterval(interval)
          return s
        }
        return s + 1
      })
    }, 1100)
    return () => clearInterval(interval)
  }, [steps.length])

  return (
    <div style={{
      position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
      background: 'white', borderRadius: '20px', padding: '32px 40px',
      minWidth: '340px', boxShadow: '0 25px 80px rgba(0,0,0,0.18)', zIndex: 1000
    }}>
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <div style={{
          width: '80px', height: '80px', borderRadius: '50%', border: '3px solid transparent',
          background: 'linear-gradient(white, white) padding-box, linear-gradient(to right, #3b82f6, #eab308) border-box',
          margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '40px',
          animation: 'rotate-marker 4s linear infinite'
        }}>
          🧭
        </div>
        <h2 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1a1a2e', margin: '16px 0 0 0' }}>Loading<br />Your Results</h2>
      </div>

      <div style={{
        height: '4px', width: '100%', maxWidth: '200px', background: '#f0f0f0',
        margin: '0 auto 24px auto', borderRadius: '2px', position: 'relative', overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute', top: 0, left: 0, height: '100%',
          background: 'linear-gradient(to right, #3b82f6, #eab308)',
          width: `${Math.min(((step) / steps.length) * 100, 100)}%`,
          transition: 'width 0.5s ease-in-out'
        }}></div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {steps.map((text, i) => {
          const isDone = i < step;
          const isActive = i === step;
          const isWaiting = i > step;
          return (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: '12px',
              opacity: isWaiting ? 0 : 1, transition: 'opacity 0.5s',
              visibility: (isWaiting && i > step + 1) ? 'hidden' : 'visible'
            }}>
              <div style={{
                width: '16px', height: '16px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: isDone ? '#16a34a' : isActive ? 'transparent' : '#e5e7eb',
                border: isActive ? '2px solid #3b82f6' : 'none',
                color: 'white', fontSize: '10px',
                borderTopColor: isActive ? 'transparent' : isDone ? '#16a34a' : '#e5e7eb',
                animation: isActive ? 'rotate-marker 1s linear infinite' : 'none'
              }}>
                {isDone ? '✓' : ''}
              </div>
              <span style={{ fontSize: '13px', color: isDone || isActive ? '#1a1a2e' : '#9ca3af', fontWeight: isActive ? 600 : 400 }}>
                {text}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
