# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---- App y CORS ----
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción limita esto a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Modelo y datos ----
# Carga el CSV (debe tener columnas: Problema, Solucion)
data = pd.read_csv("problemas.csv")
problemas = data["Problema"].fillna("").tolist()
soluciones = data["Solucion"].fillna("").tolist()

# Vectorizador TF-IDF (más liviano que embeddings)
vectorizer = TfidfVectorizer()
problemas_tfidf = vectorizer.fit_transform(problemas)

# ---- Esquema de entrada ----
class Query(BaseModel):
    query: str
    top_n: int = 4
    umbral: float = 0.0  # umbral de similitud (0 a 1). Si no alcanza, se filtra.

# ---- Endpoint ----
@app.post("/buscar")
def buscar(q: Query):
    # Transformamos la consulta en vector TF-IDF
    query_vec = vectorizer.transform([q.query])

    # Similitud coseno
    similitudes = cosine_similarity(query_vec, problemas_tfidf)[0]

    # Top N índices
    indices = similitudes.argsort()[::-1][: q.top_n]

    resultados = []
    for idx in indices.tolist():
        score = float(similitudes[idx])
        if score >= q.umbral:
            resultados.append({
                "problema": problemas[idx],
                "solucion": soluciones[idx],
                "score": score
            })

    return {"resultados": resultados}


@app.get("/todas")
def todas_las_soluciones():
    resultados = []
    for problema, solucion in zip(problemas, soluciones):
        resultados.append({
            "problema": problema,
            "solucion": solucion,
            "score": 1.0
        })
    return {"resultados": resultados}
