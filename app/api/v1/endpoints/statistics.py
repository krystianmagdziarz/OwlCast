from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from app.core.security import verify_api_key
from app.api.v1.dependencies import rate_limit
from app.schemas.statistics import (
    StatisticsCreate,
    StatisticsResponse,
    StatisticsAggregation
)
from app.services.statistics import StatisticsService

router = APIRouter()

@router.post("/", status_code=201, dependencies=[Depends(rate_limit)])
async def create_statistics(
    stats: StatisticsCreate,
    _: None = Depends(verify_api_key)
) -> None:
    await StatisticsService.create_statistics(stats)

@router.get(
    "/{domain}",
    response_model=List[StatisticsResponse],
    dependencies=[Depends(rate_limit)]
)
@cache(expire=300)
async def get_domain_statistics(
    domain: str,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    _: None = Depends(verify_api_key)
) -> List[StatisticsResponse]:
    return await StatisticsService.get_domain_statistics(
        domain=domain,
        start_date=start_date,
        end_date=end_date
    )

@router.get(
    "/{domain}/aggregate",
    response_model=StatisticsAggregation,
    dependencies=[Depends(rate_limit)]
)
@cache(expire=300)
async def get_aggregated_statistics(
    domain: str,
    path: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    _: None = Depends(verify_api_key)
) -> StatisticsAggregation:
    return await StatisticsService.get_aggregated_statistics(
        domain=domain,
        path=path,
        start_date=start_date,
        end_date=end_date
    )
