from functools import lru_cache
from math import asin, cos, radians, sin, sqrt
from pathlib import Path

import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GTFS_FOLDER = PROJECT_ROOT / "data" / "via_gtfs"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

GEOCODING_HEADERS = {
    "User-Agent": "AI-Bus-Travel-Assistant/1.0"
}


LOCATION_ALIASES = {
    "utsa": (
        "University of Texas at San Antonio, "
        "1 UTSA Circle, San Antonio, Texas"
    ),
    "utsa main campus": (
        "University of Texas at San Antonio, "
        "1 UTSA Circle, San Antonio, Texas"
    ),
    "university of texas at san antonio": (
        "University of Texas at San Antonio, "
        "1 UTSA Circle, San Antonio, Texas"
    ),
    "tamusa": (
        "Texas A&M University-San Antonio, "
        "One University Way, San Antonio, Texas"
    ),
    "texas a&m san antonio": (
        "Texas A&M University-San Antonio, "
        "One University Way, San Antonio, Texas"
    ),
    "texas a&m university san antonio": (
        "Texas A&M University-San Antonio, "
        "One University Way, San Antonio, Texas"
    ),
    "the alamo": (
        "The Alamo, 300 Alamo Plaza, "
        "San Antonio, Texas"
    ),
    "san antonio zoo": (
        "San Antonio Zoo, "
        "3903 North Saint Mary's Street, "
        "San Antonio, Texas"
    ),
    "san antonio airport": (
        "San Antonio International Airport, "
        "9800 Airport Boulevard, "
        "San Antonio, Texas"
    ),
    "san antonio international airport": (
        "San Antonio International Airport, "
        "9800 Airport Boulevard, "
        "San Antonio, Texas"
    ),
    "downtown san antonio": (
        "Downtown San Antonio, Texas"
    ),
    "centro plaza": (
        "Centro Plaza, San Antonio, Texas"
    ),
}


def haversine_distance(
    latitude_one: float,
    longitude_one: float,
    latitude_two: float,
    longitude_two: float,
) -> float:
    """
    Calculate the distance between two coordinates in miles.
    """

    earth_radius_miles = 3958.8

    latitude_one = radians(latitude_one)
    longitude_one = radians(longitude_one)
    latitude_two = radians(latitude_two)
    longitude_two = radians(longitude_two)

    latitude_difference = latitude_two - latitude_one
    longitude_difference = longitude_two - longitude_one

    value = (
        sin(latitude_difference / 2) ** 2
        + cos(latitude_one)
        * cos(latitude_two)
        * sin(longitude_difference / 2) ** 2
    )

    central_angle = 2 * asin(sqrt(value))

    return earth_radius_miles * central_angle


def gtfs_time_to_seconds(gtfs_time: str) -> int:
    """
    Convert a GTFS time such as 25:10:00 into total seconds.

    GTFS allows hour values greater than 23.
    """

    clean_time = str(gtfs_time).strip()

    hours, minutes, seconds = clean_time.split(":")

    return (
        int(hours) * 3600
        + int(minutes) * 60
        + int(seconds)
    )


def format_duration(total_seconds: int) -> str:
    """
    Convert seconds into a readable duration.
    """

    total_minutes = max(1, round(total_seconds / 60))

    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours and minutes:
        return f"{hours} hr {minutes} min"

    if hours:
        return f"{hours} hr"

    return f"{minutes} min"


def create_error_route(
    route_message: str,
    instructions: str,
    details: str,
    start_location: str | None = None,
    destination_location: str | None = None,
) -> dict:
    """
    Return a consistent route-error response.
    """

    return {
        "route": route_message,
        "route_number": None,
        "route_name": None,
        "duration": "Unavailable",
        "estimated_time": "Unavailable",
        "transfers": None,
        "transfer": "Unavailable",
        "fare": "$1.30",
        "departure_time": None,
        "arrival_time": None,
        "instructions": instructions,
        "details": details,
        "start_location": start_location,
        "destination_location": destination_location,
        "data_source": "VIA Metropolitan Transit GTFS",
    }


