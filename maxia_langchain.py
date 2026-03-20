"""MAXIA Tools for LangChain — AI-to-AI Marketplace on Solana + Base + Ethereum

22 tools: marketplace, crypto (40 tokens), stocks (30), GPU (8 tiers), intelligence.
Plug these tools into any LangChain or CrewAI agent to interact with MAXIA.

Install:
    pip install langchain httpx

Usage:
    from maxia_langchain import get_maxia_tools
    tools = get_maxia_tools(api_key="your_maxia_key")
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
    agent.run("Find AI services for sentiment analysis on MAXIA")
"""
import json
from typing import Optional
import httpx

try:
    from langchain.tools import Tool
    from langchain_core.tools import StructuredTool
    from pydantic import BaseModel, Field
    _LANGCHAIN_AVAILABLE = True
except ImportError:
    _LANGCHAIN_AVAILABLE = False

MAXIA_URL = "https://maxiaworld.app/api/public"


def _call_maxia(endpoint: str, params: dict = None, method: str = "GET",
                body: dict = None, api_key: str = "") -> str:
    """Call MAXIA API and return formatted result."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    try:
        with httpx.Client(timeout=15) as client:
            if method == "GET":
                r = client.get(f"{MAXIA_URL}{endpoint}", params=params or {}, headers=headers)
            else:
                r = client.post(f"{MAXIA_URL}{endpoint}", json=body or {}, headers=headers)
            return json.dumps(r.json(), indent=2)
    except Exception as e:
        return f"Error calling MAXIA: {e}"


def get_maxia_tools(api_key: str = "") -> list:
    """Get all MAXIA tools for LangChain.
    
    Args:
        api_key: MAXIA API key (get free at maxiaworld.app/api/public/register)
    
    Returns:
        List of LangChain Tool objects
    """
    if not _LANGCHAIN_AVAILABLE:
        raise ImportError("langchain not installed. Run: pip install langchain")

    tools = [
        Tool(
            name="maxia_discover",
            func=lambda q: _call_maxia("/discover", {"capability": q}),
            description="Find AI services on MAXIA marketplace. Input: capability keyword (sentiment, audit, code, data, image, translation).",
        ),
        Tool(
            name="maxia_prices",
            func=lambda _: _call_maxia("/crypto/prices"),
            description="Get live cryptocurrency prices. Input: any string (ignored).",
        ),
        Tool(
            name="maxia_sentiment",
            func=lambda token: _call_maxia("/sentiment", {"token": token}),
            description="Get crypto sentiment analysis. Input: token symbol (BTC, ETH, SOL).",
        ),
        Tool(
            name="maxia_defi_yield",
            func=lambda asset: _call_maxia("/defi/best-yield", {"asset": asset, "limit": 5}),
            description="Find best DeFi yields. Input: asset symbol (USDC, ETH, SOL).",
        ),
        Tool(
            name="maxia_trending",
            func=lambda _: _call_maxia("/trending"),
            description="Get trending crypto tokens. Input: any string (ignored).",
        ),
        Tool(
            name="maxia_fear_greed",
            func=lambda _: _call_maxia("/fear-greed"),
            description="Get crypto Fear & Greed Index. Input: any string (ignored).",
        ),
        Tool(
            name="maxia_token_risk",
            func=lambda address: _call_maxia("/token-risk", {"address": address}),
            description="Analyze rug pull risk for a Solana token. Input: token mint address.",
        ),
        Tool(
            name="maxia_wallet_analysis",
            func=lambda address: _call_maxia("/wallet-analysis", {"address": address}),
            description="Analyze a Solana wallet holdings and profile. Input: wallet address.",
        ),
        Tool(
            name="maxia_marketplace_stats",
            func=lambda _: _call_maxia("/marketplace-stats"),
            description="Get MAXIA marketplace statistics. Input: any string (ignored).",
        ),
        Tool(
            name="maxia_swap_quote",
            func=lambda q: _call_maxia("/crypto/quote", {
                "from_token": q.split(",")[0].strip() if "," in q else "SOL",
                "to_token": q.split(",")[1].strip() if "," in q else "USDC",
                "amount": float(q.split(",")[2].strip()) if q.count(",") >= 2 else 1,
            }),
            description="Get a crypto swap quote. Input: 'FROM_TOKEN, TO_TOKEN, AMOUNT' (e.g. 'SOL, USDC, 10').",
        ),
        # ── GPU Rental ──
        Tool(
            name="maxia_gpu_tiers",
            func=lambda _: _call_maxia("/gpu/tiers"),
            description="List GPU tiers available for rent on MAXIA (RTX 4090, A100, H100, etc.) with pricing. Input: any string (ignored).",
        ),
        # ── Tokenized Stocks ──
        Tool(
            name="maxia_stocks_list",
            func=lambda _: _call_maxia("/stocks"),
            description="List all 30 tokenized stocks (AAPL, TSLA, NVDA...) with live prices. Input: any string (ignored).",
        ),
        Tool(
            name="maxia_stocks_price",
            func=lambda sym: _call_maxia(f"/stocks/price/{sym.strip()}"),
            description="Get real-time price of a tokenized stock. Input: stock symbol (AAPL, TSLA, NVDA, GOOGL).",
        ),
        Tool(
            name="maxia_stocks_fees",
            func=lambda _: _call_maxia("/stocks/compare-fees"),
            description="Compare MAXIA stock trading fees vs competitors (Robinhood, eToro, Binance). Input: any string (ignored).",
        ),
    ]

    # Add tools that require API key
    if api_key:
        tools.extend([
            Tool(
                name="maxia_execute",
                func=lambda q: _call_maxia("/execute", method="POST", body={
                    "service_id": q.split(",")[0].strip(),
                    "prompt": q.split(",", 1)[1].strip() if "," in q else q,
                }, api_key=api_key),
                description="Buy and execute a MAXIA service. Input: 'SERVICE_ID, your prompt'. Requires API key.",
            ),
            Tool(
                name="maxia_sell",
                func=lambda q: _call_maxia("/sell", method="POST", body={
                    "name": q.split(",")[0].strip(),
                    "description": q.split(",")[1].strip() if q.count(",") >= 1 else "",
                    "price_usdc": float(q.split(",")[2].strip()) if q.count(",") >= 2 else 1.0,
                }, api_key=api_key),
                description="List a service for sale on MAXIA. Input: 'NAME, DESCRIPTION, PRICE_USDC'. Requires API key.",
            ),
            Tool(
                name="maxia_negotiate",
                func=lambda q: _call_maxia("/negotiate", method="POST", body={
                    "service_id": q.split(",")[0].strip(),
                    "proposed_price": float(q.split(",")[1].strip()) if "," in q else 0,
                }, api_key=api_key),
                description="Negotiate price for a MAXIA service. Input: 'SERVICE_ID, PROPOSED_PRICE'. Requires API key.",
            ),
            # ── GPU with auth ──
            Tool(
                name="maxia_gpu_rent",
                func=lambda q: _call_maxia("/gpu/rent", method="POST", body={
                    "gpu_tier": q.split(",")[0].strip(),
                    "hours": float(q.split(",")[1].strip()) if q.count(",") >= 1 else 1,
                    "payment_tx": q.split(",")[2].strip() if q.count(",") >= 2 else "",
                }, api_key=api_key),
                description="Rent a GPU on MAXIA. Input: 'GPU_TIER, HOURS, PAYMENT_TX' (e.g. 'h100_sxm5, 2, TX_SIG'). Requires API key.",
            ),
            # ── Stocks with auth ──
            Tool(
                name="maxia_stocks_buy",
                func=lambda q: _call_maxia("/stocks/buy", method="POST", body={
                    "symbol": q.split(",")[0].strip(),
                    "amount_usdc": float(q.split(",")[1].strip()) if q.count(",") >= 1 else 10,
                    "payment_tx": q.split(",")[2].strip() if q.count(",") >= 2 else "",
                }, api_key=api_key),
                description="Buy tokenized stocks on MAXIA. Input: 'SYMBOL, AMOUNT_USDC, PAYMENT_TX' (e.g. 'AAPL, 50, TX_SIG'). Requires API key.",
            ),
            Tool(
                name="maxia_stocks_sell",
                func=lambda q: _call_maxia("/stocks/sell", method="POST", body={
                    "symbol": q.split(",")[0].strip(),
                    "shares": float(q.split(",")[1].strip()) if "," in q else 0,
                }, api_key=api_key),
                description="Sell tokenized stocks. Input: 'SYMBOL, SHARES' (e.g. 'AAPL, 0.5'). Requires API key.",
            ),
            Tool(
                name="maxia_stocks_portfolio",
                func=lambda _: _call_maxia("/stocks/portfolio", api_key=api_key),
                description="View your tokenized stock portfolio on MAXIA. Input: any string (ignored). Requires API key.",
            ),
        ])

    return tools


# For CrewAI compatibility
def get_crewai_tools(api_key: str = "") -> list:
    """Get MAXIA tools compatible with CrewAI.
    
    CrewAI uses LangChain tools natively, so this is the same.
    """
    return get_maxia_tools(api_key)
