import { useState, useEffect, lazy, Suspense } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios'
import PropertyListCard from '../components/PropertyListCard'
import PropertyDetailPanel from '../components/PropertyDetailPanel'
import ChatBot from '../components/ChatBot'
import LoadingOverlay from '../components/LoadingOverlay'

const InteractiveMap = lazy(() => import('../components/InteractiveMap'))

export default function ResultsPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const query = location.state?.query || ''

  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedProperty, setSelectedProperty] = useState(null)

  useEffect(() => {
    if (!query) {
      navigate('/')
      return
    }

    setLoading(true)
    axios.post('http://localhost:8000/api/search', { query })
      .then(res => {
        setResults(res.data.results)
        if (res.data.results.length > 0) {
          setSelectedProperty(res.data.results[0])
        }
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false))
  }, [query, navigate])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      <div style={{ height: '56px', background: 'white', borderBottom: '1px solid #f0eeff', display: 'flex', alignItems: 'center', padding: '0 20px', gap: '12px' }}>
        <div style={{ fontWeight: 'bold', color: '#1a1a2e', fontSize: '18px', cursor: 'pointer' }} onClick={() => navigate('/')}>AreaHome</div>
        <div style={{ width: '1px', background: '#eee', height: '20px' }}></div>
        <div style={{ background: '#f5f3ff', color: '#7c3aed', borderRadius: '20px', padding: '4px 14px', fontSize: '13px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '300px' }}>
          {query}
        </div>
        <div style={{ marginLeft: 'auto', color: 'gray', fontSize: '13px' }}>
          {results.length} homes found
        </div>
        <button onClick={() => navigate('/')} style={{ border: '1px solid #ddd', borderRadius: '50px', padding: '6px 16px', background: 'white', cursor: 'pointer' }}>New Search</button>
      </div>
      
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        <div style={{ width: '300px', overflowY: 'auto', background: '#fafafa', borderRight: '1px solid #f0eeff', padding: '12px' }}>
          <h3 style={{ margin: '0 0 12px 0', fontSize: '14px', color: '#333' }}>Matching Properties <span style={{ background: '#7c3aed', color: 'white', padding: '2px 8px', borderRadius: '12px', fontSize: '11px', marginLeft: '6px' }}>{results.length}</span></h3>
          
          {loading ? (
            Array(5).fill(0).map((_, i) => (
              <div key={i} style={{ background: 'white', borderRadius: '14px', padding: '14px', marginBottom: '10px', height: '120px', animation: 'pulse 1.5s infinite' }}></div>
            ))
          ) : results.length > 0 ? (
            results.map((prop, i) => (
              <PropertyListCard 
                key={prop.id} 
                property={prop} 
                rank={i + 1}
                isSelected={selectedProperty?.id === prop.id} 
                onClick={() => setSelectedProperty(prop)} 
              />
            ))
          ) : (
            <div style={{ padding: '20px', textAlign: 'center', color: 'gray' }}>No properties found</div>
          )}
        </div>
        
        <div style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
            <Suspense fallback={null}>
              <InteractiveMap 
                properties={results} 
                selectedProperty={selectedProperty} 
                onPropertySelect={setSelectedProperty} 
                isLoading={loading}
              />
            </Suspense>
        </div>
        
        <div style={{ width: '320px', overflowY: 'auto', background: 'white', borderLeft: '1px solid #f0eeff' }}>
          <PropertyDetailPanel property={selectedProperty} />
        </div>
      </div>
      <ChatBot searchContext={query} />
    </div>
  )
}