@lru_cache(maxsize=1)
def load_gtfs_data():
    """
    Load VIA GTFS files once and cache them for later requests.
    """

    required_files = [
        "stops.txt",
        "stop_times.txt",
        "trips.txt",
        "routes.txt",
    ]

    for filename in required_files:
        file_path = GTFS_FOLDER / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required GTFS file was not found: {file_path}"
            )

    stops = pd.read_csv(
        GTFS_FOLDER / "stops.txt",
        dtype={
            "stop_id": str,
            "stop_code": str,
        },
    )

    stop_times = pd.read_csv(
        GTFS_FOLDER / "stop_times.txt",
        dtype={
            "trip_id": str,
            "stop_id": str,
            "arrival_time": str,
            "departure_time": str,
        },
        skipinitialspace=True,
    )

    trips = pd.read_csv(
        GTFS_FOLDER / "trips.txt",
        dtype={
            "trip_id": str,
            "route_id": str,
            "service_id": str,
        },
    )

    routes = pd.read_csv(
        GTFS_FOLDER / "routes.txt",
        dtype={
            "route_id": str,
            "route_short_name": str,
            "route_long_name": str,
        },
    )

    stops["stop_lat"] = pd.to_numeric(
        stops["stop_lat"],
        errors="coerce",
    )

    stops["stop_lon"] = pd.to_numeric(
        stops["stop_lon"],
        errors="coerce",
    )

    stop_times["stop_sequence"] = pd.to_numeric(
        stop_times["stop_sequence"],
        errors="coerce",
    )

    stops = stops.dropna(
        subset=[
            "stop_id",
            "stop_name",
            "stop_lat",
            "stop_lon",
        ]
    )

    stop_times = stop_times.dropna(
        subset=[
            "trip_id",
            "stop_id",
            "stop_sequence",
        ]
    )

    trips = trips.dropna(
        subset=[
            "trip_id",
            "route_id",
        ]
    )

    routes = routes.dropna(
        subset=[
            "route_id",
            "route_short_name",
        ]
    )

    return stops, stop_times, trips, routes


@lru_cache(maxsize=100)
def geocode_location(location: str) -> dict:
    """
    Convert a location name or address into coordinates using
    OpenStreetMap Nominatim.
    """

    cleaned_location = location.strip()

    if not cleaned_location:
        raise ValueError("Location cannot be empty.")

    normalized_location = cleaned_location.lower()

    search_text = LOCATION_ALIASES.get(
        normalized_location,
        cleaned_location,
    )

    if (
        normalized_location not in LOCATION_ALIASES
        and "san antonio" not in normalized_location
    ):
        search_text = (
            f"{cleaned_location}, San Antonio, Texas"
        )

    response = requests.get(
        NOMINATIM_URL,
        params={
            "q": search_text,
            "format": "jsonv2",
            "limit": 1,
            "countrycodes": "us",
        },
        headers=GEOCODING_HEADERS,
        timeout=15,
    )

    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(
            f"Could not locate '{location}'. "
            "Try entering a full San Antonio address or landmark."
        )

    result = results[0]

    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "display_name": result.get(
            "display_name",
            cleaned_location,
        ),
    }


def find_nearest_stops(
    latitude: float,
    longitude: float,
    maximum_results: int = 10,
) -> pd.DataFrame:
    """
    Return the closest VIA stops to a coordinate.
    """

    stops, _, _, _ = load_gtfs_data()

    nearby_stops = stops.copy()

    nearby_stops["distance_miles"] = nearby_stops.apply(
        lambda stop: haversine_distance(
            latitude,
            longitude,
            float(stop["stop_lat"]),
            float(stop["stop_lon"]),
        ),
        axis=1,
    )

    return (
        nearby_stops
        .sort_values("distance_miles")
        .head(maximum_results)
        .copy()
    )


