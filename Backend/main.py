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
vectorizer = TfidfVectorizer()
problemas_tfidf = vectorizer.fit_transform(problemas)

# ===== Modelos =====
class Query(BaseModel):
    query: str
    top_n: int = 4
    umbral: float = 0.1


# ===== Endpoints =====
@app.get("/")
def root():
    return {"msg": "API Soluciones TI funcionando 🚀"}

@app.post("/buscar")
def buscar(q: Query):
    query_vec = vectorizer.transform([q.query])
    similitudes = cosine_similarity(query_vec, problemas_tfidf)[0]
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
