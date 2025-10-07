from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.analytics_schema import AnalyticsResponse
from app.services.analytics_service import AnalyticsService
from infrastructure.database.database_session import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "",
    response_model=AnalyticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get sales analytics and production recommendations"
)
def get_production_analytics(db: Session = Depends(get_db)):
    return AnalyticsService(db).get_production_recommendations()
