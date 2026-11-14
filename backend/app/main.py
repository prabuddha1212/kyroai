from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.router import api_router
from app.db.supabase_client import test_connection

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="StoreLab API for physical hardware concept testing and waitlist validation."
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "StoreLab API is running", "version": settings.VERSION}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Include central API router (/api/...)
app.include_router(api_router)

# Supabase connectivity test
@app.get("/supabase-test")
async def supabase_test():
    """
    Verify that the Supabase client can talk to your project.
    Returns a few rows (or an empty list) from the `products` table.
    """
    try:
        data = test_connection()
        return {"connected": True, "sample_data": data}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
