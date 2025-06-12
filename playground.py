import os
from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

# Get configuration from environment variables
agent_storage: str = os.getenv("AGENT_STORAGE", "tmp/agents.db")
groq_api_key: str = os.getenv("GROQ_API_KEY", "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")
port: int = int(os.getenv("PORT", "7777"))

web_agent = Agent(
    name="William Cabrera",
    model=Groq(
        id="llama3-70b-8192",
        api_key=groq_api_key,
    ),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=Groq(
        id="llama3-70b-8192",
        api_key=groq_api_key,
    ),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

app = Playground(agents=[web_agent, finance_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=False, port=port, host="0.0.0.0")