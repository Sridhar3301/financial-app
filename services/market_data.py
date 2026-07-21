import yfinance as yf


def get_market_data(ticker: str):
    """
    Fetch real market and fundamental data for a stock.
    Example ticker:
        INFY.NS
        TCS.NS
        RELIANCE.NS
    """

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        market_data = {
            "company_name": info.get("longName"),
            "symbol": info.get("symbol"),
            "current_price": info.get("currentPrice"),
            "previous_close": info.get("previousClose"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "eps": info.get("trailingEps"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "revenue_growth": info.get("revenueGrowth"),
            "profit_margin": info.get("profitMargins"),
            "debt_to_equity": info.get("debtToEquity"),
            "return_on_equity": info.get("returnOnEquity"),
            "dividend_yield": info.get("dividendYield"),
        }

        return market_data

    except Exception as e:
        return {
            "error": str(e)
        }