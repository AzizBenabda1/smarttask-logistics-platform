from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ChatIntent(str, Enum):
    GREETING = "GREETING"
    TASK_STATUS = "TASK_STATUS"
    DELAYED_TASKS = "DELAYED_TASKS"
    AVAILABLE_DRIVERS = "AVAILABLE_DRIVERS"
    ORDER_TRACKING = "ORDER_TRACKING"
    MY_MISSIONS = "MY_MISSIONS"
    DASHBOARD_SUMMARY = "DASHBOARD_SUMMARY"
    HELP_WORKFLOW = "HELP_WORKFLOW"
    AI_INFO = "AI_INFO"
    UNKNOWN = "UNKNOWN"
    OFF_TOPIC = "OFF_TOPIC"


class ChatAction(BaseModel):
    label: str
    action_type: str = Field(..., alias="actionType")
    payload: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}


class ChatContextItem(BaseModel):
    id: int | None = None
    label: str = ""
    status: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class ChatContext(BaseModel):
    role: str
    user_name: str = Field(..., alias="userName")
    stats: dict[str, Any] = Field(default_factory=dict)
    tasks: list[ChatContextItem] = Field(default_factory=list)
    orders: list[ChatContextItem] = Field(default_factory=list)
    drivers: list[ChatContextItem] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: ChatContext
    session_id: str | None = Field(default=None, alias="sessionId")

    model_config = {"populate_by_name": True}


class ChatResponse(BaseModel):
    reply: str
    intent: ChatIntent
    confidence: float = Field(ge=0, le=1)
    sources: list[str] = Field(default_factory=list)
    actions: list[ChatAction] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    proactive: bool = False

    model_config = {"populate_by_name": True}


class ChatSuggestionsResponse(BaseModel):
    suggestions: list[str]
    welcome_message: str = Field(..., alias="welcomeMessage")

    model_config = {"populate_by_name": True}
