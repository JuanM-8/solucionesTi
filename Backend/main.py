from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción mejor poner tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ===== Cargar datos =====
df = pd.read_csv("problemas.csv")  # tu archivo con problemas y soluciones
problemas = df["Problema"].fillna("").tolist()
soluciones = df["Solucion"].fillna("").tolist()

# ===== Vectorizador =====
vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2))  
# 🔎 con ngram_range detecta mejor fragmentos como "wif" ~ "wifi"
problemas_tfidf = vectorizer.fit_transform(problemas)

# ===== Modelos =====
class Query(BaseModel):
    query: str
    top_n: int = 4
    umbral: float = 0.05   # 🔽 bajamos el mínimo

# ===== Endpoints =====
@app.get("/")
def root():
    return {"msg": "API Soluciones TI funcionando 🚀"}

@app.post("/buscar")
def buscar(q: Query):
    query_vec = vectorizer.transform([q.query])
    similitudes = cosine_similarity(query_vec, problemas_tfidf)[0]

    # Ordenar de mayor a menor similitud
    indices = similitudes.argsort()[::-1]

    resultados = []
    for idx in indices:
        score = float(similitudes[idx])
        if score >= q.umbral or len(resultados) < q.top_n:
            resultados.append({
                "problema": problemas[idx],
                "solucion": soluciones[idx],
                "score": round(score, 3)
            })
        if len(resultados) >= q.top_n:
            break

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
