import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { Incident, IncidentRequest, OperatorDashboard, Order, OrderRequest, Task } from '../models/role.models';
import { PageResponse } from '../models/manager.models';
import { DeliverySuccessPrediction } from '../models/ai.models';

@Injectable({ providedIn: 'root' })
export class OperatorService {
  private base = `${environment.apiUrl}/operator`;
  constructor(private http: HttpClient) {}

  getDashboard(): Observable<OperatorDashboard> { return this.http.get<OperatorDashboard>(`${this.base}/dashboard`); }
  getOrdersPage(page = 0, size = 20, status?: string, clientId?: number): Observable<PageResponse<Order>> {
    let p = new HttpParams().set('page', page).set('size', size);
    if (status) p = p.set('status', status);
    if (clientId) p = p.set('clientId', clientId);
    return this.http.get<PageResponse<Order>>(`${this.base}/orders`, { params: p });
  }
  getOrders(status?: string, clientId?: number): Observable<Order[]> {
    return this.getOrdersPage(0, 200, status, clientId).pipe(
      map(r => r.content)
    );
  }
  getPendingOrders(): Observable<Order[]> { return this.http.get<Order[]>(`${this.base}/orders/pending`); }
  getOrder(id: number): Observable<Order> { return this.http.get<Order>(`${this.base}/orders/${id}`); }
  createOrder(data: OrderRequest): Observable<Order> { return this.http.post<Order>(`${this.base}/orders`, data); }
  updateOrder(id: number, data: OrderRequest): Observable<Order> { return this.http.put<Order>(`${this.base}/orders/${id}`, data); }
  verifyOrder(id: number): Observable<Order> { return this.http.post<Order>(`${this.base}/orders/${id}/verify`, {}); }
  getTasks(): Observable<Task[]> { return this.http.get<Task[]>(`${this.base}/tasks`); }
  prepareTask(orderId: number): Observable<Task> { return this.http.post<Task>(`${this.base}/tasks/${orderId}/prepare`, {}); }
  getClients(): Observable<{id:number;firstName:string;lastName:string;email:string}[]> {
    return this.http.get<{id:number;firstName:string;lastName:string;email:string}[]>(`${this.base}/clients`);
  }
  getIncidents(): Observable<Incident[]> { return this.http.get<Incident[]>(`${this.base}/incidents`); }
  createIncident(data: IncidentRequest): Observable<Incident> { return this.http.post<Incident>(`${this.base}/incidents`, data); }
  previewDeliverySuccess(data: OrderRequest): Observable<DeliverySuccessPrediction> {
    return this.http.post<DeliverySuccessPrediction>(`${this.base}/ai/delivery-success/preview`, data);
  }
}
