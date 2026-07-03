const API_BASE_URL = "http://127.0.0.1:8000";

export async function findRoute(start, destination) {
  const response = await fetch(`${API_BASE_URL}/route`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      start,
      destination,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch route");
  }

  return await response.json();
}