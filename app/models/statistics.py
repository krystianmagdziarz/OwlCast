from datetime import datetime
from typing import Optional, Dict, Any, List
from app.db.clickhouse import clickhouse

class Statistics:
    table_name = "statistics"
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS statistics (
        id UUID DEFAULT generateUUIDv4(),
        url String,
        domain String,
        path String,
        visitor_id String,
        user_agent String,
        referrer String,
        screen_width UInt16,
        screen_height UInt16,
        language String,
        is_mobile Bool,
        scroll_depth UInt8,
        time_on_page UInt32,
        client_timestamp DateTime,
        created_at DateTime DEFAULT now(),
        date Date DEFAULT toDate(created_at)
    )
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(date)
    ORDER BY (domain, path, created_at)
    SETTINGS index_granularity = 8192
    """

    @classmethod
    def get_create_table_query(cls) -> str:
        return cls.create_table_query
    
    @classmethod
    async def create(cls, data: Dict[str, Any]) -> None:
        await clickhouse.insert_statistics(data)
    
    @classmethod
    async def get_domain_statistics(
        cls,
        domain: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return await clickhouse.get_statistics(
            domain=domain,
            start_date=start_date,
            end_date=end_date
        )
    
    @classmethod
    async def get_page_statistics(
        cls,
        domain: str,
        path: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return await clickhouse.get_statistics(
            domain=domain,
            path=path,
            start_date=start_date,
            end_date=end_date
        )
