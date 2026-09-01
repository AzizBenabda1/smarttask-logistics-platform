package tn.esprit.smarttask.service.chat;

import org.springframework.stereotype.Component;
import tn.esprit.smarttask.dto.ai.AIChatResponse;
import tn.esprit.smarttask.dto.ai.AIChatSuggestionsResponse;
import tn.esprit.smarttask.entity.Role;
import tn.esprit.smarttask.entity.User;

import java.util.List;
import java.util.Locale;
import java.util.Map;

@Component
public class ChatFallbackService {

    private static final Map<Role, List<String>> SUGGESTIONS = Map.of(
            Role.MANAGER, List.of(
                    "Quelles livraisons sont en retard ?",
                    "Chauffeurs disponibles ?",
                    "Résumé du tableau de bord",
                    "Comment fonctionne SmartTask AI ?"),
            Role.OPERATOR, List.of(
                    "Commandes en attente ?",
                    "Comment valider une commande ?",
                    "Tâches à préparer aujourd'hui"),
            Role.DRIVER, List.of(
                    "Quelle est ma prochaine mission ?",
                    "Mes missions du jour",
                    "Comment signaler un incident ?"),
            Role.CLIENT, List.of(
                    "Où en est ma commande ?",
                    "Délai de livraison estimé",
                    "Comment confirmer ma réception ?"),
            Role.ADMIN, List.of(
                    "Résumé des opérations",
                    "Comment fonctionne SmartTask ?")
    );

    public AIChatSuggestionsResponse suggestions(Role role) {
        List<String> items = SUGGESTIONS.getOrDefault(role, SUGGESTIONS.get(Role.MANAGER));
        return AIChatSuggestionsResponse.builder()
                .suggestions(items)
                .welcomeMessage(
                        "Bonjour ! Je suis SmartTask Copilot. Je réponds uniquement dans le contexte SmartTask. Comment puis-je vous aider ?")
                .build();
    }

    public AIChatResponse reply(String message, User user) {
        String lower = message.toLowerCase(Locale.ROOT);
        String reply;
        String intent = "UNKNOWN";

        if (lower.matches(".*(bonjour|salut|hello|hey|coucou).*")) {
            reply = "Bonjour " + user.getFirstName()
                    + " ! Je suis SmartTask Copilot. Posez-moi une question sur vos livraisons, commandes ou missions.";
            intent = "GREETING";
        } else if (lower.matches(".*(retard|delayed|critique).*")) {
            reply = "Consultez la page Retards ou demandez un résumé du tableau de bord pour les livraisons en retard.";
            intent = "DELAYED_TASKS";
        } else if (lower.matches(".*(commande|livraison|suivre|tracking).*")) {
            reply = "Consultez Mes commandes ou Suivi livraison pour l'état de vos commandes SmartTask.";
            intent = "ORDER_TRACKING";
        } else if (lower.matches(".*(mission|tâche|task|prochaine).*")) {
            reply = "Consultez Mes missions pour voir vos tâches actives.";
            intent = "MY_MISSIONS";
        } else if (lower.matches(".*(ia|ai|intelligence|prédiction|prediction).*")) {
            reply = "SmartTask AI analyse les retards et recommande les chauffeurs. Accédez à SmartTask AI depuis le menu manager.";
            intent = "AI_INFO";
        } else if (lower.matches(".*(chauffeur|driver|dispo).*")) {
            reply = "Consultez la page Chauffeurs pour voir la disponibilité et assigner une livraison.";
            intent = "AVAILABLE_DRIVERS";
        } else {
            reply = "Je suis SmartTask Copilot. Je réponds uniquement sur les livraisons, commandes, tâches et l'IA SmartTask. "
                    + "Essayez : « livraisons en retard », « mes missions », « où en est ma commande ».";
            intent = "UNKNOWN";
        }

        return AIChatResponse.builder()
                .reply(reply)
                .intent(intent)
                .confidence(0.55)
                .sources(List.of("fallback:spring"))
                .actions(List.of())
                .suggestions(suggestions(user.getRole()).getSuggestions())
                .proactive(false)
                .build();
    }
}
