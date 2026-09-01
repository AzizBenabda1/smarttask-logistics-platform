export interface ChatAction {
  label: string;
  actionType: string;
  payload: Record<string, unknown>;
}

export interface ChatHistoryItem {
  id: number;
  role: 'USER' | 'ASSISTANT';
  content: string;
  intent?: string;
  createdAt: string;
}

export interface ChatInit {
  sessionId: string;
  welcomeMessage: string;
  suggestions: string[];
  history: ChatHistoryItem[];
}

export interface ChatReply {
  reply: string;
  intent: string;
  confidence: number;
  sources: string[];
  actions: ChatAction[];
  suggestions: string[];
  proactive: boolean;
  sessionId: string;
  timestamp: string;
}

export interface ChatMessage {
  role: 'USER' | 'ASSISTANT';
  content: string;
  intent?: string;
  actions?: ChatAction[];
  sources?: string[];
  timestamp?: string;
}
