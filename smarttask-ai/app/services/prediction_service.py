"""Prediction service — uses ML models when loaded."""

import numpy as np

from app.schemas.prediction_schema import (
    AnomalyDetectionRequest,
    AnomalyDetectionResponse,
    DelayPredictionRequest,
    DelayPredictionResponse,
    DeliverySuccessPredictionRequest,
    DeliverySuccessPredictionResponse,
    DeliveryTimePredictionRequest,
    DeliveryTimePredictionResponse,
    RiskLevel,
)
from app.services.model_service import ModelService


class PredictionService:
    def __init__(self, model_service: ModelService) -> None:
        self.model_service = model_service

    def predict_delay(self, payload: DelayPredictionRequest) -> DelayPredictionResponse:
        model = self.model_service.require_delay_model()
        features = np.array([self._delay_features(payload)])
        proba = float(model.predict_proba(features)[0][1])
        risk = self._risk_level(proba)
        explanation = self._delay_explanation(payload, proba)
        self.model_service.record_prediction()
        return DelayPredictionResponse(
            taskId=payload.task_id,
            delayProbability=round(proba, 4),
            riskLevel=risk,
            modelVersion=self.model_service.settings.delay_model_version,
            explanation=explanation,
        )

    def predict_delivery_time(
        self, payload: DeliveryTimePredictionRequest
    ) -> DeliveryTimePredictionResponse:
        model = self.model_service.require_delivery_time_model()
        features = np.array([self._delivery_features(payload)])
        minutes = int(max(5, round(float(model.predict(features)[0]))))
        explanation = self._delivery_explanation(payload, minutes)
        self.model_service.record_prediction()
        return DeliveryTimePredictionResponse(
            taskId=payload.task_id,
            estimatedDeliveryTime=minutes,
            modelVersion=self.model_service.settings.delivery_time_model_version,
            explanation=explanation,
        )

    def predict_delivery_success(
        self, payload: DeliverySuccessPredictionRequest
    ) -> DeliverySuccessPredictionResponse:
        try:
            model = self.model_service.require_delivery_success_model()
            features = np.array([self._delivery_success_features(payload)])
            proba = float(model.predict_proba(features)[0][1])
            rule_based = False
            version = self.model_service.settings.delivery_success_model_version
        except Exception:
            proba = self._rule_based_success_probability(payload)
            rule_based = True
            version = "1.0.0-rules"

        risk = self._success_risk_level(proba)
        factors = self._success_factors(payload, proba)
        actions = self._suggested_actions(payload, proba)
        explanation = factors.copy()
        self.model_service.record_prediction()
        return DeliverySuccessPredictionResponse(
            taskId=payload.task_id,
            referenceId=payload.reference_id,
            successProbability=round(proba, 4),
            riskLevel=risk,
            factors=factors,
            suggestedActions=actions,
            modelVersion=version,
            explanation=explanation,
            ruleBased=rule_based,
        )

    def _delivery_success_features(self, p: DeliverySuccessPredictionRequest) -> list[float]:
        priority_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        traffic_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        return [
            p.address_completeness_score,
            p.distance_km,
            p.estimated_duration,
            p.deadline_minutes,
            priority_map[p.priority.value],
            p.hour,
            p.day_of_week,
            p.client_incident_rate,
            p.client_failed_delivery_rate,
            traffic_map[p.traffic_level.value],
            p.product_fragile_score,
            p.driver_current_tasks,
            p.driver_delay_rate,
        ]

    @staticmethod
    def _rule_based_success_probability(p: DeliverySuccessPredictionRequest) -> float:
        priority_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        traffic_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        score = (
            0.35 * p.address_completeness_score
            + 0.15 * (1 - min(p.client_incident_rate, 0.5))
            + 0.15 * (1 - min(p.client_failed_delivery_rate, 0.5))
            + 0.1 * (1 - traffic_map[p.traffic_level.value] / 2)
            - 0.08 * priority_map[p.priority.value]
            - 0.07 * min(p.driver_current_tasks, 5) / 5
            - 0.1 * p.driver_delay_rate
            - 0.05 * p.product_fragile_score
        )
        if p.estimated_duration >= p.deadline_minutes * 0.92:
            score -= 0.12
        return float(max(0.05, min(0.95, score)))

    @staticmethod
    def _success_risk_level(success_probability: float) -> RiskLevel:
        if success_probability >= 0.75:
            return RiskLevel.LOW
        if success_probability >= 0.55:
            return RiskLevel.MEDIUM
        if success_probability >= 0.35:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    @staticmethod
    def _success_factors(p: DeliverySuccessPredictionRequest, proba: float) -> list[str]:
        factors: list[str] = []
        if p.address_completeness_score < 0.55:
            factors.append("Adresse incomplete ou vague")
        if p.client_incident_rate >= 0.15:
            factors.append("Historique incidents client eleve")
        if p.client_failed_delivery_rate >= 0.12:
            factors.append("Echecs de livraison passes")
        if p.traffic_level.value == "HIGH":
            factors.append("Trafic eleve prevu")
        if p.estimated_duration >= p.deadline_minutes * 0.9:
            factors.append("Deadline serree")
        if p.driver_current_tasks >= 3:
            factors.append("Chauffeur fortement charge")
        if p.driver_delay_rate >= 0.15:
            factors.append("Historique retard chauffeur")
        if p.product_fragile_score >= 0.5:
            factors.append("Produit fragile ou sensible")
        if not factors:
            factors.append(
                "Conditions favorables" if proba >= 0.6 else "Plusieurs facteurs de risque moderes"
            )
        return factors

    @staticmethod
    def _suggested_actions(p: DeliverySuccessPredictionRequest, proba: float) -> list[str]:
        actions: list[str] = []
        if p.address_completeness_score < 0.55:
            actions.append("Preciser l'adresse avec numero et ville")
        if p.client_incident_rate >= 0.15 or p.client_failed_delivery_rate >= 0.12:
            actions.append("Contacter le client pour confirmer disponibilite")
        if p.estimated_duration >= p.deadline_minutes * 0.9:
            actions.append("Ajuster le creneau ou la priorite")
        if p.driver_current_tasks >= 3:
            actions.append("Assigner un chauffeur moins charge")
        if proba < 0.45:
            actions.append("Valider manuellement avant expedition")
        if not actions:
            actions.append("Poursuivre le workflow standard")
        return actions

    def _delay_features(self, p: DelayPredictionRequest) -> list[float]:
        priority_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        traffic_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        return [
            p.distance_km,
            p.estimated_duration,
            p.deadline_minutes,
            priority_map[p.priority.value],
            p.hour,
            p.day_of_week,
            p.driver_current_tasks,
            p.driver_delay_rate,
            traffic_map[p.traffic_level.value],
        ]

    def _delivery_features(self, p: DeliveryTimePredictionRequest) -> list[float]:
        priority_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        traffic_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        return [
            p.distance_km,
            p.estimated_duration,
            priority_map[p.priority.value],
            p.hour,
            p.day_of_week,
            p.driver_current_tasks,
            p.driver_performance,
            traffic_map[p.traffic_level.value],
        ]

    @staticmethod
    def _risk_level(probability: float) -> RiskLevel:
        if probability >= 0.75:
            return RiskLevel.CRITICAL
        if probability >= 0.55:
            return RiskLevel.HIGH
        if probability >= 0.35:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    @staticmethod
    def _delay_explanation(p: DelayPredictionRequest, proba: float) -> list[str]:
        reasons: list[str] = []
        if p.estimated_duration >= p.deadline_minutes * 0.9:
            reasons.append("Deadline proche")
        if p.traffic_level.value == "HIGH":
            reasons.append("Trafic élevé")
        if p.driver_current_tasks >= 3:
            reasons.append("Charge importante du chauffeur")
        if p.driver_delay_rate >= 0.15:
            reasons.append("Historique de retard élevé")
        if p.priority.value in ("HIGH", "CRITICAL"):
            reasons.append("Priorité élevée")
        if not reasons:
            reasons.append("Risque modéré selon le modèle" if proba < 0.5 else "Plusieurs facteurs défavorables")
        return reasons

    @staticmethod
    def _delivery_explanation(p: DeliveryTimePredictionRequest, minutes: int) -> list[str]:
        reasons: list[str] = []
        if p.distance_km > 15:
            reasons.append("Distance importante")
        if p.traffic_level.value == "HIGH":
            reasons.append("Trafic élevé")
        if p.driver_current_tasks >= 3:
            reasons.append("Chauffeur fortement chargé")
        if minutes > p.estimated_duration:
            reasons.append("Estimation supérieure au temps prévu initial")
        if not reasons:
            reasons.append("Estimation basée sur les features de la tâche")
        return reasons
