import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  AIModelStatus,
  AIHealthStatus,
  AnomalyDetection,
  DelayPrediction,
  DeliveryTimePrediction,
  DeliverySuccessPrediction,
  DriverRecommendationAI,
  TaskAIAnalysis,
  TaskPrioritization
} from '../models/ai.models';

@Injectable({ providedIn: 'root' })
export class AiService {
  private base = `${environment.apiUrl}/manager/ai`;

  constructor(private http: HttpClient) {}

  health(): Observable<AIHealthStatus> {
    return this.http.get<AIHealthStatus>(`${this.base}/health`);
  }

  modelStatus(): Observable<AIModelStatus> {
    return this.http.get<AIModelStatus>(`${this.base}/model-status`);
  }

  analyzeTask(taskId: number): Observable<TaskAIAnalysis> {
    return this.http.post<TaskAIAnalysis>(`${this.base}/analyze`, { taskId });
  }

  predictDelay(taskId: number): Observable<DelayPrediction> {
    return this.http.post<DelayPrediction>(`${this.base}/predict-delay`, { taskId });
  }

  predictDeliveryTime(taskId: number): Observable<DeliveryTimePrediction> {
    return this.http.post<DeliveryTimePrediction>(`${this.base}/predict-delivery-time`, { taskId });
  }

  prioritizeTask(taskId: number): Observable<TaskPrioritization> {
    return this.http.post<TaskPrioritization>(`${this.base}/prioritize-task`, { taskId });
  }

  recommendDriver(taskId: number): Observable<DriverRecommendationAI> {
    return this.http.post<DriverRecommendationAI>(`${this.base}/recommend-driver`, { taskId });
  }

  detectAnomaly(taskId: number): Observable<AnomalyDetection> {
    return this.http.post<AnomalyDetection>(`${this.base}/detect-anomaly`, { taskId });
  }

  predictDeliverySuccess(taskId: number): Observable<DeliverySuccessPrediction> {
    return this.http.post<DeliverySuccessPrediction>(`${this.base}/predict-delivery-success`, { taskId });
  }
}
