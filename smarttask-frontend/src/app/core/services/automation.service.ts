import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AutomationLog, AutomationStatus, ExpressChainResult } from '../models/automation.models';

@Injectable({ providedIn: 'root' })
export class AutomationService {
  private base = `${environment.apiUrl}/automation`;

  constructor(private http: HttpClient) {}

  status(): Observable<AutomationStatus> {
    return this.http.get<AutomationStatus>(`${this.base}/status`);
  }

  runExpress(orderId: number): Observable<ExpressChainResult> {
    return this.http.post<ExpressChainResult>(`${this.base}/express/${orderId}`, {});
  }

  logs(): Observable<AutomationLog[]> {
    return this.http.get<AutomationLog[]>(`${this.base}/logs`);
  }

  logsByRun(runId: string): Observable<AutomationLog[]> {
    return this.http.get<AutomationLog[]>(`${this.base}/logs/run/${runId}`);
  }
}