def get_stop_information(
    stop_id: str,
    nearby_stops: pd.DataFrame,
) -> dict:
    """
    Return details for a selected nearby VIA stop.
    """

    matching_stop = nearby_stops[
        nearby_stops["stop_id"].astype(str)
        == str(stop_id)
    ]

    if matching_stop.empty:
        return {
            "stop_id": str(stop_id),
            "stop_name": "Unknown VIA stop",
            "distance_miles": None,
        }

    stop = matching_stop.iloc[0]

    return {
        "stop_id": str(stop["stop_id"]),
        "stop_name": str(stop["stop_name"]),
        "distance_miles": round(
            float(stop["distance_miles"]),
            2,
        ),
    }


def find_direct_route(
    start_stops: pd.DataFrame,
    destination_stops: pd.DataFrame,
):
    """
    Find a single GTFS trip that visits a nearby starting stop before
    visiting a nearby destination stop.
    """

    _, stop_times, trips, routes = load_gtfs_data()

    start_stop_ids = set(
        start_stops["stop_id"].astype(str)
    )

    destination_stop_ids = set(
        destination_stops["stop_id"].astype(str)
    )

    starting_times = stop_times[
        stop_times["stop_id"].isin(start_stop_ids)
    ][
        [
            "trip_id",
            "stop_id",
            "stop_sequence",
            "departure_time",
        ]
    ].copy()

    destination_times = stop_times[
        stop_times["stop_id"].isin(destination_stop_ids)
    ][
        [
            "trip_id",
            "stop_id",
            "stop_sequence",
            "arrival_time",
        ]
    ].copy()

    starting_times = starting_times.rename(
        columns={
            "stop_id": "start_stop_id",
            "stop_sequence": "start_sequence",
            "departure_time": "start_departure_time",
        }
    )

    destination_times = destination_times.rename(
        columns={
            "stop_id": "destination_stop_id",
            "stop_sequence": "destination_sequence",
            "arrival_time": "destination_arrival_time",
        }
    )

    possible_routes = starting_times.merge(
        destination_times,
        on="trip_id",
        how="inner",
    )

    possible_routes = possible_routes[
        possible_routes["start_sequence"]
        < possible_routes["destination_sequence"]
    ].copy()

    if possible_routes.empty:
        return None

    start_distance_lookup = (
        start_stops
        .set_index("stop_id")["distance_miles"]
        .to_dict()
    )

    destination_distance_lookup = (
        destination_stops
        .set_index("stop_id")["distance_miles"]
        .to_dict()
    )

    possible_routes["start_walk_miles"] = (
        possible_routes["start_stop_id"]
        .map(start_distance_lookup)
    )

    possible_routes["destination_walk_miles"] = (
        possible_routes["destination_stop_id"]
        .map(destination_distance_lookup)
    )

    possible_routes["total_walk_miles"] = (
        possible_routes["start_walk_miles"]
        + possible_routes["destination_walk_miles"]
    )

    possible_routes = possible_routes.merge(
        trips[
            [
                "trip_id",
                "route_id",
                "trip_headsign",
            ]
        ],
        on="trip_id",
        how="left",
    )

    possible_routes = possible_routes.merge(
        routes[
            [
                "route_id",
                "route_short_name",
                "route_long_name",
            ]
        ],
        on="route_id",
        how="left",
    )

    possible_routes = possible_routes.sort_values(
        [
            "total_walk_miles",
            "start_sequence",
        ]
    )

    return possible_routes.iloc[0]


