import { useState, useEffect } from "react";
import "./App.css";

const API_BASE = "https://solucionesti.onrender.com";

function App() {
  const [query, setQuery] = useState("");
  const [allResults, setAllResults] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  // Credenciales
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // Token guardado
  const token = localStorage.getItem("token");

  // ---- LOGIN ----
  const handleLogin = async () => {
    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!res.ok) throw new Error("Login fallido");
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      setLoggedIn(true);
    } catch (err) {
      setErrorMsg("Usuario o contraseña incorrectos");
    }
  };

  // ---- Cargar inicial ----
  useEffect(() => {
    if (!token) return;
    const cargarInicial = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/todas`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Error al cargar soluciones");
        const data = await res.json();
        setAllResults(data.resultados || []);
        const shuffled = [...data.resultados].sort(() => 0.5 - Math.random());
        setResults(shuffled.slice(0, 4));
        setLoggedIn(true);
      } catch (err) {
        setErrorMsg("No se pudieron cargar las soluciones iniciales.");
      } finally {
        setLoading(false);
      }
    };
    cargarInicial();
  }, [token]);

  // ---- Buscar ----
  const buscarSoluciones = async () => {
    if (!query) return;
    setLoading(true);
    setErrorMsg("");
    setShowAll(false);

    try {
      const res = await fetch(`${API_BASE}/buscar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ query, top_n: 4 }),
      });

      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data = await res.json();
      setResults(data.resultados || []);
    } catch (err) {
      setErrorMsg("No se pudo consultar el backend. ¿Login realizado?");
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
  if (!loggedIn) {
    return (
      <div className="login-container">
        <h1>Iniciar sesión</h1>
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Entrar</button>
        {errorMsg && <div className="error">{errorMsg}</div>}
      </div>
    );
  }

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
