from fastapi import APIRouter

from models.route_request import RouteRequest
from services.via_service import get_placeholder_route
from services.gemini_service import generate_ai_explanation
from services.maps_service import get_map_placeholder


router = APIRouter()


@router.get("/")
def home():
    return {
        "status": "success",
        "message": (
            "AI Bus Travel Assistant Backend is running!"
        ),
    }


@router.post("/route")
def find_route(request: RouteRequest):
    route_info = get_placeholder_route(
        request.start,
        request.destination,
    )

    ai_explanation = generate_ai_explanation(
        request.start,
        request.destination,
        route_info,
    )

    map_info = get_map_placeholder(
        request.start,
        request.destination,
    )

    return {
        "status": "success",
        "start": request.start,
        "destination": request.destination,
        "route": route_info,
        "ai_explanation": ai_explanation,
        "map": map_info,
    }