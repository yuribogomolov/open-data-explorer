import asyncio
from typing import List, Dict, Set
from open_data_explorer.socrata.search_result_model import SearchApiResponse, Result
import aiohttp


class AsyncSearcher:
    def __init__(self, base_url: str):
        """Initialize the AsyncSearcher with a base URL.

        Args:
            base_url (str): The base URL for the search API.
        """
        self.base_url = base_url

    async def fetch_query(self, session: aiohttp.ClientSession, query: str) -> SearchApiResponse:
        """Fetch results for a single query asynchronously.

        Args:
            session (aiohttp.ClientSession): The HTTP session for making requests.
            query (str): The search query string.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        url = f"{self.base_url}?q={query.replace(' ', '%20')}"
        async with session.get(url) as response:
            response = await response.json()
            return SearchApiResponse(**response)

    async def fetch_queries(self, queries: List[str]) -> List[SearchApiResponse]:
        """Fetch results for a list of queries concurrently.

        Args:
            queries (List[str]): A list of search query strings.

        Returns:
            List[Dict[str, Any]]: A list of JSON responses from the API.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_query(session, query) for query in queries]
            return await asyncio.gather(*tasks)

    def get_search_results(self, queries: List[str]) -> List[Result]:
        """Synchronous wrapper to run queries asynchronously and de-duplicate results.

        Args:
            queries (List[str]): A list of search query strings.

        Returns:
            List[Result]: A de-duplicated list of Result objects.
        """
        responses = asyncio.run(self.fetch_queries(queries))
        merged_results = []
        seen_ids: Set[str] = set()

        for response in responses:
            for result in response.results:
                if len(result.resource.columns_name) > 0:
                    resource_id = result.resource.id
                    if resource_id not in seen_ids:
                        seen_ids.add(resource_id)
                        merged_results.append(result)

        return merged_results
