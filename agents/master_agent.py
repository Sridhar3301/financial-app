from .base_agent import BaseAgent

from services.market_data import get_market_data
from services.news_data import get_company_news


# ==========================================================
# COMPANY NAME -> YAHOO FINANCE TICKER MAPPING
# ==========================================================

COMPANY_TICKERS = {

    # IT Companies
    "infosys": "INFY.NS",
    "infosys limited": "INFY.NS",

    "tcs": "TCS.NS",
    "tata consultancy services": "TCS.NS",

    "wipro": "WIPRO.NS",

    "hcl": "HCLTECH.NS",
    "hcl technologies": "HCLTECH.NS",

    "tech mahindra": "TECHM.NS",

    # Reliance
    "reliance": "RELIANCE.NS",
    "reliance industries": "RELIANCE.NS",

    # Banks
    "hdfc": "HDFCBANK.NS",
    "hdfc bank": "HDFCBANK.NS",

    "icici": "ICICIBANK.NS",
    "icici bank": "ICICIBANK.NS",

    "sbi": "SBIN.NS",
    "state bank of india": "SBIN.NS",

    "axis bank": "AXISBANK.NS",

    "kotak bank": "KOTAKBANK.NS",
    "kotak mahindra bank": "KOTAKBANK.NS",

    # Automobile
    "tata motors": "TATAMOTORS.NS",

    "maruti": "MARUTI.NS",
    "maruti suzuki": "MARUTI.NS",

    "mahindra": "M&M.NS",
    "mahindra and mahindra": "M&M.NS",

    # FMCG
    "itc": "ITC.NS",

    "hindustan unilever": "HINDUNILVR.NS",
    "hul": "HINDUNILVR.NS",

    "nestle india": "NESTLEIND.NS",

    # Telecom
    "airtel": "BHARTIARTL.NS",
    "bharti airtel": "BHARTIARTL.NS",

    # Other major companies
    "adani enterprises": "ADANIENT.NS",
    "adani ports": "ADANIPORTS.NS",

    "larsen and toubro": "LT.NS",
    "l&t": "LT.NS",

    "sun pharma": "SUNPHARMA.NS",

    "asian paints": "ASIANPAINT.NS",

    "titan": "TITAN.NS",
}


# ==========================================================
# TICKER RESOLVER
# ==========================================================

def get_ticker(company: str):
    """
    Convert a company name entered by the user into
    a Yahoo Finance NSE ticker.

    Example:
        Infosys -> INFY.NS
        TCS -> TCS.NS
        Reliance -> RELIANCE.NS
    """

    if not company:
        return None

    normalized_company = company.lower().strip()

    return COMPANY_TICKERS.get(normalized_company)


# ==========================================================
# MASTER AGENT SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an expert AI Financial Advisor.

Your responsibility is to analyze a company and the user's
investment request using supplied real financial market data
and recent news articles.

PRIMARY DATA RULES:

- Use the supplied REAL FINANCIAL MARKET DATA as the primary
  factual source for company fundamentals and numerical
  financial metrics.

- Use the supplied RECENT NEWS ARTICLES as the primary source
  for company news analysis and news sentiment.

- If Google Search is available, it may be used only for
  additional context, verification, or information that is
  unavailable in the supplied data.

- If Google Search information conflicts with the supplied
  financial market data for numerical company fundamentals,
  prefer the supplied financial market data.

- Never invent financial figures.

- Never guess unavailable financial metrics.

- If information is unavailable, clearly treat it as
  unavailable.

NEWS ANALYSIS RULES:

- Analyze the supplied recent news articles.

- Determine whether the overall news sentiment is:
  Positive, Neutral, or Negative.

- Identify important events that may affect the company.

- Distinguish positive news from negative news.

- Ignore irrelevant or clickbait information.

- Consider the potential effect of the news on investment risk.

MARKET ANALYSIS RULES:

Analyze available information such as:

- Current market price
- Previous close
- Market capitalization
- P/E ratio
- Forward P/E ratio
- EPS
- 52-week high
- 52-week low
- Revenue growth
- Profit margin
- Debt-to-equity
- Return on equity
- Dividend yield

Do not assume that every metric will always be available.

RISK ANALYSIS RULES:

Consider:

- Company fundamentals
- Valuation
- Financial health
- Recent news sentiment
- Company-specific risks
- Market risks
- User risk profile
- Investment duration

PORTFOLIO RULES:

- Recommend a diversified portfolio appropriate for the
  user's budget, investment duration, and risk profile.

- Allocation percentages must total exactly 100.

VERIFICATION RULES:

- Verify that conclusions are consistent with the supplied
  market data and news.

- Identify contradictions or uncertainties.

- Reduce confidence when important information is missing.

EXPLAINABILITY RULES:

- Explain the recommendation in simple language.

- Clearly distinguish evidence from assumptions.

- Mention important uncertainties.

- Mention scenarios that could change the recommendation.


Return ONLY valid JSON.

Do not use markdown.

Do not explain anything outside JSON.


The JSON must exactly follow this structure:

{
  "market_analysis": {
    "company": "",
    "sector": "",
    "market_summary": "",
    "strengths": [],
    "weaknesses": [],
    "opportunities": [],
    "risks": [],
    "confidence": 0
  },

  "news_analysis": {
    "overall_sentiment": "",
    "major_events": [],
    "positive_news": [],
    "negative_news": [],
    "impact_score": 0,
    "confidence": 0
  },

  "risk_assessment": {
    "overall_risk": "",
    "risk_score": 0,
    "major_risks": [],
    "risk_reasoning": "",
    "confidence": 0
  },

  "portfolio_recommendation": {
    "allocation": [
      {
        "asset": "",
        "percentage": 0
      }
    ],
    "expected_strategy": "",
    "investment_horizon": "",
    "warnings": [],
    "confidence": 0
  },

  "verification": {
    "verified": true,
    "issues": [],
    "confidence_adjustment": 0,
    "verification_notes": ""
  },

  "explainability": {
    "summary": "",
    "reasoning": [],
    "evidence": [],
    "assumptions": [],
    "uncertainties": [],
    "alternative_scenarios": [],
    "confidence": 0
  }
}


