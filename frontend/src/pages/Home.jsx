import { useState } from "react";

import SearchForm from "../components/SearchForm";
import RouteCard from "../components/RouteCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { findRoute } from "../services/api";

function Home() {
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSearch(start, destination) {
    setLoading(true);
    setRouteData(null);

    try {
      const data = await findRoute(start, destination);
      setRouteData(data);
    } catch (error) {
      console.error(error);
      alert("Unable to get route from backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="home">
      <h1>Plan safer and smarter bus trips in San Antonio.</h1>

      <SearchForm onSearch={handleSearch} />

      {loading && <LoadingSpinner />}

      <RouteCard routeData={routeData} />
    </main>
  );
}

export default Home;