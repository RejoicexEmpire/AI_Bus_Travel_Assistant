# AI Bus Travel Assistant

An AI-powered Streamlit application that helps users navigate the VIA Metropolitan Transit bus system in San Antonio, Texas.

The application combines official VIA GTFS transit schedule data with Google's Gemini AI to provide easy-to-understand bus route recommendations. Instead of requiring riders to interpret GTFS data themselves, the application computes routes using official transit schedules and uses AI to explain the results in natural language.

---

# Application Overview

The AI Bus Travel Assistant allows users to:

- Enter a starting location
- Enter a destination
- Find available VIA bus routes
- View route numbers and stop information
- View scheduled departure and arrival times
- View estimated travel duration
- View transfer information
- Receive an AI-generated explanation of the trip

The application is designed to make public transportation easier to understand for new riders, students, visitors, and residents of San Antonio.

---

# System Architecture

```
                +----------------------+
                |      User Input      |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Streamlit Interface  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | VIA Routing Engine   |
                | (via_service.py)     |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
+---------------------+          +----------------------+
| GTFS Schedule Data  |          | OpenStreetMap API    |
| (Routes & Stops)    |          | (Geocoding)          |
+---------------------+          +----------------------+
                           |
                           v
                +----------------------+
                | Structured Route     |
                | Information          |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Gemini AI            |
                | (Explanation Only)   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Route Recommendation |
                +----------------------+
```

The routing engine performs all route calculations using GTFS schedule data. Gemini AI does **not** generate routes—it simply explains the verified results in natural language.

---

# Features

## Route Planning

- Route search using official VIA GTFS data
- Nearby stop identification
- Direct route matching
- One-transfer route matching
- Walking distance estimation
- Scheduled departure and arrival times
- Estimated travel duration
- Fare display

## Artificial Intelligence

Google Gemini converts structured transit information into clear, natural-language directions.

The AI **does not create routes**. Instead, all routing is computed using official VIA GTFS data, and Gemini explains the verified results.

## User Experience

- Streamlit web interface
- Input validation
- Friendly error handling
- Common San Antonio location aliases
- Expandable trip details

---

# Technologies Used

- Python
- Streamlit
- Pandas
- Google Gemini API
- OpenStreetMap Nominatim API
- VIA Metropolitan Transit GTFS Data
- Requests
- python-dotenv
- Git
- GitHub

---

# Project Structure

```text
ai_bus_travel_assistant/

├── backend/
│   ├── services/
│   │   ├── gemini_service.py
│   │   └── via_service.py
│   ├── test_gemini_connection.py
│   └── verify_data_ingestion.py
│
├── streamlit_ui/
│   └── streamlit_app.py
│
├── data/
├── docs/
│
├── requirements.txt
├── README.md
└── .gitignore
```

A local `.env` file and Python virtual environment are required but are intentionally excluded from the repository.

---

# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/RejoicexEmpire/AI_Bus_Travel_Assistant.git
```

Move into the project directory.

```bash
cd AI_Bus_Travel_Assistant
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv backend/venv
```

### Windows

```powershell
python -m venv backend\venv
```

---

## 3. Activate the virtual environment

### macOS / Linux

```bash
source backend/venv/bin/activate
```

### Windows

```powershell
backend\venv\Scripts\Activate.ps1
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure Gemini

Create a file named:

```text
.env
```

Add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

---

## 6. Run the application

```bash
streamlit run streamlit_ui/streamlit_app.py
```

The application will open at:

```
http://localhost:8501
```

---

# How the Application Works

1. The user enters a starting location and destination.
2. Inputs are validated.
3. OpenStreetMap converts addresses into coordinates.
4. Nearby VIA bus stops are identified.
5. GTFS schedule data is searched.
6. The application searches for:
   - Direct routes
   - Routes requiring one transfer
7. Route information is assembled.
8. Gemini generates a plain-language explanation.
9. Streamlit displays the complete trip recommendation.

---

# AI Integration

The application separates route computation from AI.

## Route Computation

Routes are calculated using:

- VIA GTFS stops
- Routes
- Trips
- Stop times
- Transfer information

## AI Explanation

Gemini receives verified routing information and converts it into an easy-to-understand explanation.

This architecture minimizes hallucinations because the AI explains existing route data instead of generating new transit information.

---

# GTFS Data Used

The application uses the following GTFS files:

- stops.txt
- routes.txt
- trips.txt
- stop_times.txt
- transfers.txt
- calendar.txt
- calendar_dates.txt

These files are provided by VIA Metropolitan Transit.

---

# Data Sources

The application uses publicly available transit and mapping resources:

- VIA Metropolitan Transit GTFS Schedule Data
- OpenStreetMap Nominatim API
- Google Gemini API

---

# Example Test

The application was successfully tested using:

### Starting Location

```
The Alamo
```

### Destination

```
San Antonio International Airport
```

The application successfully generated:

- VIA Route 5
- Scheduled departure time
- Scheduled arrival time
- Estimated travel duration
- Boarding stop
- Destination stop
- Walking distance estimates
- Fare estimate
- AI-generated explanation based on GTFS data

---

# Screenshots

## Home Screen

*(Insert Screenshot Here)*

---

## Route Recommendation

*(Insert Screenshot Here)*

---

## AI Explanation

*(Insert Screenshot Here)*

---

# Disclaimer

This application is an educational prototype developed as part of a university AI course.

Trip recommendations are based on downloaded GTFS schedule data and should not be interpreted as real-time transit information.

---

# Current Limitations

- Uses scheduled GTFS data instead of live vehicle locations
- Supports direct routes and routes with one transfer
- Trips requiring multiple transfers may not be returned
- Walking directions are estimated rather than turn-by-turn navigation
- OpenStreetMap geocoding requires an internet connection
- Fare information is a prototype value and should be verified with VIA Metropolitan Transit

---

# Future Improvements

Possible future enhancements include:

- GTFS-Realtime integration
- Live vehicle tracking
- Live arrival predictions
- Service alerts
- Multiple-transfer routing
- Interactive maps
- Accessibility preferences
- Departure time selection
- Improved route ranking
- Cloud deployment

---

# Security

Sensitive information, including API keys, is stored locally in a `.env` file and is never committed to the repository.

The repository excludes:

- API keys
- Python virtual environments
- Python cache files
- Local GTFS datasets

through the project's `.gitignore` configuration.

---

# Author

**Jose Torres**

Texas A&M University–San Antonio

Bachelor of Arts and Science in Computer Science

---

# License

This project was developed as part of a university Artificial Intelligence course at Texas A&M University–San Antonio.

It is intended for educational purposes.