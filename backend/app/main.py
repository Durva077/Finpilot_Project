
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.budgets import router as budgets_router
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.transactions import router as transactions_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Smart Personal Finance and Expense Tracker"
)

# Allow the React frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(budgets_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to FinPilot API",
        "version": settings.APP_VERSION
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
