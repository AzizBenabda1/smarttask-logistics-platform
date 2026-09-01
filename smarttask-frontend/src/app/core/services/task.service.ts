import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { PageResponse, Priority, Task, TaskHistory, TaskRequest, TaskStatus } from '../models/manager.models';

@Injectable({ providedIn: 'root' })
export class TaskService {
  private base = `${environment.apiUrl}/tasks`;

  constructor(private http: HttpClient) {}

  getPage(filters?: {
    status?: TaskStatus;
    priority?: Priority;
    driverId?: number;
    clientId?: number;
    date?: string;
    delayed?: boolean;
    search?: string;
    page?: number;
    size?: number;
  }): Observable<PageResponse<Task>> {
    let params = this.buildParams(filters);
    if (filters?.page != null) params = params.set('page', filters.page);
    if (filters?.size != null) params = params.set('size', filters.size);
    return this.http.get<PageResponse<Task>>(this.base, { params });
  }

  getAll(filters?: {
    status?: TaskStatus;
    priority?: Priority;
    driverId?: number;
    clientId?: number;
    date?: string;
    delayed?: boolean;
    search?: string;
  }): Observable<Task[]> {
    return this.getPage({ ...filters, page: 0, size: 200 }).pipe(map(p => p.content));
  }

  private buildParams(filters?: {
    status?: TaskStatus;
    priority?: Priority;
    driverId?: number;
    clientId?: number;
    date?: string;
    delayed?: boolean;
    search?: string;
  }): HttpParams {
    let params = new HttpParams();
    if (filters?.status) params = params.set('status', filters.status);
    if (filters?.priority) params = params.set('priority', filters.priority);
    if (filters?.driverId) params = params.set('driverId', filters.driverId);
    if (filters?.clientId) params = params.set('clientId', filters.clientId);
    if (filters?.date) params = params.set('date', filters.date);
    if (filters?.delayed != null) params = params.set('delayed', filters.delayed);
    if (filters?.search) params = params.set('search', filters.search);
    return params;
  }

  getById(id: number): Observable<Task> {
    return this.http.get<Task>(`${this.base}/${id}`);
  }

  getHistory(id: number): Observable<TaskHistory[]> {
    return this.http.get<TaskHistory[]>(`${this.base}/${id}/history`);
  }

  create(data: TaskRequest): Observable<Task> {
    return this.http.post<Task>(this.base, data);
  }

  update(id: number, data: TaskRequest): Observable<Task> {
    return this.http.put<Task>(`${this.base}/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }

  updateStatus(id: number, status: TaskStatus): Observable<Task> {
    return this.http.patch<Task>(`${this.base}/${id}/status`, { status });
  }

  updatePriority(id: number, priority: Priority): Observable<Task> {
    return this.http.patch<Task>(`${this.base}/${id}/priority`, { priority });
  }

  assignDriver(id: number, driverId: number): Observable<Task> {
    return this.http.post<Task>(`${this.base}/${id}/assign/${driverId}`, {});
  }

  assignRecommended(id: number): Observable<Task> {
    return this.http.post<Task>(`${this.base}/${id}/assign-recommended`, {});
  }
}
