function RouteCard({ routeData }) {
  if (!routeData) {
    return null;
  }

  return (
    <div className="route-card">
      <h2>Recommended Route</h2>

      <p><strong>From:</strong> {routeData.start}</p>
      <p><strong>To:</strong> {routeData.destination}</p>

      <hr />

      <p><strong>Route:</strong> VIA Route {routeData.route.route_number}</p>
      <p><strong>Transfer:</strong> {routeData.route.transfer}</p>
      <p><strong>Estimated Time:</strong> {routeData.route.estimated_time}</p>
      <p><strong>Fare:</strong> {routeData.route.fare}</p>

      <hr />

      <h3>AI Explanation</h3>
      <p>{routeData.ai_explanation}</p>
    </div>
  );
}

export default RouteCard;