FINAL RULES:

- Allocation percentages must total exactly 100.

- Confidence values must be between 0 and 100.

- Risk score and impact score must be between 0 and 100.

- If information is unavailable, return an empty string,
  empty list, or clearly state that the metric was unavailable.

- Never invent financial figures.

- Do not return markdown.

- Return ONLY JSON.
"""


# ==========================================================
# MASTER AGENT
# ==========================================================

class MasterAgent(BaseAgent):

    name = "Master Agent"

    system_prompt = SYSTEM_PROMPT

    def __init__(self):

        # Google Search remains enabled for additional
        # verification/context if required.
        super().__init__(use_web_search=True)


    # ======================================================
    # MAIN ANALYSIS METHOD
    # ======================================================

    def analyze(
        self,
        company: str,
        budget: float,
        duration: str,
        risk_profile: str,
    ):

        # --------------------------------------------------
        # STEP 1:
        # Resolve company name to Yahoo Finance ticker
        # --------------------------------------------------

        ticker = get_ticker(company)


        # --------------------------------------------------
        # STEP 2:
        # Fetch REAL financial market data
        # --------------------------------------------------

        if ticker:

            market_data = get_market_data(ticker)

        else:

            market_data = {
                "error": (
                    f"No Yahoo Finance ticker mapping "
                    f"was found for '{company}'."
                )
            }


        # --------------------------------------------------
        # STEP 3:
        # Fetch REAL recent company news
        # --------------------------------------------------

        news_articles = get_company_news(
            company_name=company,
            limit=5
        )


        # --------------------------------------------------
        # STEP 4:
        # Build the complete analysis prompt
        # --------------------------------------------------

        message = f"""

==================================================
USER INVESTMENT REQUEST
==================================================

Company:
{company}

Yahoo Finance Ticker:
{ticker if ticker else "Ticker unavailable"}

Budget:
₹{budget}

Investment Duration:
{duration}

Risk Profile:
{risk_profile}


==================================================
REAL FINANCIAL MARKET DATA
==================================================

The following financial data was retrieved
programmatically from the market data service.

{market_data}


==================================================
RECENT NEWS ARTICLES
==================================================

The following recent news articles were retrieved
programmatically from the news service.

{news_articles}


==================================================
ANALYSIS INSTRUCTIONS
==================================================


1. MARKET ANALYSIS

Analyze the company's fundamentals using the supplied
REAL FINANCIAL MARKET DATA.

Consider available metrics including:

- Current price
- Previous close
- Market capitalization
- P/E ratio
- Forward P/E
- EPS
- 52-week high
- 52-week low
- Revenue growth
- Profit margin
- Debt-to-equity
- Return on equity
- Dividend yield

Identify:

- Strengths
- Weaknesses
- Opportunities
- Risks


--------------------------------------------------


2. NEWS ANALYSIS

Analyze the supplied RECENT NEWS ARTICLES.

Determine:

- Overall sentiment
- Major events
- Positive developments
- Negative developments
- Potential investment impact

Classify overall sentiment as:

Positive
Neutral
or
Negative

Do NOT invent additional news events.


--------------------------------------------------


3. RISK ASSESSMENT

Assess investment risk using BOTH:

- Financial fundamentals
- Recent news sentiment

Also consider:

- User risk profile
- Investment duration
- Company-specific risks
- Market uncertainty

Produce an overall risk classification and
risk score.


--------------------------------------------------


4. PORTFOLIO RECOMMENDATION

Recommend a diversified portfolio appropriate for:

- ₹{budget} budget
- {duration} investment duration
- {risk_profile} risk profile

The allocation percentages MUST total exactly 100.


--------------------------------------------------


5. VERIFICATION

Verify the recommendation against:

- Supplied financial data
- Supplied news
- Risk assessment

Identify:

- Missing information
- Contradictions
- Uncertainty
- Potential weaknesses in the recommendation


--------------------------------------------------


6. EXPLAINABILITY

Explain the recommendation in simple language.

Clearly provide:

- Reasoning
- Evidence
- Assumptions
- Uncertainties
- Alternative scenarios


==================================================
CRITICAL DATA ACCURACY RULES
==================================================

1. Treat the supplied REAL FINANCIAL MARKET DATA as
   the primary source for numerical company fundamentals.

2. Do NOT invent financial figures.

3. Do NOT replace supplied financial figures with figures
   recalled from model memory.

4. Primarily analyze the supplied news articles when
   determining company news sentiment.

5. Do NOT invent news events that are not present in the
   supplied articles.

6. Google Search may only be used for additional context
   or verification when necessary.

7. If Google Search information conflicts with the supplied
   market data for numerical fundamentals, prefer the
   supplied market data.

8. If financial data contains an error or unavailable value,
   acknowledge the missing information rather than guessing.

9. Do not confuse decimal financial ratios with percentages.
   For example, revenue_growth of 0.066 represents 6.6%.

10. Base the final risk assessment and recommendation on
    evidence from the supplied data whenever possible.


==================================================
OUTPUT
==================================================

Return ONLY the JSON object described in the system prompt.

Do NOT return markdown.

Do NOT include ```json.

Do NOT include explanations outside the JSON.

"""

        # --------------------------------------------------
        # STEP 5:
        # Send everything through ONE Master Agent call
        # --------------------------------------------------

        return self.run(message)