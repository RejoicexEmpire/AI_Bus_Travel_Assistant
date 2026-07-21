# AI Bus Travel Assistant

An AI-powered Streamlit application that helps users navigate the VIA Metropolitan Transit bus system in San Antonio, Texas.

The application combines official VIA GTFS transit schedule data with Google's Gemini AI to provide easy-to-understand bus route recommendations. Instead of requiring riders to interpret GTFS data themselves, the application computes the route using official transit schedules and uses AI to explain the trip in natural language.

---

# Application Overview

The AI Bus Travel Assistant allows users to:

- Enter a starting location
- Enter a destination
- Find available VIA bus routes
- View route numbers and stop information
- See estimated travel times
- View transfer information
- Receive an AI-generated explanation of the trip

The application is designed to make public transportation easier to understand for new riders, students, visitors, and residents of San Antonio.

---

# Features

### Route Planning

- Route search using official VIA GTFS data
- Nearby stop identification
- Direct route matching
- One-transfer route matching
- Walking distance estimation
- Scheduled departure and arrival times
- Estimated trip duration
- Fare display

### Artificial Intelligence

Google Gemini is used to convert structured transit information into clear, natural-language directions.

The AI **does not generate routes**. Instead, all routing is calculated using official VIA GTFS transit data, and Gemini explains the verified results in a user-friendly format.

### User Experience

- Streamlit web interface
- Input validation
- Friendly error messages
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
│   │   ├── maps_service.py
│   │   └── via_service.py
│   ├── test_gemini_connection.py
│   └── verify_data_ingestion.py
│
├── streamlit_ui/
│   └── streamlit_app.py
│
├── data/
│
├── docs/
│
├── requirements.txt
├── README.md
└── .gitignore
```

A local `.env` file and Python virtual environment are required but are intentionally excluded from the GitHub repository.

---

# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/RejoicexEmpire/AI_Bus_Travel_Assistant.git
```

Move into the project directory:

```bash
cd AI_Bus_Travel_Assistant
```

---

## 2. Create a virtual environment

macOS / Linux

```bash
python3 -m venv backend/venv
```

Windows

```powershell
python -m venv backend\venv
```

---

## 3. Activate the virtual environment

macOS / Linux

```bash
source backend/venv/bin/activate
```

Windows

```powershell
backend\venv\Scripts\Activate.ps1
```

---

## 4. Install the required packages

```bash
pip install -r requirements.txt
```

---

## 5. Configure the Gemini API Key

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

The application will open in your browser at:

```text
http://localhost:8501
```

---

# How the Application Works

1. The user enters a starting location and destination.
2. The application validates the inputs.
3. OpenStreetMap converts the locations into geographic coordinates.
4. Nearby VIA bus stops are identified.
5. Official GTFS schedule data is searched.
6. The application looks for:
   - Direct routes
   - Routes requiring one transfer
7. Route information is formatted.
8. Gemini generates an easy-to-read explanation.
9. Streamlit displays the complete trip information.

---

# AI Integration

The application separates routing logic from AI generation.

### Route Computation

Routes are computed using:

- VIA GTFS stop data
- Route data
- Trip schedules
- Stop times
- Transfer information

### AI Explanation

Google Gemini receives the verified routing information and produces a concise explanation for the user.

This design minimizes hallucinations because the AI explains existing routes rather than creating them.

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

# Example Test

The application was successfully tested using:

**Starting Location**

```
The Alamo
```

**Destination**

```
San Antonio International Airport
```

The application successfully returned:

- VIA Route 5
- Boarding stop
- Destination stop
- Departure time
- Arrival time
- Estimated travel duration
- Walking distance
- Fare information
- AI-generated trip explanation

---

# Current Limitations

- Uses scheduled GTFS data instead of live vehicle locations
- Supports direct routes and routes with one transfer
- Trips requiring multiple transfers may not be returned
- Walking directions are estimated rather than turn-by-turn
- OpenStreetMap requires an internet connection
- Fare information is a prototype value and should be verified with VIA

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
- Route ranking improvements
- Cloud deployment

---

# Security

Sensitive information is stored in a local `.env` file.

The repository excludes:

- API keys
- Virtual environments
- Python cache files
- GTFS datasets

using `.gitignore`.

---

# Author

**Jose Torres**

Texas A&M University–San Antonio

Bachelor of Arts and Science in Computer Science

---

# License

This project was developed as part of a university AI course at Texas A&M University–San Antonio.
