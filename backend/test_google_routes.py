import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    print("ERROR: GOOGLE_MAPS_API_KEY was not found in the .env file.")
    sys.exit(1)


url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": (
        "routes.duration,"
        "routes.distanceMeters,"
        "routes.legs.steps.travelMode,"
        "routes.legs.steps.transitDetails,"
        "routes.legs.steps.navigationInstruction"
    ),
}

payload = {
    "origin": {
        "address": "Texas A&M University-San Antonio, San Antonio, TX"
    },
    "destination": {
        "address": "The Alamo, San Antonio, TX"
    },
    "travelMode": "TRANSIT",
    "computeAlternativeRoutes": True,
    "transitPreferences": {
        "allowedTravelModes": ["BUS"],
        "routingPreference": "FEWER_TRANSFERS",
    },
    "languageCode": "en-US",
    "units": "IMPERIAL",
}


try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        routes = data.get("routes", [])

        if not routes:
            print("The API request succeeded, but no transit route was found.")
        else:
            print(f"Success! Google returned {len(routes)} route(s).")
            print()
            print("Full response:")
            print(data)

    else:
        print("Google Routes API returned an error:")
        print(response.text)

except requests.exceptions.Timeout:
    print("ERROR: The request timed out.")

except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to the Google Routes API.")

except requests.exceptions.RequestException as error:
    print(f"ERROR: Request failed: {error}")
