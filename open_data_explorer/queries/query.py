from abc import ABC, abstractmethod
from open_data_explorer.models.search_results import SearchResultsModel


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
    def template_context(self) -> dict[str, str]:
        """Template file name"""
        pass


class SearchQuery(BaseQuery):

    def __init__(self, search_query: str):
        self.search_query = search_query

    @property
    def model_class(self):
        """Query response model class"""
        return SearchResultsModel

    @property
    def prompt_template(self) -> str:
        """Template file name"""
        return "search_queries.j2"

    @property
    def template_context(self) -> dict[str, str]:
        """Template file name"""
        return {
            "user_query": self.search_query
        }
