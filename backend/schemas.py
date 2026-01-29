from pydantic import BaseModel, Field
from typing import Optional

class PasteCreate(BaseModel):
    content: str = Field(min_length=1)
    ttl_seconds: Optional[int] = Field(default=None, ge=1)
    max_views: Optional[int] = Field(default=None, ge=1)

class PasteResponse(BaseModel):
    id: str
    url: str

class PasteFetchResponse(BaseModel):
    content: str
    remaining_views: Optional[int]
    expires_at: Optional[str]
