import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ChatService } from '../../../core/services/chat.service';
import { ChatInit, ChatReply, ChatAction, ChatMessage, ChatHistoryItem } from '../../../core/models/chat.models';

@Component({
  selector: 'app-chat-widget',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-widget.component.html',
  styleUrls: ['./chat-widget.component.scss']
})
export class ChatWidgetComponent implements OnInit {
  open = false;
  loading = false;
  sending = false;
  input = '';
  sessionId = '';
  suggestions: string[] = [];
  messages: ChatMessage[] = [];

  constructor(
    private chatService: ChatService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const saved = sessionStorage.getItem('st-chat-session');
    this.bootstrap(saved || undefined);
  }

  toggle(): void {
    this.open = !this.open;
    if (this.open && !this.messages.length) {
      this.bootstrap(this.sessionId || undefined);
    }
  }

  bootstrap(sessionId?: string): void {
    this.loading = true;
    this.chatService.init(sessionId).subscribe({
      next: (init: ChatInit) => {
        this.sessionId = init.sessionId;
        sessionStorage.setItem('st-chat-session', init.sessionId);
        this.suggestions = init.suggestions || [];
        if (init.history?.length) {
          this.messages = init.history.map((h: ChatHistoryItem) => ({
            role: h.role,
            content: h.content,
            intent: h.intent,
            timestamp: h.createdAt
          }));
        } else if (!this.messages.length) {
          this.messages = [{
            role: 'ASSISTANT',
            content: init.welcomeMessage
          }];
        }
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.messages = [{
          role: 'ASSISTANT',
          content: 'SmartTask Copilot est momentanément indisponible. Réessayez plus tard.'
        }];
      }
    });
  }

  send(text?: string): void {
    const message = (text ?? this.input).trim();
    if (!message || this.sending) return;

    this.messages.push({ role: 'USER', content: message });
    this.input = '';
    this.sending = true;

    this.chatService.sendMessage(message, this.sessionId).subscribe({
      next: (reply: ChatReply) => {
        this.sessionId = reply.sessionId;
        sessionStorage.setItem('st-chat-session', reply.sessionId);
        this.messages.push({
          role: 'ASSISTANT',
          content: reply.reply,
          intent: reply.intent,
          actions: reply.actions,
          sources: reply.sources,
          timestamp: reply.timestamp
        });
        if (reply.suggestions?.length) {
          this.suggestions = reply.suggestions;
        }
        this.sending = false;
      },
      error: () => {
        this.messages.push({
          role: 'ASSISTANT',
          content: 'Erreur de communication avec SmartTask Copilot. Vérifiez que le backend est démarré.'
        });
        this.sending = false;
      }
    });
  }

  useSuggestion(s: string): void {
    this.send(s);
  }

  runAction(action: ChatAction): void {
    if (action.actionType === 'navigate' && action.payload?.['path']) {
      this.router.navigateByUrl(String(action.payload['path']));
      this.open = false;
    }
  }

  formatContent(content: string): string {
    return content.replace(/\n/g, '<br>');
  }
}
