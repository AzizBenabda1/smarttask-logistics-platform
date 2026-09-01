import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  PasswordChangeRequest,
  Role,
  UpdateProfileRequest,
  User,
  UserRequest
} from '../models/auth.models';

@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getAll(search?: string, role?: Role): Observable<User[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    if (role) params = params.set('role', role);
    return this.http.get<User[]>(`${environment.apiUrl}/users`, { params });
  }

  getById(id: number): Observable<User> {
    return this.http.get<User>(`${environment.apiUrl}/users/${id}`);
  }

  create(user: UserRequest): Observable<User> {
    return this.http.post<User>(`${environment.apiUrl}/users`, user);
  }

  update(id: number, user: UserRequest): Observable<User> {
    return this.http.put<User>(`${environment.apiUrl}/users/${id}`, user);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}/users/${id}`);
  }

  updateStatus(id: number, active: boolean): Observable<User> {
    return this.http.patch<User>(`${environment.apiUrl}/users/${id}/status`, { active });
  }

  updateRole(id: number, role: Role): Observable<User> {
    return this.http.patch<User>(`${environment.apiUrl}/users/${id}/role`, { role });
  }

  getProfile(): Observable<User> {
    return this.http.get<User>(`${environment.apiUrl}/users/me`);
  }

  updateProfile(data: UpdateProfileRequest): Observable<User> {
    return this.http.put<User>(`${environment.apiUrl}/users/me`, data);
  }

  changePassword(data: PasswordChangeRequest): Observable<{ message: string }> {
    return this.http.patch<{ message: string }>(`${environment.apiUrl}/users/me/password`, data);
  }
}
