import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ChatInit, ChatHistoryItem, ChatReply } from '../models/chat.models';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private base = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) {}

  init(sessionId?: string): Observable<ChatInit> {
    const params = sessionId ? { sessionId } : undefined;
    return this.http.get<ChatInit>(`${this.base}/init`, { params: params as Record<string, string> });
  }

  sendMessage(message: string, sessionId: string): Observable<ChatReply> {
    return this.http.post<ChatReply>(`${this.base}/message`, { message, sessionId });
  }

  history(sessionId?: string): Observable<ChatHistoryItem[]> {
    const params = sessionId ? { sessionId } : undefined;
    return this.http.get<ChatHistoryItem[]>(`${this.base}/history`, { params: params as Record<string, string> });
  }
}
