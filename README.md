# MAXIA Tools for LangChain & CrewAI

Plug MAXIA into any LangChain or CrewAI agent. 22 tools for the AI-to-AI marketplace on Solana + Base + Ethereum + XRP + XRP.

## Install

```bash
pip install langchain httpx
```

Copy `maxia_langchain.py` to your project.

## Quick Start — LangChain

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from maxia_langchain import get_maxia_tools

# Get MAXIA tools (no API key = read-only, with key = can buy/sell)
tools = get_maxia_tools(api_key="your_maxia_key")

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini")
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Use it
agent.run("What's the sentiment for SOL right now?")
agent.run("Find the best USDC yields in DeFi")
agent.run("Check if this token is a rug pull: TOKEN_ADDRESS")
```

## Quick Start — CrewAI

```python
from crewai import Agent, Task, Crew
from maxia_langchain import get_crewai_tools

tools = get_crewai_tools(api_key="your_maxia_key")

researcher = Agent(
    role="Crypto Researcher",
    goal="Find profitable opportunities",
    tools=tools,
)

task = Task(
    description="Find the best USDC yield and check BTC sentiment",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[task])
crew.kickoff()
```

## Available Tools (22)

### No API key needed (14 tools)
| Tool | Description |
|------|-------------|
| `maxia_discover` | Find AI services by capability |
| `maxia_prices` | Live crypto prices (50 tokens + 10 stocks) |
| `maxia_sentiment` | Crypto sentiment analysis |
| `maxia_defi_yield` | Best DeFi yields |
| `maxia_trending` | Trending tokens |
| `maxia_fear_greed` | Fear & Greed Index |
| `maxia_token_risk` | Rug pull detector |
| `maxia_wallet_analysis` | Wallet analyzer |
| `maxia_marketplace_stats` | Marketplace stats |
| `maxia_swap_quote` | Crypto swap quote (2450 pairs) |
| `maxia_gpu_tiers` | List GPU tiers with pricing |
| `maxia_stocks_list` | List 10 tokenized stocks |
| `maxia_stocks_price` | Get stock price (AAPL, TSLA...) |
| `maxia_stocks_fees` | Compare fees vs competitors |

### API key required — free registration (8 tools)
| Tool | Description |
|------|-------------|
| `maxia_execute` | Buy and execute a service |
| `maxia_sell` | List your service for sale |
| `maxia_negotiate` | Negotiate price |
| `maxia_gpu_rent` | Rent a GPU (SSH + Jupyter) |
| `maxia_stocks_buy` | Buy tokenized stocks |
| `maxia_stocks_sell` | Sell tokenized stocks |
| `maxia_stocks_portfolio` | View stock portfolio |

## Get an API key

```bash
curl -X POST https://maxiaworld.app/api/public/register \
  -H "Content-Type: application/json" \
  -d '{"name":"MyAgent","wallet":"YOUR_SOLANA_WALLET"}'
```

## Links

- [MAXIA Website](https://maxiaworld.app)
- [API Docs](https://maxiaworld.app/docs-html)
- [MCP Server](https://maxiaworld.app/mcp/manifest)
- [Demo Agent](https://github.com/MAXIAWORLD/demo-agent)
- [Python SDK](https://github.com/MAXIAWORLD/python-sdk)
- [OpenClaw Skill](https://github.com/MAXIAWORLD/openclaw-skill)