def find_one_transfer_route(
    start_stops: pd.DataFrame,
    destination_stops: pd.DataFrame,
):
    """
    Find two VIA trips connected by one shared transfer stop.
    """

    stops, stop_times, trips, routes = load_gtfs_data()

    closest_start_stops = start_stops.head(6).copy()
    closest_destination_stops = (
        destination_stops.head(6).copy()
    )

    start_stop_ids = set(
        closest_start_stops["stop_id"].astype(str)
    )

    destination_stop_ids = set(
        closest_destination_stops["stop_id"].astype(str)
    )

    trip_details = trips[
        [
            "trip_id",
            "route_id",
            "trip_headsign",
        ]
    ].copy()

    start_candidates = stop_times[
        stop_times["stop_id"].isin(start_stop_ids)
    ][
        [
            "trip_id",
            "stop_id",
            "stop_sequence",
            "departure_time",
        ]
    ].copy()

    destination_candidates = stop_times[
        stop_times["stop_id"].isin(destination_stop_ids)
    ][
        [
            "trip_id",
            "stop_id",
            "stop_sequence",
            "arrival_time",
        ]
    ].copy()

    start_candidates = start_candidates.rename(
        columns={
            "stop_id": "start_stop_id",
            "stop_sequence": "start_sequence",
            "departure_time": "start_departure_time",
        }
    )

    destination_candidates = destination_candidates.rename(
        columns={
            "stop_id": "destination_stop_id",
            "stop_sequence": "destination_sequence",
            "arrival_time": "destination_arrival_time",
        }
    )

    start_candidates = start_candidates.merge(
        trip_details,
        on="trip_id",
        how="left",
    )

    destination_candidates = destination_candidates.merge(
        trip_details,
        on="trip_id",
        how="left",
    )

    start_distance_lookup = (
        closest_start_stops
        .set_index("stop_id")["distance_miles"]
        .to_dict()
    )

    destination_distance_lookup = (
        closest_destination_stops
        .set_index("stop_id")["distance_miles"]
        .to_dict()
    )

    start_candidates["walk_distance"] = (
        start_candidates["start_stop_id"]
        .map(start_distance_lookup)
    )

    destination_candidates["walk_distance"] = (
        destination_candidates["destination_stop_id"]
        .map(destination_distance_lookup)
    )

    start_candidates = (
        start_candidates
        .sort_values(
            [
                "walk_distance",
                "start_sequence",
            ]
        )
        .drop_duplicates("trip_id")
        .head(100)
    )

    destination_candidates = (
        destination_candidates
        .sort_values(
            [
                "walk_distance",
                "destination_sequence",
            ]
        )
        .drop_duplicates("trip_id")
        .head(100)
    )

    candidate_trip_ids = set(
        start_candidates["trip_id"].astype(str)
    )

    candidate_trip_ids.update(
        destination_candidates["trip_id"].astype(str)
    )

    candidate_stop_times = stop_times[
        stop_times["trip_id"].isin(candidate_trip_ids)
    ].copy()

    trip_stop_groups = {
        str(trip_id): group.sort_values(
            "stop_sequence"
        )
        for trip_id, group in candidate_stop_times.groupby(
            "trip_id"
        )
    }

    best_match = None
    best_score = None

    for _, first_trip in start_candidates.iterrows():
        first_trip_id = str(first_trip["trip_id"])

        first_trip_stops = trip_stop_groups.get(
            first_trip_id
        )

        if first_trip_stops is None:
            continue

        downstream_stops = first_trip_stops[
            first_trip_stops["stop_sequence"]
            > first_trip["start_sequence"]
        ]

        if downstream_stops.empty:
            continue

        downstream_lookup = {
            str(row["stop_id"]): row
            for _, row in downstream_stops.iterrows()
        }

        for _, second_trip in destination_candidates.iterrows():
            second_trip_id = str(second_trip["trip_id"])

            if first_trip_id == second_trip_id:
                continue

            if (
                str(first_trip["route_id"])
                == str(second_trip["route_id"])
            ):
                continue

            second_trip_stops = trip_stop_groups.get(
                second_trip_id
            )

            if second_trip_stops is None:
                continue

            upstream_stops = second_trip_stops[
                second_trip_stops["stop_sequence"]
                < second_trip["destination_sequence"]
            ]

            if upstream_stops.empty:
                continue

            upstream_lookup = {
                str(row["stop_id"]): row
                for _, row in upstream_stops.iterrows()
            }

            shared_transfer_stops = (
                set(downstream_lookup)
                & set(upstream_lookup)
            )

            for transfer_stop_id in shared_transfer_stops:
                first_transfer_stop = downstream_lookup[
                    transfer_stop_id
                ]

                second_transfer_stop = upstream_lookup[
                    transfer_stop_id
                ]

                try:
                    first_arrival_seconds = (
                        gtfs_time_to_seconds(
                            first_transfer_stop[
                                "arrival_time"
                            ]
                        )
                    )

                    second_departure_seconds = (
                        gtfs_time_to_seconds(
                            second_transfer_stop[
                                "departure_time"
                            ]
                        )
                    )

                    trip_start_seconds = (
                        gtfs_time_to_seconds(
                            first_trip[
                                "start_departure_time"
                            ]
                        )
                    )

                    trip_end_seconds = (
                        gtfs_time_to_seconds(
                            second_trip[
                                "destination_arrival_time"
                            ]
                        )
                    )
                except (
                    ValueError,
                    TypeError,
                    AttributeError,
                ):
                    continue

                transfer_wait_seconds = (
                    second_departure_seconds
                    - first_arrival_seconds
                )

                total_duration_seconds = (
                    trip_end_seconds
                    - trip_start_seconds
                )

                if not 120 <= transfer_wait_seconds <= 5400:
                    continue

                if total_duration_seconds <= 0:
                    continue

                total_walk_distance = (
                    float(first_trip["walk_distance"])
                    + float(second_trip["walk_distance"])
                )

                score = (
                    total_duration_seconds
                    + transfer_wait_seconds
                    + round(total_walk_distance * 1800)
                )

                if (
                    best_score is None
                    or score < best_score
                ):
                    best_score = score

                    best_match = {
                        "first_trip": first_trip,
                        "second_trip": second_trip,
                        "transfer_stop_id": (
                            transfer_stop_id
                        ),
                        "transfer_arrival_time": str(
                            first_transfer_stop[
                                "arrival_time"
                            ]
                        ).strip(),
                        "transfer_departure_time": str(
                            second_transfer_stop[
                                "departure_time"
                            ]
                        ).strip(),
                        "transfer_wait_seconds": (
                            transfer_wait_seconds
                        ),
                        "total_duration_seconds": (
                            total_duration_seconds
                        ),
                    }

    if best_match is None:
        return None

    routes_lookup = routes.set_index("route_id")
    stops_lookup = stops.set_index("stop_id")

    first_trip = best_match["first_trip"]
    second_trip = best_match["second_trip"]

    first_route_id = str(first_trip["route_id"])
    second_route_id = str(second_trip["route_id"])

    if (
        first_route_id not in routes_lookup.index
        or second_route_id not in routes_lookup.index
    ):
        return None

    transfer_stop_id = str(
        best_match["transfer_stop_id"]
    )

    if transfer_stop_id not in stops_lookup.index:
        return None

    first_route = routes_lookup.loc[first_route_id]
    second_route = routes_lookup.loc[second_route_id]
    transfer_stop = stops_lookup.loc[transfer_stop_id]

    starting_stop = get_stop_information(
        first_trip["start_stop_id"],
        closest_start_stops,
    )

    destination_stop = get_stop_information(
        second_trip["destination_stop_id"],
        closest_destination_stops,
    )

    return {
        "first_route_number": str(
            first_route["route_short_name"]
        ),
        "first_route_name": str(
            first_route.get(
                "route_long_name",
                "",
            )
        ),
        "first_headsign": str(
            first_trip.get(
                "trip_headsign",
                "",
            )
        ),
        "second_route_number": str(
            second_route["route_short_name"]
        ),
        "second_route_name": str(
            second_route.get(
                "route_long_name",
                "",
            )
        ),
        "second_headsign": str(
            second_trip.get(
                "trip_headsign",
                "",
            )
        ),
        "starting_stop": starting_stop,
        "destination_stop": destination_stop,
        "transfer_stop_id": transfer_stop_id,
        "transfer_stop_name": str(
            transfer_stop["stop_name"]
        ),
        "start_departure_time": str(
            first_trip["start_departure_time"]
        ).strip(),
        "transfer_arrival_time": best_match[
            "transfer_arrival_time"
        ],
        "transfer_departure_time": best_match[
            "transfer_departure_time"
        ],
        "destination_arrival_time": str(
            second_trip["destination_arrival_time"]
        ).strip(),
        "transfer_wait": format_duration(
            best_match["transfer_wait_seconds"]
        ),
        "duration": format_duration(
            best_match["total_duration_seconds"]
        ),
    }


