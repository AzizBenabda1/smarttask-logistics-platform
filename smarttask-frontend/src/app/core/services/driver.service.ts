import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DriverDashboard, DriverPerformance, DriverRouteOptimization, Incident, IncidentRequest, Task } from '../models/role.models';

@Injectable({ providedIn: 'root' })
export class DriverService {
  private base = `${environment.apiUrl}/driver`;
  constructor(private http: HttpClient) {}

  getDashboard(): Observable<DriverDashboard> { return this.http.get<DriverDashboard>(`${this.base}/dashboard`); }
  getTasks(): Observable<Task[]> { return this.http.get<Task[]>(`${this.base}/tasks`); }
  getTask(id: number): Observable<Task> { return this.http.get<Task>(`${this.base}/tasks/${id}`); }
  accept(id: number): Observable<Task> { return this.http.patch<Task>(`${this.base}/tasks/${id}/accept`, {}); }
  start(id: number): Observable<Task> { return this.http.patch<Task>(`${this.base}/tasks/${id}/start`, {}); }
  inDelivery(id: number): Observable<Task> { return this.http.patch<Task>(`${this.base}/tasks/${id}/delivery`, {}); }
  complete(id: number): Observable<Task> { return this.http.patch<Task>(`${this.base}/tasks/${id}/complete`, {}); }
  updateLocation(id: number, latitude: number, longitude: number): Observable<Task> {
    return this.http.patch<Task>(`${this.base}/tasks/${id}/location`, { latitude, longitude });
  }
  uploadProof(id: number, imageBase64: string, note?: string): Observable<Task> {
    return this.http.post<Task>(`${this.base}/tasks/${id}/proof`, { imageBase64, note });
  }
  getRoute(): Observable<Task[]> { return this.http.get<Task[]>(`${this.base}/route`); }
  getOptimizedRoute(): Observable<DriverRouteOptimization> {
    return this.http.get<DriverRouteOptimization>(`${this.base}/route/optimized`);
  }
  triggerAlerts(): Observable<{ alertsSent: number }> {
    return this.http.post<{ alertsSent: number }>(`${this.base}/alerts/check`, {});
  }
  getHistory(): Observable<Task[]> { return this.http.get<Task[]>(`${this.base}/history`); }
  getPerformance(): Observable<DriverPerformance> { return this.http.get<DriverPerformance>(`${this.base}/performance`); }
  createIncident(data: IncidentRequest): Observable<Incident> { return this.http.post<Incident>(`${this.base}/incidents`, data); }
}
