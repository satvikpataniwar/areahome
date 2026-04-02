import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

export default function ChatBot({ searchContext }) {
  const [isOpen, setIsOpen] = useState(false)
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'ai', text: "Hi! I'm your AreaHome assistant. Ask me anything about Hyderabad neighborhoods, rental prices, or finding the right area for you!" }
  ])
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    if (isOpen) scrollToBottom()
  }, [messages, isOpen])

  const handleSend = async () => {
    if (!inputText.trim()) return

    const userMsg = { role: 'user', text: inputText }
    setMessages(prev => [...prev, userMsg])
    setInputText('')
    setIsLoading(true)

    try {
      const res = await axios.post('http://localhost:8000/api/chat', {
        message: inputText,
        context: searchContext
      })
      
      setMessages(prev => [...prev, { role: 'ai', text: res.data.reply }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: "Sorry, I'm having trouble connecting right now. Please try again!" }])
    } finally {
      setIsLoading(false)
    }
  }

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed', bottom: '24px', right: '24px', zIndex: 1000,
          width: '56px', height: '56px', borderRadius: '50%',
          background: 'linear-gradient(135deg, #7c3aed, #6d28d9)', color: 'white',
          border: 'none', cursor: 'pointer', boxShadow: '0 8px 25px rgba(124,58,237,0.4)',
          fontSize: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}
      >
        💬
      </button>
    )
  }

  return (
    <div style={{
      position: 'fixed', bottom: '90px', right: '24px', zIndex: 1000,
      width: '340px', height: '440px', background: 'white', borderRadius: '20px',
      boxShadow: '0 20px 60px rgba(0,0,0,0.2)', border: '1px solid #e8e4ff',
      display: 'flex', flexDirection: 'column', overflow: 'hidden'
    }}>
      <div style={{
        background: 'linear-gradient(135deg, #7c3aed, #6d28d9)', padding: '16px 20px',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center'
      }}>
        <div>
          <div style={{ color: 'white', fontWeight: 'bold', fontSize: '15px' }}>AreaHome AI</div>
          <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: '12px' }}>Hyderabad property expert</div>
        </div>
        <button onClick={() => setIsOpen(false)} style={{ background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '16px' }}>✕</button>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {messages.map((msg, i) => (
          <div key={i} className={msg.role === 'ai' ? 'chat-bubble-ai' : 'chat-bubble-user'}>
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="chat-bubble-ai" style={{ width: '50px', textAlign: 'center' }}>
            <span style={{ animation: 'pulse-ring 1s infinite' }}>...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ padding: '12px', borderTop: '1px solid #f0eeff', display: 'flex', gap: '8px' }}>
        <input 
          type="text" 
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask about areas..."
          style={{
            flex: 1, border: '1.5px solid #e5e7eb', borderRadius: '12px', padding: '10px 14px',
            fontSize: '14px', outline: 'none'
          }}
          onFocus={e => e.target.style.borderColor = '#7c3aed'}
          onBlur={e => e.target.style.borderColor = '#e5e7eb'}
        />
        <button 
          onClick={handleSend}
          style={{ background: '#7c3aed', color: 'white', border: 'none', borderRadius: '10px', padding: '10px 14px', cursor: 'pointer', fontWeight: 'bold' }}
        >
          →
        </button>
      </div>
    </div>
  )
}