def build_direct_route_response(
    selected_route,
    start_stops: pd.DataFrame,
    destination_stops: pd.DataFrame,
    start_location: dict,
    destination_location: dict,
) -> dict:
    """
    Build the response for a direct VIA trip.
    """

    starting_stop = get_stop_information(
        selected_route["start_stop_id"],
        start_stops,
    )

    destination_stop = get_stop_information(
        selected_route["destination_stop_id"],
        destination_stops,
    )

    departure_seconds = gtfs_time_to_seconds(
        selected_route["start_departure_time"]
    )

    arrival_seconds = gtfs_time_to_seconds(
        selected_route["destination_arrival_time"]
    )

    duration_seconds = arrival_seconds - departure_seconds

    if duration_seconds > 0:
        duration_text = format_duration(
            duration_seconds
        )
    else:
        duration_text = "See VIA schedule"

    route_number = str(
        selected_route["route_short_name"]
    )

    route_name = str(
        selected_route.get(
            "route_long_name",
            "",
        )
    )

    headsign = str(
        selected_route.get(
            "trip_headsign",
            "",
        )
    )

    instructions = (
        f"Walk approximately "
        f"{starting_stop['distance_miles']} miles to "
        f"{starting_stop['stop_name']}. "
        f"Board VIA Route {route_number} toward "
        f"{headsign}. "
        f"Exit at {destination_stop['stop_name']}. "
        f"Your destination is approximately "
        f"{destination_stop['distance_miles']} miles "
        f"from that stop."
    )

    return {
        "route": f"VIA Route {route_number}",
        "route_number": route_number,
        "route_name": route_name,
        "duration": duration_text,
        "estimated_time": duration_text,
        "transfers": 0,
        "transfer": "No transfer required",
        "fare": "$1.30",
        "departure_time": str(
            selected_route["start_departure_time"]
        ).strip(),
        "arrival_time": str(
            selected_route["destination_arrival_time"]
        ).strip(),
        "headsign": headsign,
        "starting_stop": starting_stop,
        "destination_stop": destination_stop,
        "instructions": instructions,
        "details": instructions,
        "start_location": start_location[
            "display_name"
        ],
        "destination_location": destination_location[
            "display_name"
        ],
        "data_source": "VIA Metropolitan Transit GTFS",
    }


