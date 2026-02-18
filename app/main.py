from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import auth, entries

app = FastAPI(
    title="Memento API",
    description="Backend for the Memento journal app.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(entries.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
