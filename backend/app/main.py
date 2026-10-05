from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.seed import seed_database
from app.routes import (
    auth,
    departments,
    complaints,
    routing,
    escalations,
    analytics,
    experiments,
    stakeholders,
    overrides,
    features,
    recommendations
)

# Ensure all database tables exist and are seeded immediately
Base.metadata.create_all(bind=engine)
_init_db = SessionLocal()
try:
    seed_database(_init_db)
finally:
    _init_db.close()


app = FastAPI(
    title="Citizen Grievance Routing Tool API (Intent Detection, Department Mandates, Escalation)",
    version="1.0.0 (35% Milestone & Full System Verified)",
    description="Backend REST API for Multilingual Citizen Grievance Intent Detection, Department Mandates Routing, Escalations, and Analytics."
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
app.include_router(departments.router)
app.include_router(complaints.router)
app.include_router(routing.router)
app.include_router(escalations.router)
app.include_router(overrides.router)
app.include_router(analytics.router)
app.include_router(experiments.router)
app.include_router(stakeholders.router)
app.include_router(features.router)
app.include_router(recommendations.router)


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
        "service": "Citizen Grievance Routing Tool API (Intent Detection, Department Mandates, Escalation)",
        "milestone": "Review 1 (35% Milestone Verified)",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
