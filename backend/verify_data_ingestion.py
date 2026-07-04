from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
GTFS_DIRECTORY = PROJECT_ROOT / "data" / "via_gtfs"


def main():
    routes = pd.read_csv(GTFS_DIRECTORY / "routes.txt")
    stops = pd.read_csv(GTFS_DIRECTORY / "stops.txt")
    trips = pd.read_csv(GTFS_DIRECTORY / "trips.txt")

    print("VIA GTFS data ingestion successful.")
    print(f"Routes: {len(routes)}")
    print(f"Stops: {len(stops)}")
    print(f"Trips: {len(trips)}")

    print("\nSample routes:")
    print(routes.head())


if __name__ == "__main__":
    main()
