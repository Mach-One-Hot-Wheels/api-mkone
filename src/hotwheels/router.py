from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.database import get_session
from src.hotwheels.models import Hotwheels
from src.hotwheels.schemas import HotwheelsResponse
import uuid

router = APIRouter()

@router.get("/{id}", response_model=HotwheelsResponse)
def get_specific_hotwheels(id: str, session: Session = Depends(get_session)):
    try:
        uuid_id = uuid.UUID(id)
        hotwheels = session.execute(select(Hotwheels).where(Hotwheels.id == uuid_id)).scalars().first()
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido. Formato esperado: UUID.")
    
    if hotwheels:
        return hotwheels
    raise HTTPException(status_code=404, detail="Hotwheels não encontrado.")