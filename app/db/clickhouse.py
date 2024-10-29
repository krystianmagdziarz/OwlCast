from typing import Any, Dict, List
import clickhouse_connect
from clickhouse_connect.driver.client import Client

from app.core.config import settings
from app.models.statistics import Statistics

class ClickHouseClient:
    def __init__(self):
        self.client: Client = clickhouse_connect.get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            username=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DB
        )
        self.init_database()
    
    def init_database(self) -> None:
        self.client.command(f"CREATE DATABASE IF NOT EXISTS {settings.CLICKHOUSE_DB}")
        self.client.command(Statistics.get_create_table_query())
    
    async def insert_statistics(self, data: Dict[str, Any]) -> None:
        query = f"""
        INSERT INTO {Statistics.table_name} 
        (url, domain, path, visitor_id, user_agent, referrer, 
         screen_width, screen_height, language, is_mobile, 
         scroll_depth, time_on_page, client_timestamp)
        VALUES
        """
        self.client.command(query, parameters=data)
    
    async def get_statistics(
        self, 
        domain: str, 
        path: str = None, 
        start_date: str = None, 
        end_date: str = None
    ) -> List[Dict[str, Any]]:
        conditions = [f"domain = '{domain}'"]
        if path:
            conditions.append(f"path = '{path}'")
        if start_date:
            conditions.append(f"date >= '{start_date}'")
        if end_date:
            conditions.append(f"date <= '{end_date}'")
            
        where_clause = " AND ".join(conditions)
        
        query = f"""
        SELECT *
        FROM {Statistics.table_name}
        WHERE {where_clause}
        ORDER BY created_at DESC
        """
        
        result = self.client.query(query)
        return result.named_results()

clickhouse = ClickHouseClient()
