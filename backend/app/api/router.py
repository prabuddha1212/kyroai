from fastapi import APIRouter
from app.api.products import router as products_router
from app.api.waitlist import router as waitlist_router
from app.api.analytics import router as analytics_router
from app.api.owner import router as owner_router

api_router = APIRouter(prefix="/api")

api_router.include_router(products_router)
api_router.include_router(waitlist_router)
api_router.include_router(analytics_router)
api_router.include_router(owner_router)
