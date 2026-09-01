import { RiskLevel } from './manager.models';

export interface TaskIdRequest {
  taskId: number;
}

export interface TaskAIAnalysis {
  taskId: number;
  delayProbability: number;
  riskLevel: RiskLevel;
  estimatedDeliveryTimeMinutes: number;
  deliveryTimeUnit?: string;
  priorityScore?: number;
  recommendedPriority?: string;
  explanation: string[];
  delayModelVersion?: string;
  deliveryTimeModelVersion?: string;
  aiServiceAvailable?: boolean;
}

export interface DelayPrediction {
  taskId: number;
  delayProbability: number;
  riskLevel: RiskLevel;
  modelVersion?: string;
  explanation: string[];
}

export interface DeliveryTimePrediction {
  taskId: number;
  estimatedDeliveryTime: number;
  unit: string;
  modelVersion?: string;
  explanation: string[];
}

export interface TaskPrioritization {
  taskId: number;
  priorityScore: number;
  recommendedPriority: string;
  reason: string;
  scoringMethod?: string;
}

export interface DriverRecommendationAI {
  taskId: number;
  recommendedDriverId: number;
  score: number;
  reasons: string[];
  scoringMethod?: string;
  modelVersion?: string;
}

export interface AnomalyDetection {
  anomaly: boolean;
  score: number;
  reason: string;
  explanation: string[];
}

export interface AIHealthStatus {
  status: string;
  service: string;
  version: string;
}

export interface AIModelStatus {
  delayModel: string;
  deliveryTimeModel: string;
  deliverySuccessModel?: string;
  priorityModel: string;
  modelsPath?: string;
}

export interface DeliverySuccessPrediction {
  taskId?: number;
  referenceId?: string;
  successProbability: number;
  riskLevel: RiskLevel;
  factors: string[];
  suggestedActions: string[];
  modelVersion?: string;
  explanation: string[];
  ruleBased?: boolean;
}
