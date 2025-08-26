import { useState, useEffect } from "react";
import "./App.css";

// ⚠️ Cambia esta URL cuando lo subas a Render
const API_BASE = "https://solucionesti.onrender.com";

function App() {
  const [query, setQuery] = useState("");
  const [allResults, setAllResults] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [showAll, setShowAll] = useState(false);

  // ---- Cargar inicial ----
  useEffect(() => {
    const cargarInicial = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/todas`);
        if (!res.ok) throw new Error("Error al cargar soluciones");
        const data = await res.json();
        setAllResults(data.resultados || []);
        const shuffled = [...data.resultados].sort(() => 0.5 - Math.random());
        setResults(shuffled.slice(0, 4));
      } catch (err) {
        setErrorMsg("No se pudieron cargar las soluciones iniciales.");
      } finally {
        setLoading(false);
      }
    };
    cargarInicial();
  }, []);

  // ---- Buscar ----
  const buscarSoluciones = async () => {
    if (!query) return;
    setLoading(true);
    setErrorMsg("");
    setShowAll(false);

    try {
      const res = await fetch(`${API_BASE}/buscar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_n: 4 }),
      });

      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data = await res.json();
      setResults(data.resultados || []);
    } catch (err) {
      setErrorMsg("No se pudo consultar el backend.");
    } finally {
      setLoading(false);
    }
  };

  const mostrarTodas = () => {
    setResults(allResults);
    setShowAll(true);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") buscarSoluciones();
  };

  // ---- Render ----
  return (
    <div className="app-container">
      <section className="app-header">
        <h1 className="app-title">Buscador de Soluciones</h1>
      </section>

      <div className="panel">
        <input
          type="text"
          placeholder="Describe tu problema… (Enter para buscar)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="input-box"
        />
      </div>

      {errorMsg && <div className="error">{errorMsg}</div>}

      <section className="results">
        {results.length === 0 && !loading && !errorMsg && (
          <div className="empty">
            No hay resultados aún. Escribe algo o muestra todas las soluciones.
          </div>
        )}

        {results.map((r, i) => (
          <div key={i} className="card">
            <h2 className="problem">🔹 {r.problema}</h2>
            <p className="solution">✅ {r.solucion}</p>
          </div>
        ))}
      </section>

      <button className="btn" onClick={mostrarTodas}>
        Mostrar todas las soluciones
      </button>

      <footer>
        <p>∞ Juan Marin ∞</p>
      </footer>
    </div>
  );
}

export default App;
