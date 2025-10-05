from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
import getpass
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
import wikipedia
from langchain_core.tools import tool
import os
import pandas as pd
from langchain_experimental.utilities import PythonREPL

repl = PythonREPL()

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart"]
) -> str:
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. The chart should be displayed using `plt.show()`."""
    try:
        result = repl.run(code)
    except Exception as e:
        return f"Failed to execute. Error: {repr(e)}"
    return (
        "Successfully executed the Python REPL tool.\n\nPython code executed:\n"
        f"```python\n{code}\n```\n\nCode output:\n```\n{result}```"
    )

@tool
def wikipedia_tool(
    query: Annotated[str, "The Wikipedia search to execute to find key summary information."],
):
    """Use this to search Wikipedia for factual information."""
    try:
        results = wikipedia.search(query)
        if not results:
            return "No results found on Wikipedia."
        title = results[0]
        summary = wikipedia.summary(title, sentences=8, auto_suggest=False, redirect=True)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return f"Successfully executed:\nWikipedia summary: {summary}"

BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "data")

@tool
def stock_data_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company to retrieve stock performance data."],
    num_days: Annotated[int, "Number of days of stock data required."]
) -> str:
    """
    Look up stock performance data for companies from a CSV (one CSV per ticker).
    Example tickers: AAPL, AMZN, META, MSFT, TSLA
    """
    file_path = f"{DATA_PATH}/{company_ticker.upper()}.csv"
    if not os.path.exists(file_path):
        return f"Sorry, but data for company {company_ticker} is not available. Try Apple, Amazon, Meta, Microsoft, Tesla."

    stock_df = pd.read_csv(file_path, index_col="Date", parse_dates=True)

    # DO NOT overwrite the index with booleans (bug fix)
    # stock_df.index = stock_df.index.duplicated

    max_num_days = (stock_df.index.max() - stock_df.index.min()).days
    if num_days > max_num_days:
        return "Sorry, but this time period exceeds the data available. Please reduce it to continue."

    final_date = stock_df.index.max()
    filtered_df = stock_df[stock_df.index > (final_date - pd.Timedelta(days=num_days))]

    return (
        f"Successfully executed the stock performance data retrieval tool to retrieve the last *{num_days} days* "
        f"of data for company **{company_ticker}**:\n\n{filtered_df.to_markdown()}"
    )

# ---- 1. Set up API Key securely ----
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# ---- Graph State ----
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Tools list
tools = [wikipedia_tool, stock_data_tool, python_repl_tool]

# LLM with tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def llm_node(state: State):
    msgs = state.get("messages", [])
    return {"messages": [llm_with_tools.invoke(msgs)]}

# Nodes
graph_builder.add_node("llm", llm_node)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tool", tool_node)

# Linear edges
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", "tool")
graph_builder.add_edge("tool", END)

graph = graph_builder.compile()

# Pretty print for streaming
def pretty_print_chunk(chunk: dict):
    # chunk like {"llm": {"messages":[...]}} or {"tool": {"messages":[...]}}
    for node_name, payload in chunk.items():
        if isinstance(payload, dict) and "messages" in payload:
            for m in payload["messages"]:
                # Support both LC message objects and dicts
                role = getattr(m, "type", None) or getattr(m, "role", "unknown")
                content = getattr(m, "content", None)
                if content is None and isinstance(m, dict):
                    content = m.get("content")
                print(f"[{node_name}] {role}: {content}")

# --- Run ---
for step in graph.stream({"messages": [{"role": "user", "content": "Tell me about Apple Inc and its stock performance data of last 4 days"}]}):
    pretty_print_chunk(step)
