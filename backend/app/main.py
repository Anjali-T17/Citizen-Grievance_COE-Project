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
    analytics,
    experiments,
    stakeholders
)

app = FastAPI(
    title="Citizen Grievance Role-Aware Feature Discovery Assistant API",
    version="3.0.0 (100% Complete System)",
    description="Backend REST API for Multilingual Grievances, Role-Aware Discovery Assistant, RBAC Enforcement, Experiments, and Analytics."
)

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
app.include_router(experiments.router)
app.include_router(stakeholders.router)

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
        "phase": "Phase 1, Phase 2 & Phase 3 Complete (100% Full Project)",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
