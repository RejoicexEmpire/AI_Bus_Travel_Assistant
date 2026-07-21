import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_FOLDER = PROJECT_ROOT / "backend"

if str(BACKEND_FOLDER) not in sys.path:
    sys.path.insert(0, str(BACKEND_FOLDER))


from services.gemini_service import generate_ai_explanation
from services.maps_service import get_map_placeholder
from services.via_service import get_placeholder_route


st.set_page_config(
    page_title="AI Bus Travel Assistant",
    layout="centered",
)


def display_value(value, fallback="Unavailable"):
    """
    Return a readable value for missing route fields.
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


with st.form("route_form"):
    start = st.text_input(
        "Starting location",
        placeholder=(
            "Example: San Antonio International Airport"
        ),
    )

    destination = st.text_input(
        "Destination",
        placeholder="Example: The Alamo",
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
                route_info = get_placeholder_route(
                    cleaned_start,
                    cleaned_destination,
                )

                ai_explanation = generate_ai_explanation(
                    cleaned_start,
                    cleaned_destination,
                    route_info,
                )

                map_info = get_map_placeholder(
                    cleaned_start,
                    cleaned_destination,
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
            st.write(
                f"**Estimated Time:** {estimated_time}"
            )
            st.write(f"**Fare:** {fare}")

            departure_time = display_value(
                route_info.get("departure_time"),
            )

            arrival_time = display_value(
                route_info.get("arrival_time"),
            )

            if departure_time != "Unavailable":
                st.write(
                    f"**Scheduled Departure:** {departure_time}"
                )

            if arrival_time != "Unavailable":
                st.write(
                    f"**Scheduled Arrival:** {arrival_time}"
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
                            starting_stop.get(
                                "stop_name",
                                "Unavailable",
                            )
                        )
                        st.write(
                            "Walking distance: "
                            f"{display_value(
                                starting_stop.get(
                                    'distance_miles'
                                )
                            )} miles"
                        )

                    if destination_stop:
                        st.write("**Destination VIA stop**")
                        st.write(
                            destination_stop.get(
                                "stop_name",
                                "Unavailable",
                            )
                        )
                        st.write(
                            "Walking distance: "
                            f"{display_value(
                                destination_stop.get(
                                    'distance_miles'
                                )
                            )} miles"
                        )

            if map_info:
                with st.expander("Map Information"):
                    if isinstance(map_info, dict):
                        st.json(map_info)
                    else:
                        st.write(map_info)

            with st.expander("Raw Route Data"):
                st.json(route_info)

        except Exception as error:
            st.error(
                "An unexpected error occurred while planning "
                "the trip."
            )

            with st.expander("Technical Error Details"):
                st.code(str(error))
