from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, constr

class StatisticsBase(BaseModel):
    url: HttpUrl
    user_agent: str
    referrer: Optional[HttpUrl] = None
    screen_width: int
    screen_height: int
    language: constr(max_length=10)
    is_mobile: bool
    scroll_depth: int
    time_on_page: int  # in seconds
    
class StatisticsCreate(StatisticsBase):
    client_timestamp: datetime
    visitor_id: str
    
class StatisticsResponse(StatisticsBase):
    id: str
    domain: str
    path: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class StatisticsAggregation(BaseModel):
    total_views: int
    unique_visitors: int
    avg_time_on_page: float
    bounce_rate: float
    avg_scroll_depth: float
