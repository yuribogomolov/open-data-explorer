from abc import ABC, abstractmethod
from open_data_explorer.models.search_queries import DatasetSelectionModel, SearchQueriesModel
from open_data_explorer.socrata.search_result_model import Result
from typing import Any


class BaseQuery(ABC):
    @property
    @abstractmethod
    def model_class(self):
        """Query response model class"""
        pass

    @property
    @abstractmethod
    def prompt_template(self) -> str:
        """Template file name"""
        pass

    @property
    @abstractmethod
    def template_context(self) -> dict[str, Any]:
        """Template file name"""
        pass


class SearchQuery(BaseQuery):

    def __init__(self, search_query: str):
        self.search_query = search_query

    @property
    def model_class(self):
        """Query response model class"""
        return SearchQueriesModel

    @property
    def prompt_template(self) -> str:
        """Template file name"""
        return "search_queries.j2"

    @property
    def template_context(self) -> dict[str, Any]:
        """Template file name"""
        return {
            "user_query": self.search_query
        }


class DataSelectionQuery(BaseQuery):

    def __init__(self, search_query: str, datasets: list[Result]):
        self.search_query = search_query
        self.datasets = datasets

    @property
    def model_class(self):
        """Query response model class"""
        return DatasetSelectionModel

    @property
    def prompt_template(self) -> str:
        """Template file name"""
        return "dataset_selection.j2"

    @property
    def template_context(self) -> dict[str, Any]:
        """Template file name"""
        return {
            "user_query": self.search_query,
            "datasets": self.datasets
        }
