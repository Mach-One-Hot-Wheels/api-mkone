from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func, text
from typing import List
from sqlalchemy.orm import Session
from src.database import get_session
from src.hotwheels.models import Hotwheels
from src.hotwheels.schemas import HotwheelsResponse, HotwheelsSearchResponse, PaginatedResponse, PaginationMeta
import uuid
import math

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

@router.get("/search/", response_model=PaginatedResponse[HotwheelsSearchResponse])
def search_hotwheels(
    query: str = Query(None, min_length=2, description="Search query for model name"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    similarity_threshold: float = Query(0.3, ge=0.1, le=0.9, description="Similarity threshold for fuzzy search"),
    session: Session = Depends(get_session)
):
    """
    Search for Hotwheels models by name with typo tolerance.
    Performs a case-insensitive search with trigram similarity.
    Supports pagination with page and page_size parameters.
    Returns both results and pagination metadata.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Search query is required")
    
    # Calculate offset from page and page_size
    skip = (page - 1) * page_size
    
    # Ensure pg_trgm extension is enabled (this should be done during DB setup,
    # but we'll make sure it's available for our query)
    try:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        session.commit()
        
        # Get total count for pagination metadata
        similarity_condition = func.similarity(Hotwheels.model_name, query) > similarity_threshold
        count_query = select(func.count()).select_from(Hotwheels).where(similarity_condition)
        total_items = session.execute(count_query).scalar() or 0
        
        # Query with pagination
        stmt = select(Hotwheels).where(
            similarity_condition
        ).order_by(
            func.similarity(Hotwheels.model_name, query).desc()
        ).offset(skip).limit(page_size)
        
        results = session.execute(stmt).scalars().all()
        
        if not results and total_items == 0:
            # If no results with similarity, try a fallback with ILIKE for partial matches
            search_pattern = f"%{query}%"
            fallback_condition = Hotwheels.model_name.ilike(search_pattern)
            
            # Get total count for fallback
            count_query = select(func.count()).select_from(Hotwheels).where(fallback_condition)
            total_items = session.execute(count_query).scalar() or 0
            
            fallback_stmt = select(Hotwheels).where(
                fallback_condition
            ).offset(skip).limit(page_size)
            
            results = session.execute(fallback_stmt).scalars().all()
    except Exception:
        # Fallback if pg_trgm is not available
        search_pattern = f"%{query}%"
        fallback_condition = Hotwheels.model_name.ilike(search_pattern)
        
        # Get total count
        count_query = select(func.count()).select_from(Hotwheels).where(fallback_condition)
        total_items = session.execute(count_query).scalar() or 0
        
        stmt = select(Hotwheels).where(
            fallback_condition
        ).offset(skip).limit(page_size)
        
        results = session.execute(stmt).scalars().all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No Hotwheels models found matching the search criteria")
    
    # Calculate pagination metadata
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 0
    has_next = page < total_pages
    has_prev = page > 1
    
    # Create pagination metadata
    meta = PaginationMeta(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        page_size=page_size,
        has_next=has_next,
        has_prev=has_prev
    )
    
    # Return paginated response
    return PaginatedResponse(items=results, meta=meta)