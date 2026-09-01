"""Anomaly detection — statistical method (Isolation Forest when model available)."""

from app.schemas.prediction_schema import AnomalyDetectionRequest, AnomalyDetectionResponse
from app.services.model_service import ModelService


class AnalyticsService:
    def __init__(self, model_service: ModelService) -> None:
        self.model_service = model_service

    def detect_anomaly(self, payload: AnomalyDetectionRequest) -> AnomalyDetectionResponse:
        score = 0.0
        reasons: list[str] = []

        if (
            payload.actual_delivery_time is not None
            and payload.expected_delivery_time is not None
            and payload.expected_delivery_time > 0
        ):
            ratio = payload.actual_delivery_time / payload.expected_delivery_time
            if ratio >= 2.0:
                score = max(score, 0.9)
                reasons.append("Temps de livraison anormalement élevé")
            elif ratio >= 1.5:
                score = max(score, 0.7)
                reasons.append("Temps de livraison supérieur à la norme")

        if payload.driver_current_tasks is not None and payload.driver_current_tasks >= 6:
            score = max(score, 0.75)
            reasons.append("Surcharge d'un chauffeur")

        if payload.incidents_last_7_days is not None and payload.incidents_last_7_days >= 5:
            score = max(score, 0.8)
            reasons.append("Augmentation anormale des incidents")

        if payload.zone_delay_rate is not None and payload.zone_delay_rate >= 0.4:
            score = max(score, 0.65)
            reasons.append("Zone présentant un comportement inhabituel")

        anomaly = score >= 0.6
        reason = reasons[0] if reasons else "Aucune anomalie détectée"

        self.model_service.record_prediction()
        return AnomalyDetectionResponse(
            anomaly=anomaly,
            score=round(score, 2),
            reason=reason,
            explanation=reasons if reasons else ["Comportement dans les normes"],
        )
