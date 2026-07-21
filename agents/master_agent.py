from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are an expert AI Financial Advisor.

Analyze the given company and investment request.

If Google Search is available, use it to obtain recent financial news before answering.

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

Rules:

- Allocation percentages must total exactly 100.
- Confidence values must be between 0 and 100.
- If information is unavailable, return an empty string or empty list.
- Never invent financial figures.
- Return ONLY JSON.
"""


class MasterAgent(BaseAgent):

    name = "Master Agent"
    system_prompt = SYSTEM_PROMPT

    def __init__(self):
        super().__init__(use_web_search=True)

    def analyze(
        self,
        company: str,
        budget: float,
        duration: str,
        risk_profile: str,
    ):

        message = f"""
Company: {company}

Budget: ₹{budget}

Investment Duration: {duration}

Risk Profile: {risk_profile}

Perform all of the following:

1. Analyze the company fundamentals.
2. Analyze the latest financial news.
3. Assess investment risks.
4. Recommend a diversified portfolio.
5. Verify the recommendation.
6. Explain the recommendation in simple language.

Return ONLY the JSON object described in the system prompt.
"""

        return self.run(message)