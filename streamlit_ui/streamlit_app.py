import sys
from pathlib import Path

import streamlit as st


# Add the backend directory to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_FOLDER = PROJECT_ROOT / "backend"

if str(BACKEND_FOLDER) not in sys.path:
    sys.path.insert(0, str(BACKEND_FOLDER))


from services.gemini_service import generate_ai_explanation
from services.via_service import find_via_route


st.set_page_config(
    page_title="AI Bus Travel Assistant",
    layout="centered",
)


def display_value(
    value,
    fallback: str = "Unavailable",
) -> str:
    """
    Return a readable string for a route value.

    Missing, empty, or whitespace-only values are replaced with the
    supplied fallback text.
    """

    if value is None:
        return fallback

    value_text = str(value).strip()

    if not value_text:
        return fallback

    return value_text


st.title("AI Bus Travel Assistant")

st.write(
    "Enter a starting location and destination to receive a "
    "VIA bus route recommendation based on local GTFS schedule data."
)

st.caption(
    "This prototype uses downloaded VIA schedule data and does not "
    "provide live bus locations or real-time arrival predictions."
)


with st.form("route_form"):
    start = st.text_input(
        "Starting location",
        placeholder="Example: Downtown San Antonio",
    )

    destination = st.text_input(
        "Destination",
        placeholder="Example: San Antonio International Airport",
    )

    submit_button = st.form_submit_button(
        "Plan My Trip",
        type="primary",
        use_container_width=True,
    )


if submit_button:
    cleaned_start = start.strip()
    cleaned_destination = destination.strip()

    if not cleaned_start or not cleaned_destination:
        st.error(
            "Please enter both a starting location and a destination."
        )

    elif cleaned_start.lower() == cleaned_destination.lower():
        st.error(
            "The starting location and destination must be different."
        )

    else:
        try:
            with st.spinner(
                "Searching VIA schedule data and generating guidance..."
            ):
                route_info = find_via_route(
                    cleaned_start,
                    cleaned_destination,
                )

                if not isinstance(route_info, dict):
                    raise ValueError(
                        "The routing service returned an invalid response."
                    )

                ai_explanation = generate_ai_explanation(
                    cleaned_start,
                    cleaned_destination,
                    route_info,
                )

            route_title = display_value(
                route_info.get("route"),
                "No route found",
            )

            route_number = display_value(
                route_info.get("route_number"),
            )

            transfer = display_value(
                route_info.get("transfer"),
            )

            estimated_time = display_value(
                route_info.get("estimated_time")
                or route_info.get("duration"),
            )

            fare = display_value(
                route_info.get("fare"),
            )

            route_found = (
                route_info.get("route_number") is not None
            )

            if route_found:
                st.success("Your route recommendation is ready.")
            else:
                st.warning(
                    "A complete VIA itinerary could not be found."
                )

            st.subheader("Recommended Route")

            st.write(f"**From:** {cleaned_start}")
            st.write(f"**To:** {cleaned_destination}")

            st.divider()

            st.write(f"**Route:** {route_title}")

            if route_number != "Unavailable":
                st.write(
                    f"**Route Number or Sequence:** {route_number}"
                )

            st.write(f"**Transfer:** {transfer}")
            st.write(f"**Estimated Time:** {estimated_time}")
            st.write(f"**Fare:** {fare}")

            departure_time = display_value(
                route_info.get("departure_time"),
            )

            arrival_time = display_value(
                route_info.get("arrival_time"),
            )

            if departure_time != "Unavailable":
                st.write(
                    f"**GTFS Scheduled Departure:** {departure_time}"
                )

            if arrival_time != "Unavailable":
                st.write(
                    f"**GTFS Scheduled Arrival:** {arrival_time}"
                )

            if (
                departure_time != "Unavailable"
                or arrival_time != "Unavailable"
            ):
                st.caption(
                    "Schedule times come from the downloaded VIA GTFS "
                    "dataset and are not live arrival predictions."
                )

            transfer_wait = display_value(
                route_info.get("transfer_wait"),
            )

            if transfer_wait != "Unavailable":
                st.write(
                    f"**Estimated Transfer Wait:** {transfer_wait}"
                )

            st.divider()

            st.subheader("AI Explanation")
            st.write(ai_explanation)

            instructions = route_info.get("instructions")

            if instructions:
                with st.expander("Detailed Route Instructions"):
                    st.write(instructions)

            starting_stop = route_info.get("starting_stop")
            destination_stop = route_info.get(
                "destination_stop"
            )

            if starting_stop or destination_stop:
                with st.expander("Stop Information"):
                    if starting_stop:
                        st.write("**Starting VIA stop**")

                        st.write(
                            display_value(
                                starting_stop.get("stop_name")
                            )
                        )

                        start_distance = display_value(
                            starting_stop.get(
                                "distance_miles"
                            )
                        )

                        st.write(
                            f"Walking distance: "
                            f"{start_distance} miles"
                        )

                    if destination_stop:
                        st.write("**Destination VIA stop**")

                        st.write(
                            display_value(
                                destination_stop.get("stop_name")
                            )
                        )

                        destination_distance = display_value(
                            destination_stop.get(
                                "distance_miles"
                            )
                        )

                        st.write(
                            f"Walking distance: "
                            f"{destination_distance} miles"
                        )

            with st.expander("Technical Route Details"):
                st.json(route_info)

        except Exception:
            st.error(
                "An unexpected error occurred while planning the trip. "
                "Please check your connection and try again."
            )