from pydantic import BaseModel


class SearchResultsModel(BaseModel):
    search_queries: list[str]
