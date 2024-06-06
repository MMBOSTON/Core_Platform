from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common.database import get_db
from .chd_schemas import HealthScoreResponse
from .services import get_health_score

router = APIRouter()

@router.get("/health_scores/{customer_id}", response_model=HealthScoreResponse)
def read_health_score(customer_id: int, db: Session = Depends(get_db)):
    return get_health_score(customer_id, db)
