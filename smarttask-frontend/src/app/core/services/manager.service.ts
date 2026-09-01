import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  AIRecommendation,
  Analytics,
  Client,
  DelayedTask,
  Driver,
  IncidentItem,
  IncidentStatus,
  ManagerDashboard,
  NotificationItem,
  Operator,
  PageResponse
} from '../models/manager.models';

@Injectable({ providedIn: 'root' })
export class ManagerService {
  private base = `${environment.apiUrl}/manager`;

  constructor(private http: HttpClient) {}

  getDashboard(): Observable<ManagerDashboard> {
    return this.http.get<ManagerDashboard>(`${this.base}/dashboard`);
  }

  getDrivers(): Observable<Driver[]> {
    return this.http.get<Driver[]>(`${this.base}/drivers`);
  }

  getDriver(id: number): Observable<Driver> {
    return this.http.get<Driver>(`${this.base}/drivers/${id}`);
  }

  getClients(): Observable<Client[]> {
    return this.http.get<Client[]>(`${this.base}/clients`);
  }

  getOperators(): Observable<Operator[]> {
    return this.http.get<Operator[]>(`${this.base}/operators`);
  }

  getDelays(): Observable<DelayedTask[]> {
    return this.http.get<DelayedTask[]>(`${this.base}/delays`);
  }

  getNotifications(): Observable<NotificationItem[]> {
    return this.http.get<NotificationItem[]>(`${this.base}/notifications`);
  }

  markNotificationRead(id: number): Observable<{ message: string }> {
    return this.http.patch<{ message: string }>(`${this.base}/notifications/${id}/read`, {});
  }

  getAnalytics(): Observable<Analytics> {
    return this.http.get<Analytics>(`${this.base}/analytics`);
  }

  getAiRecommendations(): Observable<AIRecommendation[]> {
    return this.http.get<AIRecommendation[]>(`${this.base}/ai/recommendations`);
  }

  recommendDriver(taskId: number): Observable<AIRecommendation> {
    return this.http.get<AIRecommendation>(`${this.base}/ai/recommend-driver/${taskId}`);
  }

  getIncidents(status?: IncidentStatus, page = 0, size = 15): Observable<PageResponse<IncidentItem>> {
    let params = `?page=${page}&size=${size}`;
    if (status) params += `&status=${status}`;
    return this.http.get<PageResponse<IncidentItem>>(`${this.base}/incidents${params}`);
  }

  updateIncident(id: number, status: IncidentStatus, resolutionNote?: string): Observable<IncidentItem> {
    return this.http.patch<IncidentItem>(`${this.base}/incidents/${id}`, { status, resolutionNote });
  }

  exportAnalytics(): Observable<Blob> {
    return this.http.get(`${this.base}/analytics/export`, { responseType: 'blob' });
  }
}
