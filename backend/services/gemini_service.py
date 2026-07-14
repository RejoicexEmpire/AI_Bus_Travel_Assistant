import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_ai_explanation(
    start: str,
    destination: str,
    route_info: dict,
) -> str:
    """
    Ask Gemini to explain the returned VIA route without inventing
    additional transit information.
    """

    route_name = (
        route_info.get("route")
        or "No route available"
    )

    route_number = (
        route_info.get("route_number")
        or "Unavailable"
    )

    transfer = (
        route_info.get("transfer")
        or "Unavailable"
    )

    transfer_count = route_info.get("transfers")

    if transfer_count is None:
        transfer_count_text = "Unavailable"
    else:
        transfer_count_text = str(transfer_count)

    estimated_time = (
        route_info.get("estimated_time")
        or route_info.get("duration")
        or "Unavailable"
    )

    departure_time = (
        route_info.get("departure_time")
        or "Unavailable"
    )

    arrival_time = (
        route_info.get("arrival_time")
        or "Unavailable"
    )

    fare = route_info.get(
        "fare",
        "Unavailable",
    )

    instructions = (
        route_info.get("instructions")
        or route_info.get("details")
        or "No additional route instructions were returned."
    )

    prompt = f"""
You are an AI bus travel assistant for San Antonio.

Explain this VIA transit result in simple, helpful language.

Starting location:
{start}

Destination:
{destination}

Route:
{route_name}

Route number or route sequence:
{route_number}

Number of transfers:
{transfer_count_text}

Transfer location:
{transfer}

Estimated travel time:
{estimated_time}

Scheduled departure:
{departure_time}

Scheduled arrival:
{arrival_time}

Fare:
{fare}

Route instructions:
{instructions}

Rules:
- Only use the transit information provided above.
- Do not invent route numbers, stops, times, transfers, or fares.
- If the route result says no route was found, clearly explain that.
- Keep the explanation concise.
- Use plain text without Markdown symbols such as asterisks.
"""

    if client is None:
        return (
            "AI explanation is unavailable because the Gemini "
            f"API key was not loaded. Route details: {instructions}"
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if response.text:
            return response.text.strip()

        return (
            "The route information was found, but Gemini did "
            f"not return an explanation. Route details: {instructions}"
        )

    except Exception:
        return (
            "AI explanation is temporarily unavailable. "
            f"Route details: {instructions}"
        )