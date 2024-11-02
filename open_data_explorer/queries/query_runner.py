from openai import OpenAI
from pydantic import BaseModel
from open_data_explorer.queries.query import BaseQuery, SearchQuery, DataSelectionQuery
from open_data_explorer.models.search_queries import DatasetSelectionModel, SearchQueriesModel
from open_data_explorer.socrata.searcher import AsyncSearcher
from open_data_explorer.socrata.search_result_model import Resource, Result

from jinja2 import Environment, PackageLoader, Template

BASE_URL = "https://api.us.socrata.com/api/catalog/v1"


def find_datasets(datasets: list[Result], selected_resource_ids: list[str]) -> list[Result]:
    resources = []

    for dataset in datasets:
        if dataset.resource.id in selected_resource_ids:
            resources.append(dataset)

    return resources


class QueryRunner:

    def __init__(self):
        self.client = OpenAI()
        self.searcher = AsyncSearcher(base_url=BASE_URL)

    def run_query(self, query: BaseQuery) -> BaseModel:
        prompt = PromptGenerator.render_template(query.prompt_template, query.template_context)
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
            ],
            response_format=query.model_class,
        )
        return completion.choices[0].message.parsed

    def generate_search_queries(self, query: str) -> SearchQueriesModel:
        search_query = SearchQuery(query)
        search_queries = self.run_query(search_query)
        return search_queries

    def search(self, query: str) -> list[Result]:
        search_queries = self.generate_search_queries(query)
        search_results = self.searcher.get_search_results(search_queries.search_queries)
        return search_results

    def select_datasets(self, query: str) -> list[Result]:
        datasets = self.search(query)
        selection_query = DataSelectionQuery(search_query=query, datasets=datasets)
        selected_datasets = self.run_query(selection_query)
        selected = find_datasets(datasets, selected_resource_ids=selected_datasets.selected_resource_ids)
        return selected


class PromptGenerator:
    @staticmethod
    def get_template(template_fname: str) -> Template:
        environment = Environment(loader=PackageLoader("open_data_explorer", package_path="prompts"))
        return environment.get_template(template_fname)

    @staticmethod
    def render_template(template_fname: str, context: dict[str, str]) -> str:
        template = PromptGenerator.get_template(template_fname)
        prompt_str = template.render(context)
        return prompt_str
