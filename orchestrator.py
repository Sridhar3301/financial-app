"""
Orchestrator using ONE Gemini API call via MasterAgent.
"""

from dataclasses import dataclass, field

from agents.master_agent import MasterAgent


@dataclass
class UserRequest:
    company: str
    budget: float
    duration: str
    risk_profile: str = "moderate"


@dataclass
class PipelineResult:
    request: UserRequest
    market_analysis: dict = field(default_factory=dict)
    news_analysis: dict = field(default_factory=dict)
    risk_assessment: dict = field(default_factory=dict)
    portfolio_recommendation: dict = field(default_factory=dict)
    verification: dict = field(default_factory=dict)
    explainability: dict = field(default_factory=dict)
    final_confidence: int = 0


class Orchestrator:

    def __init__(self):
        self.master_agent = MasterAgent()

    def run(self, request: UserRequest, verbose: bool = True) -> PipelineResult:

        result = PipelineResult(request=request)

        if verbose:
            print("\nRunning Master Agent...\n")

        analysis = self.master_agent.analyze(
            company=request.company,
            budget=request.budget,
            duration=request.duration,
            risk_profile=request.risk_profile,
        )

        result.market_analysis = analysis.get("market_analysis", {})
        result.news_analysis = analysis.get("news_analysis", {})
        result.risk_assessment = analysis.get("risk_assessment", {})
        result.portfolio_recommendation = analysis.get("portfolio_recommendation", {})
        result.verification = analysis.get("verification", {})
        result.explainability = analysis.get("explainability", {})

        result.final_confidence = self._compute_final_confidence(result)

        return result

    @staticmethod
    def _compute_final_confidence(result: PipelineResult) -> int:

        confidences = [
            result.market_analysis.get("confidence", 0),
            result.news_analysis.get("confidence", 0),
            result.risk_assessment.get("confidence", 0),
            result.portfolio_recommendation.get("confidence", 0),
        ]

        confidences = [
            c for c in confidences
            if isinstance(c, (int, float))
        ]

        avg = sum(confidences) / len(confidences) if confidences else 0

        adjustment = result.verification.get(
            "confidence_adjustment",
            0,
        )

        try:
            adjustment = float(adjustment)
        except (ValueError, TypeError):
            adjustment = 0

        final = avg + adjustment

        return max(0, min(100, round(final)))