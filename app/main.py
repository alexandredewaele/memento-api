from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import auth, entries
import time
import logging

logger = logging.getLogger(__name__)

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
    logger.info("CORS allowed origins: %s", settings.allowed_origins_list)
    retries = 5
    for attempt in range(1, retries + 1):
        try:
            init_db()
            logger.info("Database initialised successfully.")
            return
        except Exception as e:
            logger.warning(f"DB init attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(2)
            else:
                logger.error("Could not initialise database after %d attempts.", retries)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
