import os
import logging
import sys
from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Get configuration from environment variables
agent_storage: str = os.getenv("AGENT_STORAGE", "tmp/agents.db")
groq_api_key: str = os.getenv("GROQ_API_KEY", "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")
port: int = int(os.getenv("PORT", "8080"))

logger.info(f"Starting application on port {port}")
logger.info(f"Agent storage: {agent_storage}")

# Ensure the tmp directory exists
os.makedirs("tmp", exist_ok=True)
logger.info("Created tmp directory")

# Ensure the tmp directory exists
os.makedirs("tmp", exist_ok=True)
logger.info("Created tmp directory")

logger.info("Creating web agent...")
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

logger.info("Creating finance agent...")
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

logger.info("Creating playground app...")
app = Playground(agents=[web_agent, finance_agent]).get_app()
logger.info("Playground app created successfully")

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
    try:
        logger.info("Starting uvicorn server...")
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port, 
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)