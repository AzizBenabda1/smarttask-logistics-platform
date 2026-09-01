"""SmartTask Copilot — intent-based grounded chat engine."""

from __future__ import annotations

import json
import re
from pathlib import Path

from app.schemas.chat_schema import (
    ChatAction,
    ChatContext,
    ChatIntent,
    ChatRequest,
    ChatResponse,
    ChatSuggestionsResponse,
)

_KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"

OFF_TOPIC_PATTERNS = re.compile(
    r"\b(météo|weather|capital|football|politique|recette|cuisine|film|musique|"
    r"devoir|examen|math|python tutorial|javascript|bitcoin|crypto|amour|dating)\b",
    re.IGNORECASE,
)

INTENT_PATTERNS: list[tuple[ChatIntent, re.Pattern[str]]] = [
    (ChatIntent.GREETING, re.compile(r"\b(bonjour|salut|hello|bonsoir|coucou|hey|aide)\b", re.I)),
    (ChatIntent.DELAYED_TASKS, re.compile(r"\b(retard|retardé|delayed|en retard|critique|risk)\b", re.I)),
    (ChatIntent.AVAILABLE_DRIVERS, re.compile(r"\b(chauffeur|driver|dispo|disponible|assign)\b", re.I)),
    (ChatIntent.ORDER_TRACKING, re.compile(r"\b(commande|order|suivre|tracking|livraison|où en est|ou en est)\b", re.I)),
    (ChatIntent.MY_MISSIONS, re.compile(r"\b(mission|mes tâches|my task|prochaine|itinéraire|route)\b", re.I)),
    (ChatIntent.DASHBOARD_SUMMARY, re.compile(r"\b(kpi|tableau|dashboard|statistique|analytics|résumé|resume|aujourd'hui)\b", re.I)),
    (ChatIntent.AI_INFO, re.compile(r"\b(ia|ai|intelligence|prédiction|prediction|modèle|model|analyser)\b", re.I)),
    (ChatIntent.HELP_WORKFLOW, re.compile(r"\b(comment|aide|help|workflow|statut|status|fonctionne)\b", re.I)),
    (ChatIntent.TASK_STATUS, re.compile(r"\b(tâche|task|#\d+|mission)\b", re.I)),
]


