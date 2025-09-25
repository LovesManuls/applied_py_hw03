from sqlalchemy import Table, Column, Integer, DateTime, MetaData, String
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

# id = Column(UUID, primary_key=True, index=True)

links = Table(
    "links",
    metadata,
    Column("link_id", Integer, primary_key=True),
    Column("user_id", UUID),
    Column("short_code", String),
    Column("orig_url", String),
    Column("created_time", DateTime, nullable=False),
    Column("expired_time", DateTime, nullable=False),
    Column("last_usage_time", DateTime, nullable=False),
    Column("usage_cnt", Integer),
)

# users = Table(
#     "users",
#     metadata,
#     Column("user_id", Integer, primary_key=True),
# )