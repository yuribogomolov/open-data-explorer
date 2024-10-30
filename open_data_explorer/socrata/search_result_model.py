from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class PageViews(BaseModel):
    page_views_last_week: int
    page_views_last_month: int
    page_views_total: int
    page_views_last_week_log: float
    page_views_last_month_log: float
    page_views_total_log: float


class Resource(BaseModel):
    name: str
    id: str
    resource_name: Optional[str] = None
    parent_fxf: List[Any]
    description: str
    attribution: Optional[str] = None
    attribution_link: Optional[str] = None
    contact_email: Optional[str] = None
    type: str
    updatedAt: Optional[datetime] = None
    createdAt: Optional[datetime] = None
    metadata_updated_at: Optional[datetime] = None
    data_updated_at: Optional[datetime] = None
    page_views: PageViews
    columns_name: List[str]
    columns_field_name: List[str]
    columns_datatype: List[str]
    columns_description: List[str]
    columns_format: List[Dict[str, Any]]
    download_count: int
    provenance: str
    lens_view_type: str
    lens_display_type: str
    locked: bool
    blob_mime_type: Optional[str] = None
    hide_from_data_json: bool
    publication_date: Optional[datetime] = None

    @field_validator('updatedAt', 'createdAt', 'metadata_updated_at', 'data_updated_at', 'publication_date',
                     mode='before')
    def parse_datetime(cls, value):
        if value is None:
            return None
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return None


class Classification(BaseModel):
    categories: List[str]
    tags: List[str]
    domain_category: Optional[str] = None
    domain_tags: List[str]
    domain_metadata: List[Dict[str, Any]]


class Metadata(BaseModel):
    domain: str
    license: Optional[str] = None


class User(BaseModel):
    id: str
    user_type: str
    display_name: str


class Result(BaseModel):
    resource: Resource
    classification: Classification
    metadata: Metadata
    permalink: str
    link: str
    owner: User
    creator: User


class Timings(BaseModel):
    serviceMillis: int
    searchMillis: List[int]


class SearchApiResponse(BaseModel):
    results: List[Result]
    resultSetSize: int
    timings: Timings
    warnings: List[Any] = Field(default_factory=list)