class ChatService:
    def __init__(self) -> None:
        self._kb = self._load_kb()

    def _load_kb(self) -> dict:
        if _KB_PATH.exists():
            return json.loads(_KB_PATH.read_text(encoding="utf-8"))
        return {}

    def get_suggestions(self, role: str) -> ChatSuggestionsResponse:
        role = role.upper()
        suggestions_map = {
            "MANAGER": [
                "Quelles livraisons sont en retard ?",
                "Chauffeurs disponibles ?",
                "Résumé du tableau de bord",
                "Comment fonctionne SmartTask AI ?",
            ],
            "OPERATOR": [
                "Commandes en attente ?",
                "Comment valider une commande ?",
                "Tâches à préparer aujourd'hui",
            ],
            "DRIVER": [
                "Quelle est ma prochaine mission ?",
                "Mes missions du jour",
                "Comment signaler un incident ?",
            ],
            "CLIENT": [
                "Où en est ma commande ?",
                "Délai de livraison estimé",
                "Comment confirmer ma réception ?",
            ],
            "ADMIN": [
                "Résumé des opérations",
                "Comment fonctionne SmartTask ?",
            ],
        }
        suggestions = suggestions_map.get(role, suggestions_map["MANAGER"])
        welcome = (
            "Bonjour ! Je suis SmartTask Copilot, votre assistant logistique. "
            "Je réponds uniquement dans le contexte SmartTask (livraisons, commandes, IA). "
            "Comment puis-je vous aider ?"
        )
        return ChatSuggestionsResponse(suggestions=suggestions, welcomeMessage=welcome)

    def chat(self, payload: ChatRequest) -> ChatResponse:
        message = payload.message.strip()
        ctx = payload.context

        if OFF_TOPIC_PATTERNS.search(message):
            return self._off_topic()

        intent, confidence = self._classify(message, ctx.role)

        handlers = {
            ChatIntent.GREETING: self._greeting,
            ChatIntent.DELAYED_TASKS: self._delayed_tasks,
            ChatIntent.AVAILABLE_DRIVERS: self._available_drivers,
            ChatIntent.ORDER_TRACKING: self._order_tracking,
            ChatIntent.MY_MISSIONS: self._my_missions,
            ChatIntent.DASHBOARD_SUMMARY: self._dashboard,
            ChatIntent.AI_INFO: self._ai_info,
            ChatIntent.HELP_WORKFLOW: self._help_workflow,
            ChatIntent.TASK_STATUS: self._task_status,
            ChatIntent.UNKNOWN: self._unknown,
        }

        handler = handlers.get(intent, self._unknown)
        return handler(message, ctx, intent, confidence)

    def _classify(self, message: str, role: str) -> tuple[ChatIntent, float]:
        role = role.upper()
        scores: dict[ChatIntent, float] = {}

        for intent, pattern in INTENT_PATTERNS:
            if pattern.search(message):
                scores[intent] = scores.get(intent, 0) + 0.6

        if role == "DRIVER" and re.search(r"\b(mission|tâche|prochaine)\b", message, re.I):
            scores[ChatIntent.MY_MISSIONS] = scores.get(ChatIntent.MY_MISSIONS, 0) + 0.5
        if role == "CLIENT" and re.search(r"\b(commande|livraison|suivre)\b", message, re.I):
            scores[ChatIntent.ORDER_TRACKING] = scores.get(ChatIntent.ORDER_TRACKING, 0) + 0.5
        if role == "MANAGER" and re.search(r"\b(retard|kpi|chauffeur)\b", message, re.I):
            for i in (ChatIntent.DELAYED_TASKS, ChatIntent.DASHBOARD_SUMMARY, ChatIntent.AVAILABLE_DRIVERS):
                if i in scores:
                    scores[i] += 0.2

        if not scores:
            faq = self._match_faq(message)
            if faq:
                return ChatIntent.HELP_WORKFLOW, 0.75
            return ChatIntent.UNKNOWN, 0.3

        best = max(scores, key=scores.get)
        return best, min(scores[best], 0.95)

    def _match_faq(self, message: str) -> str | None:
        lower = message.lower()
        for item in self._kb.get("faq", []):
            if any(kw in lower for kw in item.get("keywords", [])):
                return item.get("answer")
        return None

    def _off_topic(self) -> ChatResponse:
        return ChatResponse(
            reply=self._kb.get("off_topic_response", "Hors sujet SmartTask."),
            intent=ChatIntent.OFF_TOPIC,
            confidence=0.99,
            sources=["knowledge_base:guardrails"],
            suggestions=["Quelles livraisons sont en retard ?", "Où en est ma commande ?"],
        )

    def _greeting(self, _msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        name = ctx.user_name.split()[0] if ctx.user_name else "Utilisateur"
        role_desc = self._kb.get("workflows", {}).get("roles", {}).get(ctx.role.upper(), ctx.role)
        stats = ctx.stats
        summary = ""
        if stats:
            parts = [f"{k}: {v}" for k, v in list(stats.items())[:3]]
            summary = " État actuel — " + ", ".join(parts) + "."

        return ChatResponse(
            reply=(
                f"Bonjour {name} ! Je suis SmartTask Copilot.{summary} "
                f"En tant que {ctx.role.lower()}, vous pouvez : {role_desc}. Que souhaitez-vous savoir ?"
            ),
            intent=intent,
            confidence=conf,
            sources=[f"role:{ctx.role}", "knowledge_base:workflows"],
            suggestions=self.get_suggestions(ctx.role).suggestions[:3],
        )

    def _delayed_tasks(self, _msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        delayed = [t for t in ctx.tasks if (t.status or "").upper() in ("DELAYED", "DELAY")]
        if not delayed:
            delayed = [t for t in ctx.tasks if t.extra.get("delayed")]

        if not delayed:
            count = ctx.stats.get("delayedTasks", 0)
            if count and int(count) > 0:
                return ChatResponse(
                    reply=f"Il y a {count} tâche(s) en retard selon le tableau de bord. Consultez la page Retards pour le détail.",
                    intent=intent,
                    confidence=conf,
                    sources=["stats:delayedTasks"],
                    actions=[ChatAction(label="Voir les retards", actionType="navigate", payload={"path": "/manager/delays"})],
                )
            return ChatResponse(
                reply="Aucune livraison en retard pour le moment. Toutes les deadlines sont respectées.",
                intent=intent,
                confidence=conf,
                sources=["context:tasks"],
            )

        lines = [f"• #{t.id} — {t.label} — statut {t.status}" for t in delayed[:5]]
        reply = f"{len(delayed)} livraison(s) en retard :\n" + "\n".join(lines)
        actions = [
            ChatAction(label=f"Voir tâche #{t.id}", actionType="navigate", payload={"path": "/manager/tasks", "taskId": t.id})
            for t in delayed[:3]
        ]
        return ChatResponse(
            reply=reply,
            intent=intent,
            confidence=conf,
            sources=["context:tasks", "PostgreSQL:tasks"],
            actions=actions,
        )

    def _available_drivers(self, _msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        if not ctx.drivers:
            avail = ctx.stats.get("availableDrivers", "?")
            total = ctx.stats.get("totalDrivers", "?")
            return ChatResponse(
                reply=f"Chauffeurs disponibles : {avail}/{total}. Consultez la page Chauffeurs pour assigner.",
                intent=intent,
                confidence=conf,
                sources=["stats:drivers"],
                actions=[ChatAction(label="Gérer chauffeurs", actionType="navigate", payload={"path": "/manager/drivers"})],
            )

        available = [d for d in ctx.drivers if (d.status or "").upper() == "AVAILABLE"]
        lines = [f"• {d.label} — zone {d.extra.get('zone', 'N/A')} — charge {d.extra.get('load', 0)}" for d in available[:5]]
        reply = f"{len(available)} chauffeur(s) disponible(s) :\n" + "\n".join(lines) if lines else "Aucun chauffeur disponible actuellement."
        return ChatResponse(
            reply=reply,
            intent=intent,
            confidence=conf,
            sources=["context:drivers", "PostgreSQL:driver_profiles"],
            actions=[ChatAction(label="Assigner une tâche", actionType="navigate", payload={"path": "/manager/tasks"})],
        )

    def _order_tracking(self, _msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        if not ctx.orders:
            return ChatResponse(
                reply="Aucune commande trouvée dans votre contexte. Vérifiez la page Mes commandes.",
                intent=intent,
                confidence=conf,
                sources=["context:orders"],
                actions=[ChatAction(label="Mes commandes", actionType="navigate", payload={"path": self._orders_path(ctx.role)})],
            )

        lines = []
        actions = []
        for o in ctx.orders[:5]:
            eta = o.extra.get("estimatedMinutes", "N/A")
            lines.append(f"• Commande #{o.id} — {o.label} — {o.status}" + (f" — ETA ~{eta} min" if eta != "N/A" else ""))
            if o.extra.get("taskId"):
                actions.append(
                    ChatAction(
                        label=f"Suivre #{o.id}",
                        actionType="navigate",
                        payload={"path": f"/client/delivery/{o.extra['taskId']}"},
                    )
                )

        return ChatResponse(
            reply="Voici vos commandes :\n" + "\n".join(lines),
            intent=intent,
            confidence=conf,
            sources=["context:orders", "PostgreSQL:orders"],
            actions=actions[:3],
        )

    def _my_missions(self, _msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        active = [t for t in ctx.tasks if (t.status or "").upper() not in ("COMPLETED", "CANCELLED")]
        if not active:
            return ChatResponse(
                reply="Vous n'avez aucune mission active pour le moment.",
                intent=intent,
                confidence=conf,
                sources=["context:tasks"],
            )

        next_task = active[0]
        addr = next_task.extra.get("address", "Adresse non renseignée")
        reply = (
            f"Prochaine mission : #{next_task.id} — {next_task.label}\n"
            f"Statut : {next_task.status} — Adresse : {addr}\n"
            f"Total missions actives : {len(active)}"
        )
        return ChatResponse(
            reply=reply,
            intent=intent,
            confidence=conf,
            sources=[f"task:{next_task.id}"],
            actions=[
                ChatAction(label="Ouvrir mission", actionType="navigate", payload={"path": f"/driver/tasks/{next_task.id}"}),
                ChatAction(label="Mon itinéraire", actionType="navigate", payload={"path": "/driver/route"}),
            ],
        )

    def _dashboard(self, _msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        if not ctx.stats:
            return ChatResponse(
                reply="Résumé indisponible. Ouvrez le tableau de bord pour les KPI complets.",
                intent=intent,
                confidence=0.5,
                sources=["context:stats"],
            )

        lines = [f"• {k} : {v}" for k, v in ctx.stats.items()]
        return ChatResponse(
            reply="Résumé SmartTask :\n" + "\n".join(lines),
            intent=intent,
            confidence=conf,
            sources=["PostgreSQL:aggregates", "context:stats"],
            actions=[ChatAction(label="Tableau de bord", actionType="navigate", payload={"path": self._dashboard_path(ctx.role)})],
        )

    def _ai_info(self, _msg: str, _ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        faq = self._match_faq("ia prédiction")
        reply = faq or (
            "SmartTask AI utilise des modèles ML pour prédire les retards (Logistic Regression) "
            "et estimer les temps de livraison (XGBoost). Le manager peut analyser chaque tâche "
            "depuis Gestion des tâches → Analyser IA, ou consulter SmartTask AI."
        )
        return ChatResponse(
            reply=reply,
            intent=intent,
            confidence=conf,
            sources=["knowledge_base:faq", "smarttask-ai:models"],
            actions=[ChatAction(label="Page SmartTask AI", actionType="navigate", payload={"path": "/manager/ai"})],
        )

    def _help_workflow(self, msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        faq = self._match_faq(msg)
        if faq:
            return ChatResponse(
                reply=faq,
                intent=intent,
                confidence=conf,
                sources=["knowledge_base:faq"],
            )

        workflows = self._kb.get("workflows", {})
        reply = (
            f"Workflow commande : {workflows.get('order_lifecycle', 'N/A')}\n"
            f"Workflow tâche : {workflows.get('task_lifecycle', 'N/A')}\n"
            f"Votre rôle ({ctx.role}) : {workflows.get('roles', {}).get(ctx.role.upper(), 'Utilisateur SmartTask')}"
        )
        return ChatResponse(
            reply=reply,
            intent=intent,
            confidence=conf,
            sources=["knowledge_base:workflows"],
        )

    def _task_status(self, msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        match = re.search(r"#?(\d+)", msg)
        if match:
            task_id = int(match.group(1))
            task = next((t for t in ctx.tasks if t.id == task_id), None)
            if task:
                return ChatResponse(
                    reply=f"Tâche #{task.id} — {task.label} — Statut : {task.status}",
                    intent=intent,
                    confidence=0.9,
                    sources=[f"task:{task.id}"],
                )

        if ctx.tasks:
            t = ctx.tasks[0]
            return ChatResponse(
                reply=f"Dernière tâche contextuelle : #{t.id} — {t.label} — {t.status}. Précisez un numéro (#ID) pour plus de détail.",
                intent=intent,
                confidence=conf,
                sources=["context:tasks"],
            )

        return self._unknown(msg, ctx, intent, conf)

    def _unknown(self, msg: str, ctx: ChatContext, intent: ChatIntent, conf: float) -> ChatResponse:
        faq = self._match_faq(msg)
        if faq:
            return ChatResponse(
                reply=faq,
                intent=ChatIntent.HELP_WORKFLOW,
                confidence=0.7,
                sources=["knowledge_base:faq"],
            )

        return ChatResponse(
            reply=(
                "Je n'ai pas trouvé d'information précise pour cette question dans SmartTask. "
                "Essayez : « livraisons en retard », « mes missions », « où en est ma commande », "
                "ou « résumé du tableau de bord »."
            ),
            intent=ChatIntent.UNKNOWN,
            confidence=conf,
            sources=["knowledge_base:guardrails"],
            suggestions=self.get_suggestions(ctx.role).suggestions[:4],
        )

    def _orders_path(self, role: str) -> str:
        return {"CLIENT": "/client/orders", "OPERATOR": "/operator/orders"}.get(role.upper(), "/manager/tasks")

    def _dashboard_path(self, role: str) -> str:
        paths = {
            "MANAGER": "/manager/dashboard",
            "OPERATOR": "/operator/dashboard",
            "DRIVER": "/driver/dashboard",
            "CLIENT": "/client/dashboard",
            "ADMIN": "/admin/dashboard",
        }
        return paths.get(role.upper(), "/manager/dashboard")
