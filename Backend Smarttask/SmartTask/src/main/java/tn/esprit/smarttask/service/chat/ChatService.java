package tn.esprit.smarttask.service.chat;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.client.SmartTaskAIClient;
import tn.esprit.smarttask.config.AIProperties;
import tn.esprit.smarttask.dto.ai.AIChatRequest;
import tn.esprit.smarttask.dto.ai.AIChatResponse;
import tn.esprit.smarttask.dto.ai.AIChatSuggestionsResponse;
import tn.esprit.smarttask.dto.request.ChatSendRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.ChatMessage;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;
import tn.esprit.smarttask.repository.ChatMessageRepository;

import java.time.LocalDateTime;
import java.util.Comparator;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class ChatService {

    private final ChatMessageRepository chatMessageRepository;
    private final ChatContextBuilderService contextBuilder;
    private final SmartTaskAIClient aiClient;
    private final AIProperties aiProperties;
    private final ChatFallbackService fallbackService;

    @Transactional
    public ChatInitResponse initSession(User user, String sessionId) {
        String sid = sessionId != null && !sessionId.isBlank() ? sessionId : UUID.randomUUID().toString();
        AIChatSuggestionsResponse suggestions = fetchSuggestions(user);

        List<ChatHistoryItemResponse> history = chatMessageRepository
                .findTop30ByUserIdAndSessionIdOrderByCreatedAtAsc(user.getId(), sid)
                .stream()
                .map(this::toHistoryItem)
                .toList();

        return ChatInitResponse.builder()
                .sessionId(sid)
                .welcomeMessage(suggestions.getWelcomeMessage())
                .suggestions(suggestions.getSuggestions())
                .history(history)
                .build();
    }

    @Transactional
    public ChatReplyResponse sendMessage(User user, ChatSendRequest request) {
        String sessionId = request.getSessionId() != null && !request.getSessionId().isBlank()
                ? request.getSessionId()
                : UUID.randomUUID().toString();

        saveMessage(user, ChatMessage.MessageRole.USER, request.getMessage(), null, sessionId);

        AIChatRequest aiRequest = AIChatRequest.builder()
                .message(request.getMessage())
                .context(contextBuilder.buildContext(user))
                .sessionId(sessionId)
                .build();

        AIChatResponse aiResponse = resolveResponse(aiRequest, user);

        saveMessage(user, ChatMessage.MessageRole.ASSISTANT, aiResponse.getReply(),
                aiResponse.getIntent(), sessionId);

        return toReplyResponse(aiResponse, sessionId);
    }

    @Transactional(readOnly = true)
    public List<ChatHistoryItemResponse> getHistory(User user, String sessionId) {
        if (sessionId == null || sessionId.isBlank()) {
            return chatMessageRepository.findTop30ByUserIdOrderByCreatedAtDesc(user.getId())
                    .stream()
                    .sorted(Comparator.comparing(ChatMessage::getCreatedAt))
                    .map(this::toHistoryItem)
                    .toList();
        }
        return chatMessageRepository.findTop30ByUserIdAndSessionIdOrderByCreatedAtAsc(user.getId(), sessionId)
                .stream()
                .map(this::toHistoryItem)
                .toList();
    }

    private AIChatResponse resolveResponse(AIChatRequest aiRequest, User user) {
        if (aiProperties.isEnabled()) {
            try {
                return aiClient.chat(aiRequest);
            } catch (AIServiceUnavailableException ex) {
                log.warn("Chat AI unavailable, using fallback: {}", ex.getMessage());
            }
        }
        return fallbackService.reply(aiRequest.getMessage(), user);
    }

    private AIChatSuggestionsResponse fetchSuggestions(User user) {
        if (aiProperties.isEnabled()) {
            try {
                return aiClient.chatSuggestions(user.getRole().name());
            } catch (Exception ex) {
                log.warn("Chat suggestions unavailable: {}", ex.getMessage());
            }
        }
        return fallbackService.suggestions(user.getRole());
    }

    private void saveMessage(User user, ChatMessage.MessageRole role, String content, String intent, String sessionId) {
        chatMessageRepository.save(ChatMessage.builder()
                .user(user)
                .role(role)
                .content(content)
                .intent(intent)
                .sessionId(sessionId)
                .build());
    }

    private ChatHistoryItemResponse toHistoryItem(ChatMessage m) {
        return ChatHistoryItemResponse.builder()
                .id(m.getId())
                .role(m.getRole().name())
                .content(m.getContent())
                .intent(m.getIntent())
                .createdAt(m.getCreatedAt())
                .build();
    }

    private ChatReplyResponse toReplyResponse(AIChatResponse ai, String sessionId) {
        List<ChatActionResponse> actions = ai.getActions() != null
                ? ai.getActions().stream().map(a -> ChatActionResponse.builder()
                .label(a.getLabel())
                .actionType(a.getActionType())
                .payload(a.getPayload())
                .build()).toList()
                : List.of();

        return ChatReplyResponse.builder()
                .reply(ai.getReply())
                .intent(ai.getIntent())
                .confidence(ai.getConfidence())
                .sources(ai.getSources() != null ? ai.getSources() : List.of())
                .actions(actions)
                .suggestions(ai.getSuggestions() != null ? ai.getSuggestions() : List.of())
                .proactive(ai.isProactive())
                .sessionId(sessionId)
                .timestamp(LocalDateTime.now())
                .build();
    }
}
