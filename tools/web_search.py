from typing import Any, Optional
from smolagents.tools import Tool
import duckduckgo_search
import time

class DuckDuckGoSearchTool(Tool):
    name = "web_search"
    description = "Performs a duckduckgo web search based on your query (think a Google search) then returns the top search results."
    inputs = {'query': {'type': 'string', 'description': 'The search query to perform.'}}
    output_type = "string"

    def __init__(self, max_results=10, max_retries=3, retry_delay=4, **kwargs):
        super().__init__()
        self.max_results = max_results
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        try:
            from duckduckgo_search import DDGS
        except ImportError as e:
            raise ImportError(
                "You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`."
            ) from e
        self.ddgs = DDGS(**kwargs)

    def forward(self, query: str) -> str:
        last_error = None
        for attempt in range(self.max_retries):
            try:
                results = self.ddgs.text(query, max_results=self.max_results)
                if not results:
                    return f"No search results found for '{query}'. Try rephrasing the query."
                postprocessed_results = [f"[{result['title']}]({result['href']})\n{result['body']}" for result in results]
                return "## Search Results\n\n" + "\n\n".join(postprocessed_results)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        # All retries failed (likely rate-limited) — return a message instead of raising,
        # so the agent can recover gracefully instead of crashing the whole step.
        return (
            f"Web search is temporarily unavailable, likely due to DuckDuckGo rate-limiting "
            f"(error: {last_error}). Answer from what you already know if possible, and let the "
            f"user know live web results weren't available right now."
        )
