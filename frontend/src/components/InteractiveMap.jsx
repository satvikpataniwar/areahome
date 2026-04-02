import { MapContainer, TileLayer, Marker, Popup, useMap, Circle, Polyline } from 'react-leaflet'
import { useState, useEffect } from 'react'
import L from 'leaflet'
import LoadingOverlay from './LoadingOverlay'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function FlyTo({ position }) {
  const map = useMap()
  useEffect(() => {
    if (position) {
      map.flyTo(position, 16, { duration: 1.5 })
    }
  }, [position, map])
  return null
}

export default function InteractiveMap({ properties, selectedProperty, onPropertySelect, isLoading }) {
  const [userLocation, setUserLocation] = useState(null)
  const [showRoute, setShowRoute] = useState(false)

  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setUserLocation([pos.coords.latitude, pos.coords.longitude]),
        // error handler ignored for simplicity
      )
    }
  }, [])

  const emojiIcons = {
    hospital: '🏥', supermarket: '🛒', park: '🌳', gym: '💪', 
    temple: '🕌', transport: '🚇', it_hub: '💻', mall: '🏬', 
    barber: '✂️', mechanic: '🔧', school: '🏫'
  }

  const getEmojiIcon = (type) => {
    const emoji = emojiIcons[type] || '📍'
    return L.divIcon({
      className: 'custom-div-icon',
      html: `<div style="font-size: 20px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">${emoji}</div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    })
  }

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {isLoading && <LoadingOverlay />}
      <MapContainer center={[17.3850, 78.4867]} zoom={12} style={{ width: '100%', height: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        
        {properties.map(prop => {
          const isSelected = selectedProperty?.id === prop.id
          
          let iconHtml = ''
          if (isSelected) {
            iconHtml = `
              <div style="position:relative;">
                <div style="width:44px; height:44px; border-radius:50%; background:linear-gradient(135deg, #7c3aed, #6d28d9); color:white; display:flex; align-items:center; justify-content:center; font-weight:bold; border:3px solid white; box-shadow:0 4px 10px rgba(0,0,0,0.3); position:relative; z-index:2;">
                  ${prop.bedrooms}B
                </div>
                <div class="marker-selected-ring"></div>
              </div>`
          } else {
            iconHtml = `
              <div style="width:36px; height:36px; border-radius:50%; background:#1d4ed8; color:white; display:flex; align-items:center; justify-content:center; font-weight:bold; border:2px solid white; box-shadow:0 2px 5px rgba(0,0,0,0.3);">
                ${prop.bedrooms}B
              </div>`
          }

          const icon = L.divIcon({
            className: 'custom-div-icon',
            html: iconHtml,
            iconSize: isSelected ? [44, 44] : [36, 36],
            iconAnchor: isSelected ? [22, 44] : [18, 36]
          })

          return (
            <Marker key={prop.id} position={[prop.lat, prop.lng]} icon={icon} eventHandlers={{ click: () => onPropertySelect(prop) }}>
              <Popup>
                <div>
                  <div style={{ fontWeight: 'bold', fontSize: '14px', marginBottom: '2px' }}>{prop.title}</div>
                  <div style={{ color: '#7c3aed', fontSize: '12px', marginBottom: '4px' }}>{prop.area}</div>
                  <div style={{ fontWeight: 'bold', fontSize: '14px', marginBottom: '4px' }}>₹{prop.rent_monthly.toLocaleString('en-IN')}/mo</div>
                  <div style={{ fontSize: '11px', marginBottom: '4px' }}>{prop.bedrooms}BHK · {prop.sqft}sqft</div>
                  <div style={{ background: '#f3f4f6', display: 'inline-block', padding: '2px 6px', borderRadius: '10px', fontSize: '10px' }}>
                    {prop.society_type}
                  </div>
                </div>
              </Popup>
            </Marker>
          )
        })}

        {selectedProperty && selectedProperty.nearby_amenities && selectedProperty.nearby_amenities.map((am, i) => {
          let amColor = '#6b7280'
          if (am.type === 'hospital') amColor = '#dc2626'
          else if (am.type === 'mall') amColor = '#f97316'
          else if (am.type === 'it_hub') amColor = '#8b5cf6'
          else if (am.type === 'park' || am.type === 'supermarket') amColor = '#16a34a'
          else if (am.type === 'transport') amColor = '#0284c7'
          else if (am.type === 'temple' || am.type === 'barber') amColor = '#d97706'
          else if (am.type === 'gym') amColor = '#be185d'
          else if (am.type === 'school') amColor = '#0891b2'

          return (
            <div key={i}>
              <Circle center={[am.lat, am.lng]} radius={80} pathOptions={{ color: amColor, fillColor: amColor, fillOpacity: 0.2 }} />
              <Marker position={[am.lat, am.lng]} icon={getEmojiIcon(am.type)}>
                <Popup>
                  <strong>{am.name}</strong><br/><span style={{ textTransform: 'capitalize' }}>{am.type.replace('_', ' ')}</span>
                </Popup>
              </Marker>
            </div>
          )
        })}

        {userLocation && selectedProperty && showRoute && (
          <Polyline 
            positions={[userLocation, [selectedProperty.lat, selectedProperty.lng]]} 
            pathOptions={{ color: '#7c3aed', weight: 4, dashArray: '10, 10', opacity: 0.8 }} 
          />
        )}

        {selectedProperty && <FlyTo position={[selectedProperty.lat, selectedProperty.lng]} />}
      </MapContainer>

      {userLocation && selectedProperty && (
        <button 
          onClick={() => setShowRoute(!showRoute)}
          style={{
            position: 'absolute', top: '16px', right: '16px', zIndex: 500,
            background: 'white', borderRadius: '8px', padding: '8px 12px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)', border: 'none',
            fontSize: '12px', fontWeight: 'bold', cursor: 'pointer', color: '#1a1a2e'
          }}
        >
          📍 {showRoute ? 'Hide Route' : 'Show Route'}
        </button>
      )}
    </div>
  )
}