def build_transfer_route_response(
    transfer_route: dict,
    start_location: dict,
    destination_location: dict,
) -> dict:
    """
    Build the response for a one-transfer VIA trip.
    """

    first_route = transfer_route[
        "first_route_number"
    ]

    second_route = transfer_route[
        "second_route_number"
    ]

    transfer_stop = transfer_route[
        "transfer_stop_name"
    ]

    instructions = (
        f"Walk approximately "
        f"{transfer_route['starting_stop']['distance_miles']} "
        f"miles to "
        f"{transfer_route['starting_stop']['stop_name']}. "
        f"Board VIA Route {first_route} toward "
        f"{transfer_route['first_headsign']}. "
        f"Exit at {transfer_stop}. "
        f"Transfer to VIA Route {second_route} toward "
        f"{transfer_route['second_headsign']}. "
        f"Exit at "
        f"{transfer_route['destination_stop']['stop_name']}. "
        f"Your destination is approximately "
        f"{transfer_route['destination_stop']['distance_miles']} "
        f"miles from that stop."
    )

    return {
        "route": (
            f"VIA Routes {first_route} and "
            f"{second_route}"
        ),
        "route_number": (
            f"{first_route} → {second_route}"
        ),
        "route_name": (
            f"{transfer_route['first_route_name']} / "
            f"{transfer_route['second_route_name']}"
        ),
        "duration": transfer_route["duration"],
        "estimated_time": transfer_route["duration"],
        "transfers": 1,
        "transfer": transfer_stop,
        "transfer_wait": transfer_route[
            "transfer_wait"
        ],
        "fare": "$1.30",
        "departure_time": transfer_route[
            "start_departure_time"
        ],
        "arrival_time": transfer_route[
            "destination_arrival_time"
        ],
        "first_route": {
            "route_number": first_route,
            "route_name": transfer_route[
                "first_route_name"
            ],
            "headsign": transfer_route[
                "first_headsign"
            ],
        },
        "second_route": {
            "route_number": second_route,
            "route_name": transfer_route[
                "second_route_name"
            ],
            "headsign": transfer_route[
                "second_headsign"
            ],
        },
        "starting_stop": transfer_route[
            "starting_stop"
        ],
        "destination_stop": transfer_route[
            "destination_stop"
        ],
        "instructions": instructions,
        "details": instructions,
        "start_location": start_location[
            "display_name"
        ],
        "destination_location": destination_location[
            "display_name"
        ],
        "data_source": "VIA Metropolitan Transit GTFS",
    }


