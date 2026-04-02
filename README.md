# AreaHome 🏠

AI-powered rental property search for Hyderabad, India.

## Features
- 🔍 Natural language property search ("2BHK in ECIL under ₹20k, girl-friendly")
- 🗺️ Interactive 3D map with property markers and amenity icons
- 🤖 AI chatbot powered by Gemini
- 📊 Radar charts showing area scores (safety, water, IT proximity, etc.)
- 🌤️ Live weather data per area
- 👩 Smart social context (girl-friendly, bachelor-friendly, family societies)
- 50+ Hyderabad areas covered

## Tech Stack
- **Backend**: FastAPI + Python + Gemini AI + Open-Meteo Weather API + OpenStreetMap
- **Frontend**: React + Vite + Tailwind CSS + Leaflet Maps + Chart.js

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
# Create .env file with:
# GEMINI_API_KEY=your_key_here
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
# Set your MapTiler key in src/pages/HomePage.jsx
npm run dev
```

Open http://localhost:5173
