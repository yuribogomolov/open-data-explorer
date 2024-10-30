import asyncio
from typing import List, Dict, Any
from open_data_explorer.socrata.search_result_model import SearchApiResponse
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

    def get_search_results(self, queries: List[str]) -> List[SearchApiResponse]:
        """Synchronous wrapper to run the asynchronous fetch_queries method.

        Args:
            queries (List[str]): A list of search query strings.

        Returns:
            List[Dict[str, Any]]: A list of JSON responses from the API.
        """
        return asyncio.run(self.fetch_queries(queries))
