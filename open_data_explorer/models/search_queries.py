from pydantic import BaseModel


class SearchQueriesModel(BaseModel):
    search_queries: list[str]


class DatasetSelectionModel(BaseModel):
    selected_resource_ids: list[str]
