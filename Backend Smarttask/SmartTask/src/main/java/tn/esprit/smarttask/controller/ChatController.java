package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.dto.request.ChatSendRequest;
import tn.esprit.smarttask.dto.response.ChatHistoryItemResponse;
import tn.esprit.smarttask.dto.response.ChatInitResponse;
import tn.esprit.smarttask.dto.response.ChatReplyResponse;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.security.SecurityUtils;
import tn.esprit.smarttask.service.chat.ChatService;

import java.util.List;

@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
@Tag(name = "SmartTask Copilot", description = "Assistant conversationnel contextuel SmartTask")
@SecurityRequirement(name = "Bearer Authentication")
public class ChatController {

    private final ChatService chatService;

    @GetMapping("/init")
    @Operation(summary = "Initialiser une session de chat")
    public ResponseEntity<ChatInitResponse> init(@RequestParam(required = false) String sessionId) {
        User user = SecurityUtils.getCurrentUser();
        return ResponseEntity.ok(chatService.initSession(user, sessionId));
    }

    @PostMapping("/message")
    @Operation(summary = "Envoyer un message au copilot")
    public ResponseEntity<ChatReplyResponse> sendMessage(@Valid @RequestBody ChatSendRequest request) {
        User user = SecurityUtils.getCurrentUser();
        return ResponseEntity.ok(chatService.sendMessage(user, request));
    }

    @GetMapping("/history")
    @Operation(summary = "Historique des messages")
    public ResponseEntity<List<ChatHistoryItemResponse>> history(@RequestParam(required = false) String sessionId) {
        User user = SecurityUtils.getCurrentUser();
        return ResponseEntity.ok(chatService.getHistory(user, sessionId));
    }
}
