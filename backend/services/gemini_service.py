def generate_ai_explanation(start: str, destination: str, route_info: dict):
    return (
        f"The recommended trip from {start} to {destination} is VIA Route "
        f"{route_info['route_number']}. You may need to transfer at "
        f"{route_info['transfer']}. Estimated travel time is "
        f"{route_info['estimated_time']}. The estimated fare is {route_info['fare']}."
    )