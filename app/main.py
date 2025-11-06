# app/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import (
    auth_routes,
    courses_routes,
    admin_routes,
    admin_notifications_routes,
    incidents_routes,
    sensors_routes,
    allocation_routes  # ✅ Added allocation routes
)

# ============================================================
# FASTAPI APP INITIALIZATION
# ============================================================
app = FastAPI(
    title="AIDRP - Python Backend Service",
    version="0.1.0",
    description="AI Disaster Response and Prediction Platform API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================================
# CORS CONFIGURATION
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# DATABASE INITIALIZATION
# ============================================================
def init_db():
    """Create all database tables if they do not exist."""
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("✅ Database tables created successfully")
    except Exception as e:
        logging.error(f"❌ Database initialization failed: {e}")
        raise

# ============================================================
# ROUTES INITIALIZATION
# ============================================================
def init_routes():
    """Attach all route modules to FastAPI app."""
    try:
        app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
        app.include_router(courses_routes.router, prefix="/courses", tags=["Courses"])
        app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
        app.include_router(admin_notifications_routes.router, prefix="/admin/notifications", tags=["Admin Notifications"])
        app.include_router(incidents_routes.router, prefix="/incidents", tags=["Incidents"])
        app.include_router(sensors_routes.router, prefix="/sensors", tags=["Sensors"])
        app.include_router(allocation_routes.router, prefix="/allocation", tags=["Allocation"])  # ✅ Allocation route
        logging.info("✅ Routes initialized successfully")
    except Exception as e:
        logging.error(f"❌ Route initialization failed: {e}")
        raise

# ============================================================
# HEALTH CHECK ENDPOINTS
# ============================================================
@app.get("/", tags=["Health"])
async def read_root():
    """Root endpoint for API health check."""
    return {
        "message": "🚀 AIDRP Python API is running successfully!",
        "version": "0.1.0",
        "docs_url": "/docs"
    }

@app.get("/status", tags=["Health"])
async def status_check():
    """Detailed service status endpoint."""
    return {
        "status": "ok",
        "service": "AIDRP Backend",
        "database": "connected",
        "version": "0.1.0"
    }

# ============================================================
# APPLICATION STARTUP & SHUTDOWN EVENTS
# ============================================================
@app.on_event("startup")
async def startup_event():
    """Initialize app components on startup."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logging.info("🚀 Starting AIDRP FastAPI service...")
    init_db()
    init_routes()
    logging.info("✅ AIDRP FastAPI service started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Perform cleanup on application shutdown."""
    logging.info("⏹️ Shutting down AIDRP FastAPI service")

# ============================================================
# LOCAL DEVELOPMENT ENTRY POINT
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
