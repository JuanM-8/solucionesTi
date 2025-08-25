# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---- App y CORS ----
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://solucionesti.netlify.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Autenticación (simple) ----
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Usuarios simulados en memoria (puedes poner en BD luego)
fake_users_db = {
    "juan": {
        "username": "juan",
        "password": "1234",  # ⚠️ en producción nunca guardar plano
        "token": "secrettoken123"  # token estático para simplificar
    }
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Buscar si el token existe en nuestra "BD"
    for user in fake_users_db.values():
        if user["token"] == token:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or user_dict["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    # Retornamos un token fijo (simple)
    return {"access_token": user_dict["token"], "token_type": "bearer"}

# ---- Modelo y datos ----
data = pd.read_csv("problemas.csv")
problemas = data["Problema"].fillna("").tolist()
soluciones = data["Solucion"].fillna("").tolist()

vectorizer = TfidfVectorizer()
problemas_tfidf = vectorizer.fit_transform(problemas)

class Query(BaseModel):
    query: str
    top_n: int = 4
    umbral: float = 0.0

# ---- Endpoint protegido ----
@app.post("/buscar")
def buscar(q: Query, user: dict = Depends(get_current_user)):
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
def todas_las_soluciones(user: dict = Depends(get_current_user)):
    resultados = []
    for problema, solucion in zip(problemas, soluciones):
        resultados.append({
            "problema": problema,
            "solucion": solucion,
            "score": 1.0
        })
    return {"resultados": resultados}
