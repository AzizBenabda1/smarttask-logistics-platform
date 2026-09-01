import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/api/ai/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert data["service"] == "smarttask-ai"
    assert "version" in data


def test_model_status_endpoint(client):
    response = client.get("/api/ai/model/status")
    assert response.status_code == 200
    data = response.json()
    assert data["delayModel"] == "loaded"
    assert data["deliveryTimeModel"] == "loaded"
    assert "modelsPath" in data


def test_predict_delay_with_model(client):
    payload = {
        "taskId": 125,
        "distanceKm": 12.5,
        "estimatedDuration": 40,
        "deadlineMinutes": 50,
        "priority": "HIGH",
        "hour": 17,
        "dayOfWeek": 5,
        "driverCurrentTasks": 3,
        "driverDelayRate": 0.12,
        "trafficLevel": "HIGH",
    }
    response = client.post("/api/ai/predict/delay", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["delayProbability"] <= 1
    assert data["riskLevel"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert len(data["explanation"]) >= 1


def test_predict_delivery_time_with_model(client):
    payload = {
        "taskId": 125,
        "distanceKm": 12.5,
        "estimatedDuration": 40,
        "priority": "HIGH",
        "hour": 17,
        "dayOfWeek": 5,
        "driverCurrentTasks": 3,
        "driverPerformance": 0.85,
        "trafficLevel": "HIGH",
    }
    response = client.post("/api/ai/predict/delivery-time", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimatedDeliveryTime"] >= 5
    assert data["unit"] == "minutes"


def test_predict_delay_without_model_returns_503():
    """503 when models are absent — tested without session training fixture."""
    from app.config import get_settings
    from app.main import app
    from app.services.model_service import ModelService

    settings = get_settings()
    bare_service = ModelService(settings)
    bare_service.delay_model = None
    bare_service.delivery_time_model = None

    with TestClient(app) as isolated:
        isolated.app.state.model_service = bare_service
        payload = {
            "taskId": 125,
            "distanceKm": 12.5,
            "estimatedDuration": 40,
            "deadlineMinutes": 50,
            "priority": "HIGH",
            "hour": 17,
            "dayOfWeek": 5,
            "driverCurrentTasks": 3,
            "driverDelayRate": 0.12,
            "trafficLevel": "HIGH",
        }
        response = isolated.post("/api/ai/predict/delay", json=payload)
        assert response.status_code == 503


def test_predict_delivery_success(client):
    payload = {
        "referenceId": "preview",
        "deliveryAddress": "12 Rue Example, Tunis 1000",
        "distanceKm": 8.5,
        "estimatedDuration": 35,
        "deadlineMinutes": 60,
        "priority": "MEDIUM",
        "hour": 14,
        "dayOfWeek": 2,
        "addressCompletenessScore": 0.85,
        "clientIncidentRate": 0.05,
        "clientFailedDeliveryRate": 0.03,
        "productFragileScore": 0.0,
        "driverCurrentTasks": 1,
        "driverDelayRate": 0.08,
        "trafficLevel": "MEDIUM",
    }
    response = client.post("/api/ai/predict/delivery-success", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["successProbability"] <= 1
    assert data["riskLevel"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert len(data["factors"]) >= 1
    assert len(data["suggestedActions"]) >= 1


def test_recommend_driver_scoring(client):
    payload = {
        "taskId": 125,
        "distanceKm": 12.5,
        "priority": "HIGH",
        "deadlineMinutes": 60,
        "drivers": [
            {
                "id": 1,
                "distanceFromClient": 3.2,
                "currentTasks": 2,
                "performanceScore": 0.94,
                "delayRate": 0.08,
            },
            {
                "id": 2,
                "distanceFromClient": 8.4,
                "currentTasks": 5,
                "performanceScore": 0.81,
                "delayRate": 0.19,
            },
        ],
    }
    response = client.post("/api/ai/recommend/driver", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recommendedDriverId"] == 1
    assert data["score"] > 0
    assert len(data["reasons"]) >= 1


def test_prioritize_task(client):
    payload = {
        "taskId": 125,
        "deadlineMinutes": 45,
        "priority": "HIGH",
        "delayProbability": 0.7,
        "distanceKm": 10,
        "estimatedDuration": 40,
        "driverCurrentTasks": 4,
    }
    response = client.post("/api/ai/prioritize/task", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["priorityScore"] >= 50
    assert data["recommendedPriority"] in ("HIGH", "CRITICAL")


def test_detect_anomaly(client):
    payload = {
        "taskId": 1,
        "actualDeliveryTime": 120,
        "expectedDeliveryTime": 45,
        "driverCurrentTasks": 7,
    }
    response = client.post("/api/ai/detect/anomaly", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["anomaly"] is True
    assert data["score"] >= 0.6


def test_metrics_endpoint(client):
    response = client.get("/api/ai/metrics")
    assert response.status_code == 200
    assert "predictionCount" in response.json()


def test_chat_endpoint(client):
    payload = {
        "message": "Bonjour",
        "context": {
            "role": "MANAGER",
            "userName": "Test Manager",
            "stats": {"delayedTasks": 2},
            "tasks": [],
            "orders": [],
            "drivers": [],
        },
    }
    response = client.post("/api/ai/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["intent"] == "GREETING"


def test_chat_suggestions_endpoint(client):
    response = client.get("/api/ai/chat/suggestions?role=DRIVER")
    assert response.status_code == 200
    data = response.json()
    assert len(data["suggestions"]) >= 2
    assert data["welcomeMessage"]
