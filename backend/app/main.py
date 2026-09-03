from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.seed import seed_database
from app.routes import (
    auth,
    organisations,
    roles,
    complaints,
    features,
    recommendations,
    overrides,
    analytics
)

app = FastAPI(
    title="Citizen Grievance Role-Aware Feature Discovery Assistant API",
    version="1.0.0 (Phase 1 / Review 1 MVP)",
    description="Backend REST API for Multilingual Grievances, Role-Aware Discovery Assistant, RBAC Permission Enforcement, and Analytics."
)

# Enable CORS for React frontend (Vite dev server runs on 5173 / 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(organisations.router)
app.include_router(roles.router)
app.include_router(complaints.router)
app.include_router(features.router)
app.include_router(recommendations.router)
app.include_router(overrides.router)
app.include_router(analytics.router)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Role-Aware Feature Discovery Assistant API",
        "phase": "Phase 1 - Review 1 (35% MVP)",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
