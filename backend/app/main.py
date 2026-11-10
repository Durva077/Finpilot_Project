
from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import router as auth_router
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Smart Personal Finance and Expense Tracker"
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to FinPilot API",
        "version": settings.APP_VERSION
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
