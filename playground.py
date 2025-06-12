import os
import logging
from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment variables
agent_storage: str = os.getenv("AGENT_STORAGE", "tmp/agents.db")
groq_api_key: str = os.getenv("GROQ_API_KEY", "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")
port: int = int(os.getenv("PORT", "8080"))  # Changed default to 8080 for Cloud Run

logger.info(f"Starting application on port {port}")

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

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "port": port}

# Add root endpoint
@app.get("/")
async def root():
    return {"message": "Agent Playground is running", "port": port}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")