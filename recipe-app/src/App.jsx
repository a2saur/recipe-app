import { useState } from "react";
import "./App.css";

function App() {
  const [search, setSearch] = useState("");

  return (
    <main>
      <h1>My Recipe Book</h1>
      <p>Find something delicious to make.</p>

      <input
        type="text"
        placeholder="Search recipes..."
        value={search}
        onChange={(event) => setSearch(event.target.value)}
      />

      <p>Current search: {search || "Nothing yet"}</p>
    </main>
  );
}

export default App;
