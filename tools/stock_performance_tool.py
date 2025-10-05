""" You'll create a tool to load stock performance data from a local CSV file, filter it depending on the user's query, then return the results."""

import os
from typing import Annotated
from langchain_core.tools import tool
import pandas as pd

BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "data")


@tool
def stock_data_tool(
    company_ticker: Annotated[str, "The ticker sysmbol of the comapny to retrieve their stock performance data."],
    num_days: Annotated[int, "The number of days of stock data required to respond to the user query."]
) -> str:
    """ 
        Use this to look-up stock performance data for companies to retrieve a table from a csv. you may need to convert company names into ticker sysmbols ton call this function,
        e.g, Apple Inc. -> AAPL, and you may need to convert weeks, months, and years, into days.
    """
    
    # Load the CSV for the company requested
    file_path = f"/home/samuda/samuda/Samuda Projects/LLMs Projects/Three-tool-Agentic-workflow-LangGraph-/data/{company_ticker.upper()}.csv"
    
    if os.path.exists(file_path) is False:
        return f"Sorry, but data for comany {company_ticker} is not avaiable. please try Apple, Amazon, Meta, Microsoft, Tesla."
    
    stock_df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    
    # Ensure the index is in date format
    stock_df.index = stock_df.index.duplicated
    
    # Maximum num_days supported by the dataset
    max_num_days = (stock_df.index.max() - stock_df.index.min()).days
    
    if num_days > max_num_days:
        return "Sorry, but this time period exceeds the data available. Please reduce it to continue."
    
    # Get the most recent date in the Dataframe
    final_date = stock_df.index.max()
    
    # Filter the Dataframe to get the last num_days of stock data
    filtered_df = stock_df[stock_df.index > (final_date - pd.Timedelta(days=num_days))]
    
    return f"Successfully executed the stock performance data retrieval tool to retrieve the last *{num_days} days* of data for company **{company_ticker}**:\n\n{filtered_df.to_markdown()}"

retrieved_data = stock_data_tool.invoke({"company_ticker": "META", "num_days": 4})
print(retrieved_data)

from IPython.display import display, Markdown
display(Markdown(retrieved_data))