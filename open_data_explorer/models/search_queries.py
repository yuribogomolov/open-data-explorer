from pydantic import BaseModel


class SearchQueriesModel(BaseModel):
    search_queries: list[str]
