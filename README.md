# AI Bus Travel Assistant

The AI Bus Travel Assistant is a Streamlit application that helps users find VIA Metropolitan Transit bus routes in San Antonio.

Users enter a starting location and destination. The application searches local VIA GTFS schedule data, identifies a direct route or a route requiring one transfer, and uses Gemini to explain the trip in simple language.

## Project Purpose

Public transportation information can be difficult to understand, especially when riders need to identify nearby stops, route numbers, transfers, walking distances, and scheduled travel times.

This project provides a simple interface that combines official VIA schedule data with an AI-generated explanation.

## Current Features

- Streamlit user interface
- Starting-location input
- Destination input
- Input validation
- OpenStreetMap location lookup
- Local VIA GTFS schedule processing
- Nearby VIA stop identification
- Direct-route matching
- One-transfer route matching
- Route number and route name display
- Starting and destination stop information
- Scheduled departure and arrival times
- Estimated trip duration
- Walking-distance estimates
- Fare information
- Gemini-generated route explanations
- Common San Antonio location aliases
- Graceful error handling

## Technology Used

- Python
- Streamlit
- Pandas
- VIA Metropolitan Transit GTFS data
- OpenStreetMap Nominatim
- Gemini API
- Python-dotenv
- Requests

## Project Structure

```text
ai_bus_travel_assistant/
├── backend/
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── maps_service.py
│   │   └── via_service.py
│   ├── requirements.txt
│   ├── test_gemini_connection.py
│   ├── verify_data_ingestion.py
│   └── venv/
├── data/
│   ├── via_gtfs.zip
│   └── via_gtfs/
│       ├── agency.txt
│       ├── calendar.txt
│       ├── calendar_dates.txt
│       ├── feed_info.txt
│       ├── routes.txt
│       ├── shapes.txt
│       ├── stop_times.txt
│       ├── stops.txt
│       ├── transfers.txt
│       └── trips.txt
├── streamlit_ui/
│   └── streamlit_app.py
├── .env
├── .gitignore
└── README.md
```

The `backend/venv` folder and `.env` file should remain excluded from Git.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

Move into the project folder:

```bash
cd ai_bus_travel_assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv backend/venv
```

### 3. Activate the virtual environment

On macOS or Linux:

```bash
source backend/venv/bin/activate
```

On Windows PowerShell:

```powershell
backend\venv\Scripts\Activate.ps1
```

### 4. Install the required packages

```bash
python -m pip install -r backend/requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit the `.env` file or share the API key publicly.

The `.gitignore` file should include:

```text
.env
backend/venv/
__pycache__/
*.pyc
.DS_Store
.streamlit/
```

## Running the Application

From the project root, activate the virtual environment:

```bash
source backend/venv/bin/activate
```

Start the Streamlit application:

```bash
streamlit run streamlit_ui/streamlit_app.py
```

The application should open automatically in a browser.

The default local address is:

```text
http://localhost:8501
```

Only the Streamlit process is required. FastAPI, Uvicorn, React, and Vite are not used in the current version.

## How the Application Works

1. The user enters a starting location and destination.
2. The application checks that both inputs are present and different.
3. OpenStreetMap Nominatim converts each location into coordinates.
4. The application finds nearby VIA stops using latitude and longitude.
5. Local VIA GTFS files are searched for matching scheduled trips.
6. The application first searches for a direct route.
7. If no direct route is found, it searches for a route requiring one transfer.
8. The route details are passed to Gemini.
9. Gemini creates a concise explanation without inventing route information.
10. Streamlit displays the route details and AI explanation.

## VIA GTFS Data Used

The application uses the following GTFS files:

- `stops.txt` for VIA stop names and coordinates
- `routes.txt` for route numbers and route names
- `trips.txt` for individual scheduled trips and destinations
- `stop_times.txt` for stop order, departure times, and arrival times
- `transfers.txt` for available GTFS transfer information
- `calendar.txt` and `calendar_dates.txt` for service schedules

## Successful Test

The application was tested using:

```text
Starting location: The Alamo
Destination: San Antonio International Airport
```

The application successfully returned:

- VIA Route 5
- no transfer required
- nearby boarding and destination stops
- scheduled departure and arrival times
- estimated trip duration
- walking-distance information
- fare information
- an AI-generated explanation

This test confirms that the Streamlit interface, VIA GTFS processing, location lookup, and Gemini logic work together.

## Phase 2 Completion

### Core Logic Completion

The following core logic is implemented:

- VIA GTFS data loading
- location geocoding
- nearby-stop calculation
- direct-route matching
- one-transfer route matching
- route-response formatting
- Gemini prompt generation
- AI response generation
- error handling

### UI Integration

The Streamlit interface allows the user to:

- enter a starting location
- enter a destination
- submit the trip request
- see route information change dynamically
- view route numbers and transfers
- view scheduled travel details
- view AI-generated guidance
- expand detailed route and stop information

## Current Limitations

- The application uses scheduled GTFS data rather than live bus positions.
- Trips are not yet filtered by the current day and time.
- The routing system supports direct routes and routes with one transfer.
- Some trips requiring two or more transfers may not return an itinerary.
- Walking information is shown as estimated distance rather than street-by-street directions.
- OpenStreetMap location lookup requires an internet connection.
- The displayed fare is a prototype value and should be verified against current VIA fare information before production use.

## Future Improvements

Possible future improvements include:

- filter routes by the current date and time
- add GTFS-Realtime vehicle positions
- add live arrival predictions
- add service alerts
- support routes requiring multiple transfers
- improve trip ranking
- add an interactive map
- add accessibility preferences
- add departure-time selection
- cache commonly searched locations
- deploy the Streamlit application online

## Data and API Security

The Gemini API key is stored in `.env`.

The `.env` file must not be committed to GitHub.

Before pushing changes, verify that it is ignored:

```bash
git check-ignore -v .env
```

## Updating the Repository

Check the current changes:

```bash
git status
```

Stage the changes:

```bash
git add README.md backend/requirements.txt
```

Commit them:

```bash
git commit -m "Update Streamlit requirements and project documentation"
```

Push the commit:

```bash
git push
```

## Author

Jose Torres

Texas A&M University-San Antonio
