export default function PropertyListCard({ property, isSelected, onClick, rank }) {
  const { title, area, rent_monthly, bedrooms, bathrooms, sqft, tags, score } = property

  return (
    <div 
      onClick={onClick}
      style={{
        background: isSelected ? 'linear-gradient(135deg, #f5f3ff, #ede9fe)' : 'white',
        border: isSelected ? '2px solid #7c3aed' : '2px solid transparent',
        borderRadius: '14px',
        padding: '14px',
        marginBottom: '10px',
        cursor: 'pointer',
        boxShadow: isSelected ? '0 10px 25px rgba(124, 58, 237, 0.15)' : '0 2px 10px rgba(0,0,0,0.05)',
        transform: isSelected ? 'translateY(-2px)' : 'none',
        transition: 'all 200ms ease'
      }}
    >
      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ color: '#9ca3af', fontSize: '11px', fontWeight: 'bold' }}>#{rank}</span>
        <h4 style={{ margin: 0, fontSize: '14px', fontWeight: 'bold', color: '#1a1a2e', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {title}
        </h4>
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
        <span style={{ color: '#6b7280', fontSize: '13px' }}>{area}</span>
        <span style={{ color: '#1a1a2e', fontSize: '14px', fontWeight: 'bold' }}>₹{rent_monthly.toLocaleString('en-IN')}/mo</span>
      </div>

      <div style={{ color: '#9ca3af', fontSize: '12px', marginBottom: '10px' }}>
        {bedrooms}BHK · {bathrooms}BA · {sqft}sqft
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
        {tags && tags.map((t, i) => {
          let dotColor = '#gray'
          if (t.color === 'green') dotColor = '#16a34a'
          if (t.color === 'blue') dotColor = '#3b82f6'
          if (t.color === 'emerald') dotColor = '#10b981'
          if (t.color === 'purple') dotColor = '#7c3aed'
          if (t.color === 'indigo') dotColor = '#4f46e5'
          if (t.color === 'amber') dotColor = '#d97706'
          if (t.color === 'teal') dotColor = '#0d9488'
          if (t.color === 'pink') dotColor = '#db2777'
          if (t.color === 'violet') dotColor = '#6d28d9'
          
          return (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: '4px',
              background: `rgba(0,0,0,0.04)`, borderRadius: '50px', padding: '2px 8px', fontSize: '11px', color: '#374151'
            }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: dotColor }}></div>
              {t.label}
            </div>
          )
        })}
      </div>

      <div>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '4px' }}>
          <span style={{ fontSize: '10px', color: '#6b7280' }}>Match: {score}%</span>
        </div>
        <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', overflow: 'hidden' }}>
          <div style={{ 
            height: '100%', 
            width: `${score}%`, 
            background: score >= 70 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444' 
          }}></div>
        </div>
      </div>
    </div>
  )
}
