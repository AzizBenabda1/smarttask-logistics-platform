import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';
import {
  ClientDashboard, DeliveryTracking, Incident, IncidentRequest, NotificationItem, Order, Review, ReviewRequest, Task, TaskLiveUpdate
} from '../models/role.models';

@Injectable({ providedIn: 'root' })
export class ClientService {
  private base = `${environment.apiUrl}/client`;
  constructor(private http: HttpClient, private auth: AuthService) {}

  getDashboard(): Observable<ClientDashboard> { return this.http.get<ClientDashboard>(`${this.base}/dashboard`); }
  getOrders(): Observable<Order[]> { return this.http.get<Order[]>(`${this.base}/orders`); }
  getOrder(id: number): Observable<Order> { return this.http.get<Order>(`${this.base}/orders/${id}`); }
  getDelivery(taskId: number): Observable<DeliveryTracking> { return this.http.get<DeliveryTracking>(`${this.base}/deliveries/${taskId}`); }

  openDeliveryStream(taskId: number, onUpdate: (update: TaskLiveUpdate) => void): EventSource {
    const token = this.auth.getToken();
    const url = `${this.base}/deliveries/${taskId}/stream?token=${encodeURIComponent(token || '')}`;
    const source = new EventSource(url);
    source.addEventListener('update', (event: MessageEvent) => {
      try { onUpdate(JSON.parse(event.data) as TaskLiveUpdate); } catch { /* ignore */ }
    });
    return source;
  }

  confirmDelivery(taskId: number, comment?: string): Observable<Task> {
    return this.http.post<Task>(`${this.base}/deliveries/${taskId}/confirm`, { comment });
  }
  getNotifications(): Observable<NotificationItem[]> { return this.http.get<NotificationItem[]>(`${this.base}/notifications`); }
  getReviews(): Observable<Review[]> { return this.http.get<Review[]>(`${this.base}/reviews`); }
  createReview(data: ReviewRequest): Observable<Review> { return this.http.post<Review>(`${this.base}/reviews`, data); }
  createIncident(data: IncidentRequest): Observable<Incident> { return this.http.post<Incident>(`${this.base}/incidents`, data); }
}
