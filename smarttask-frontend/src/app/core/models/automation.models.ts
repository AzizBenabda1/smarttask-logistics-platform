export interface AutomationLog {
  id: number;
  runId: string;
  chainType: string;
  orderId?: number;
  taskId?: number;
  stepNumber: number;
  stepName: string;
  status: string;
  message: string;
  createdAt: string;
}

export interface ExpressChainResult {
  runId: string;
  orderId: number;
  taskId?: number;
  success: boolean;
  summary: string;
  steps: AutomationLog[];
}

export interface AutomationStatus {
  expressEnabled: boolean;
  minDriverScore: number;
  autoTriggerPriorities: string;
  chainName: string;
  stepCount: number;
}
