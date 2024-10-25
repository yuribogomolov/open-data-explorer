from openai import OpenAI
from pydantic import BaseModel
from open_data_explorer.queries.query import BaseQuery, SearchQuery
from open_data_explorer.models.search_results import SearchResultsModel

from jinja2 import Environment, PackageLoader, Template


class QueryRunner:

    def __init__(self):
        self.client = OpenAI()

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

    def search(self, query: str) -> SearchResultsModel:
        search_query = SearchQuery(query)
        search_queries = self.run_query(search_query)
        return search_queries


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
