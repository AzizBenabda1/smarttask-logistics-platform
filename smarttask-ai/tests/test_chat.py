from app.schemas.chat_schema import ChatContext, ChatRequest
from app.services.chat_service import ChatService


def test_greeting():
    svc = ChatService()
    req = ChatRequest(
        message="Bonjour",
        context=ChatContext(role="MANAGER", userName="Test Manager"),
    )
    resp = svc.chat(req)
    assert resp.intent.value == "GREETING"
    assert "SmartTask Copilot" in resp.reply


def test_off_topic():
    svc = ChatService()
    req = ChatRequest(
        message="Quelle est la météo à Paris ?",
        context=ChatContext(role="CLIENT", userName="Test Client"),
    )
    resp = svc.chat(req)
    assert resp.intent.value == "OFF_TOPIC"


def test_suggestions_by_role():
    svc = ChatService()
    resp = svc.get_suggestions("DRIVER")
    assert len(resp.suggestions) >= 2
    assert resp.welcome_message