def get_placeholder_route(
    start: str,
    destination: str,
) -> dict:
    """
    Calculate a real direct or one-transfer VIA route.

    The original function name remains unchanged so routes.py does
    not need to be modified.
    """

    try:
        start_location = geocode_location(start)

        destination_location = geocode_location(
            destination
        )

        start_stops = find_nearest_stops(
            start_location["latitude"],
            start_location["longitude"],
        )

        destination_stops = find_nearest_stops(
            destination_location["latitude"],
            destination_location["longitude"],
        )

        selected_direct_route = find_direct_route(
            start_stops,
            destination_stops,
        )

        if selected_direct_route is not None:
            return build_direct_route_response(
                selected_direct_route,
                start_stops,
                destination_stops,
                start_location,
                destination_location,
            )

        selected_transfer_route = (
            find_one_transfer_route(
                start_stops,
                destination_stops,
            )
        )

        if selected_transfer_route is not None:
            return build_transfer_route_response(
                selected_transfer_route,
                start_location,
                destination_location,
            )

        return create_error_route(
            route_message="No route found",
            instructions=(
                "No direct or one-transfer VIA route was found "
                "between the nearby stops. Try entering more "
                "specific addresses or selecting nearby landmarks."
            ),
            details=(
                f"No direct or one-transfer VIA route was found "
                f"from {start} to {destination}."
            ),
            start_location=start_location["display_name"],
            destination_location=destination_location[
                "display_name"
            ],
        )

    except requests.exceptions.Timeout:
        return create_error_route(
            route_message="Location lookup timed out",
            instructions=(
                "The location lookup service took too long "
                "to respond. Please try again."
            ),
            details="Location lookup timed out.",
        )

    except requests.exceptions.RequestException as error:
        return create_error_route(
            route_message="Location lookup failed",
            instructions=(
                "The app could not contact the location lookup "
                "service. Check your internet connection and "
                "try again."
            ),
            details=str(error),
        )

    except (ValueError, FileNotFoundError) as error:
        return create_error_route(
            route_message="Route could not be calculated",
            instructions=str(error),
            details=str(error),
        )

    except Exception as error:
        return create_error_route(
            route_message="Unexpected routing error",
            instructions=(
                "An unexpected error occurred while searching "
                "the VIA schedule."
            ),
            details=str(error),
        )