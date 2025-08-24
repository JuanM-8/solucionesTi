# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer, util

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
problemas = data["Problema"].tolist()
soluciones = data["Solucion"].tolist()

# Modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
problemas_embeddings = model.encode(problemas, convert_to_tensor=True)

# ---- Esquema de entrada ----
class Query(BaseModel):
    query: str
    top_n: int = 4 # cuántas soluciones devolver 
    umbral: float = 0.0  # umbral de similitud (0 a 1). Si no alcanza, se filtra.

# ---- Endpoint ----
@app.post("/buscar")
def buscar(q: Query):
    # Embedding de la consulta
    query_embedding = model.encode(q.query, convert_to_tensor=True)

    # Similitudes (cosine)
    similitudes = util.pytorch_cos_sim(query_embedding, problemas_embeddings)[0]

    # Top N índices
    indices = similitudes.argsort(descending=True)[: q.top_n]

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
            "score": 1.0  # opcional, como marcador
        })
    return {"resultados": resultados}
