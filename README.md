# 🤖 Linear Agentic Workflow with 3 Tools

<img width="866" height="356" alt="agent" src="https://github.com/user-attachments/assets/3e506067-bee6-46d0-a8fd-91fc90256098" />

---

This project demonstrates how to build a **Linear Agentic Workflow** using **LangGraph** and **OpenAI GPT-4o models**.  
The agent intelligently uses three specialized tools follows

  1) **Wikipedia**
  2) **Stock Data**,
  3) **Python REPL** 
  
  — to perform research, data retrieval, and computation tasks in sequence.

---


Each node has a defined role:
- **LLM Node:** Understands the user query and determines the required tool.
- **Tool Node:** Executes the chosen tool and returns structured output.
- **Graph:** Orchestrates the process from start to finish.

This design makes the workflow **interpretable**, **deterministic**, and **easily extendable** to more tools or conditional logic.

---



## 🚀 Features

- 🧠 **Agentic reasoning** with OpenAI GPT-4o-mini  
- 🧩 **Three tool integration** via LangChain ToolNode  
- 🔗 **Wikipedia + Stock Data + Python REPL** in one pipeline  
- 🧾 **Readable Markdown output** using `pandas.to_markdown()`  
- ⚙️ **Linear workflow graph** built using LangGraph  
- 💡 **Easy extensibility** — add new tools or branches with minimal changes  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Language** | Python 3.9+ |
| **Framework** | [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://www.langchain.com/) |
| **Model** | OpenAI GPT-4o / GPT-4o-mini |
| **Data Handling** | pandas, tabulate |
| **Computation** | Python REPL (`langchain_experimental.utilities.PythonREPL`) |
| **Factual Search** | Wikipedia API |

---

## 🧩 Tool Descriptions

### 🪶 1. Wikipedia Tool (`wikipedia_tool`)

## 📸 Preview

<img width="1005" height="311" alt="workflow-preview" src="https://github.com/user-attachments/assets/03bdb352-60c9-4381-b821-c00a4be5feb5" />

**Purpose:**  
Fetch factual summaries from Wikipedia.

**How it works:**
- Takes a query such as “Apple Inc.” or “LangChain”.
- Searches for the most relevant Wikipedia page.
- Returns an 8-sentence factual summary.

**Example Use:**
> “Tell me about OpenAI.”  
→ Returns a concise, verified summary using the Wikipedia API.

**Dependencies:**
```bash
pip install wikipedia
```
---

### 📈 2. Stock Data Tool (`stock_data_tool`)

## 📸 Preview

<img width="1037" height="299" alt="stock" src="https://github.com/user-attachments/assets/80eeee34-ad6b-42ad-8c78-79f582bb0226" />

**Purpose:**  
Retrieve and format historical stock performance data.

**How it works:**
- Loads stock CSV files stored in the `/data` directory (e.g., `AAPL.csv`, `TSLA.csv`).
- Filters the dataset to the requested number of days (`num_days`).
- Returns a markdown-formatted table using `pandas.to_markdown()`.

**Dependencies:**  
```bash
pip install pandas tabulate


