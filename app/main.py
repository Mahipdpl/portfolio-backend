from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import projects, skills, certifications, contact, admin, auth
from app.core.seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mahesh Portfolio API",
    description="Backend API for Mahesh Reddy's portfolio",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(certifications.router, prefix="/api/certifications", tags=["Certifications"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.on_event("startup")
def on_startup():
    seed_data()


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Mahesh Portfolio API is running 🚀"}


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "healthy"}
