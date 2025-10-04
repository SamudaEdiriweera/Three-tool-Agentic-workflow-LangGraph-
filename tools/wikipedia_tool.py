"""Tool that uses the wikipedia library to fetch summaries from Wikipedia."""

from typing import Annotated
import wikipedia
from langchain_core.tools import tool

@tool 
def wikipedia_tool(
    query: Annotated[str, "The Wikipedia search to execute to find tkey summary information."],
):
    """ use this to search Wikipedia for factual information."""
    try:
        # step 1: Search using query
        results = wikipedia.search(query)
        
        if not results:
            return "No results found on Wikipedia."
        
        # step 2. REtrieve page title
        title = results[0]
        
        # step 3. Fetch summary
        summary = wikipedia.summary(title, sentences=8, auto_suggest=False, redirect=True)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return f"Successfully executed:\nWikipedia summary: {summary}"

# Test with Apple query
company_name = "Apple Inc."
wiki_summary = wikipedia_tool.invoke(f"{company_name}")
print(wiki_summary)
