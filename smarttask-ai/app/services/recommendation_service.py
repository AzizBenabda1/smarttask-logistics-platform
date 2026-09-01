"""Explainable scoring for driver recommendation and task prioritization.

When sufficient historical data exists, replace scoring with trained ML models.
"""

from app.schemas.prediction_schema import PriorityLevel
from app.schemas.recommendation_schema import (
    DriverCandidate,
    DriverRecommendationRequest,
    DriverRecommendationResponse,
    TaskPrioritizationRequest,
    TaskPrioritizationResponse,
)
from app.services.model_service import ModelService


class RecommendationService:
    def __init__(self, model_service: ModelService) -> None:
        self.model_service = model_service

    def recommend_driver(self, payload: DriverRecommendationRequest) -> DriverRecommendationResponse:
        best: DriverCandidate | None = None
        best_score = -1
        best_reasons: list[str] = []

        for driver in payload.drivers:
            score, reasons = self._score_driver(driver, payload)
            if score > best_score:
                best_score = score
                best = driver
                best_reasons = reasons

        assert best is not None
        self.model_service.record_prediction()
        return DriverRecommendationResponse(
            taskId=payload.task_id,
            recommendedDriverId=best.id,
            score=min(best_score, 100),
            reasons=best_reasons,
            scoringMethod="explainable_scoring",
            modelVersion="1.0.0-scoring",
        )

    def prioritize_task(self, payload: TaskPrioritizationRequest) -> TaskPrioritizationResponse:
        score = 0
        reasons: list[str] = []

        if payload.deadline_minutes <= 30:
            score += 35
            reasons.append("Deadline très proche")
        elif payload.deadline_minutes <= 60:
            score += 25
            reasons.append("Deadline proche")

        priority_boost = {"LOW": 5, "MEDIUM": 15, "HIGH": 25, "CRITICAL": 35}
        score += priority_boost[payload.priority.value]

        score += int(payload.delay_probability * 30)
        if payload.delay_probability >= 0.6:
            reasons.append("Risque élevé de retard")

        if payload.driver_current_tasks >= 4:
            score += 10
            reasons.append("Chauffeur surchargé")

        score = min(score, 100)
        recommended = self._score_to_priority(score, payload.priority)
        reason = reasons[0] if reasons else "Score calculé à partir des facteurs logistiques"

        self.model_service.record_prediction()
        return TaskPrioritizationResponse(
            taskId=payload.task_id,
            priorityScore=score,
            recommendedPriority=recommended,
            reason=reason,
            scoringMethod="explainable_scoring",
        )

    def _score_driver(
        self, driver: DriverCandidate, payload: DriverRecommendationRequest
    ) -> tuple[int, list[str]]:
        score = 0
        reasons: list[str] = []

        if driver.available:
            score += 30
            reasons.append("Chauffeur disponible")

        if driver.distance_from_client <= 5:
            score += 25
            reasons.append("Proche du client")
        elif driver.distance_from_client <= 10:
            score += 15
            reasons.append("Distance acceptable")

        if driver.current_tasks <= 2:
            score += 20
            reasons.append("Faible charge")
        elif driver.current_tasks <= 4:
            score += 10
            reasons.append("Charge modérée")

        if driver.performance_score >= 0.85:
            score += 15
            reasons.append("Bonne performance historique")
        elif driver.performance_score >= 0.7:
            score += 8
            reasons.append("Performance correcte")

        if driver.delay_rate <= 0.1:
            score += 10
            reasons.append("Faible taux de retard")

        if payload.priority.value in ("HIGH", "CRITICAL") and driver.current_tasks <= 2:
            score += 5

        return score, reasons

    @staticmethod
    def _score_to_priority(score: int, current: PriorityLevel) -> PriorityLevel:
        if score >= 85:
            return PriorityLevel.CRITICAL
        if score >= 65:
            return PriorityLevel.HIGH
        if score >= 40:
            return PriorityLevel.MEDIUM
        return current if current != PriorityLevel.CRITICAL else PriorityLevel.HIGH
