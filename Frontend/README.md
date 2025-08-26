# SolucionesTI

Base de conocimiento interactiva para soporte técnico: permite buscar y listar soluciones a problemas frecuentes, usando **FastAPI** en el backend y **Vite + React** en el frontend. El matching se realiza con **TF‑IDF** y **similaridad del coseno** sobre un CSV de problemas/soluciones.

> **Demo**
>
> * Frontend (Netlify): [https://solucionesti.netlify.app](https://solucionesti.netlify.app)
> * Backend (Render): [https://solucionesti.onrender.com](https://solucionesti.onrender.com)

---

## ✨ Características

* Login sencillo con token Bearer (prototipo).
* Búsqueda de soluciones por texto libre (TF‑IDF + coseno).
* Vista previa con 4 soluciones aleatorias al iniciar sesión.
* Botón para **mostrar todas** las soluciones del dataset.
* CORS configurado para permitir el frontend desplegado en Netlify.

> ⚠️ **Datos sensibles**: el CSV de ejemplo incluye credenciales internas. No publicar repositorio/instancias públicas con esos datos. Sustituir por ejemplos o mover a una base de datos segura.

---

## 🛠️ Tecnologías

* **Backend**: Python 3, FastAPI, Uvicorn, Pandas, scikit‑learn
* **Frontend**: Vite + React, Fetch API, CSS
* **Despliegue**: Render (backend), Netlify (frontend)
---

## 🤝 Contribuciones

1. Hacer fork y rama feature: `feature/nueva-funcionalidad`.
2. Pull Request con descripción y evidencias.