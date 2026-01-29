from sqlalchemy import Table, Column, String, Text, Integer, DateTime
from db import metadata

pastes = Table(
    "pastes",
    metadata,
    Column("id", String, primary_key=True),
    Column("content", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=True),
    Column("max_views", Integer, nullable=True),
    Column("view_count", Integer, nullable=False, default=0),
)
