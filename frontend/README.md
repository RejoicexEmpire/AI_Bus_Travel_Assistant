# AI Bus Travel Assistant

## Overview

The AI Bus Travel Assistant is a full-stack web application designed to help users plan safer and smarter bus trips in San Antonio. The application combines transit information, mapping services, and Generative AI to provide easy-to-understand travel recommendations.

This project is being developed as part of a Computer Science course focused on strengthening the San Antonio community through technology.

---

## Features

### Current Features

- Search for a starting location and destination
- React frontend with a FastAPI backend
- Display route recommendations
- Component-based frontend architecture
- REST API communication between frontend and backend

### Planned Features

- Real VIA Metropolitan Transit route recommendations
- Google Gemini AI travel assistant
- Interactive route map
- Bus stop locations
- Estimated travel time
- Fare information
- Transfer recommendations
- Accessibility information
- Safety recommendations
- Nearby points of interest

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI

- Google Gemini API *(Coming Soon)*

### APIs

- VIA Transit Data *(Planned)*
- Google Maps API or OpenStreetMap *(Planned)*

---

## Project Structure

```text
AI-Bus-Travel-Assistant
│
├── backend
│   ├── api
│   ├── models
│   ├── services
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   └── services
│   └── package.json
│
├── docs
├── data
├── README.md
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd AI-Bus-Travel-Assistant
```

---

## Backend Setup

Navigate to the backend folder.

```bash
cd backend
```

Create a virtual environment.

```bash
python3 -m venv venv
```

Activate the virtual environment.

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the backend server.

```bash
uvicorn main:app --reload
```

The backend will run at:

```
http://127.0.0.1:8000
```

API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Navigate to the frontend folder.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Run the development server.

```bash
npm run dev
```

The frontend will run at:

```
http://localhost:5173
```

---

## Current Status

### Completed

- Project setup
- Backend architecture
- Frontend architecture
- REST API communication
- Route recommendation prototype

### In Progress

- Gemini AI integration
- Transit data integration
- Interactive maps

### Planned

- User authentication
- Saved trips
- Favorite locations
- Real-time bus tracking
- Mobile responsiveness

---

## Future Improvements

- AI-powered travel explanations
- Live bus arrival times
- Route optimization
- Weather-aware recommendations
- Accessibility routing
- Multi-language support
- Trip history
- Notifications

---

## Authors

- Jose Torres
- Team Members (To Be Added)

---

## License

This project is being developed for educational purposes.