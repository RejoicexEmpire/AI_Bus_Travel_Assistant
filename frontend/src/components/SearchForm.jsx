import { useState } from "react";

function SearchForm({ onSearch }) {
  const [start, setStart] = useState("");
  const [destination, setDestination] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    if (!start || !destination) {
      alert("Please enter both a starting location and destination.");
      return;
    }

    onSearch(start, destination);
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Starting location"
        value={start}
        onChange={(e) => setStart(e.target.value)}
      />

      <input
        type="text"
        placeholder="Destination"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
      />

      <button type="submit">Find Route</button>
    </form>
  );
}

export default SearchForm;