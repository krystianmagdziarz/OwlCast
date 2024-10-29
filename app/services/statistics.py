from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import HTTPException

from app.models.statistics import Statistics
from app.schemas.statistics import StatisticsCreate, StatisticsAggregation
from app.helpers import get_domain, get_path

class StatisticsService:
    @staticmethod
    async def create_statistics(stats: StatisticsCreate) -> None:
        try:
            data = stats.model_dump()
            data["domain"] = get_domain(str(stats.url))
            data["path"] = get_path(str(stats.url))
            
            await Statistics.create(data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create statistics: {str(e)}"
            )
    
    @staticmethod
    async def get_domain_statistics(
        domain: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        try:
            return await Statistics.get_domain_statistics(
                domain=domain,
                start_date=start_date.isoformat() if start_date else None,
                end_date=end_date.isoformat() if end_date else None
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get domain statistics: {str(e)}"
            )
    
    @staticmethod
    async def get_aggregated_statistics(
        domain: str,
        path: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> StatisticsAggregation:
        try:
            stats = await Statistics.get_page_statistics(
                domain=domain,
                path=path,
                start_date=start_date.isoformat() if start_date else None,
                end_date=end_date.isoformat() if end_date else None
            )
            
            if not stats:
                return StatisticsAggregation(
                    total_views=0,
                    unique_visitors=0,
                    avg_time_on_page=0.0,
                    bounce_rate=0.0,
                    avg_scroll_depth=0.0
                )
            
            unique_visitors = len(set(s["visitor_id"] for s in stats))
            total_views = len(stats)
            avg_time = sum(s["time_on_page"] for s in stats) / total_views
            avg_scroll = sum(s["scroll_depth"] for s in stats) / total_views
            
            # Bounce rate calculation (sessions with only one page view)
            visitor_sessions = {}
            for s in stats:
                visitor_sessions.setdefault(s["visitor_id"], []).append(s)
            bounced = sum(1 for sessions in visitor_sessions.values() if len(sessions) == 1)
            bounce_rate = (bounced / len(visitor_sessions)) * 100 if visitor_sessions else 0
            
            return StatisticsAggregation(
                total_views=total_views,
                unique_visitors=unique_visitors,
                avg_time_on_page=avg_time,
                bounce_rate=bounce_rate,
                avg_scroll_depth=avg_scroll
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get aggregated statistics: {str(e)}"
            )
