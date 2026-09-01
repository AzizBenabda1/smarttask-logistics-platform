import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface ProductType {
  id: number;
  code: string;
  name: string;
  description?: string;
}

@Injectable({ providedIn: 'root' })
export class ProductTypeService {
  private base = `${environment.apiUrl}/product-types`;

  constructor(private http: HttpClient) {}

  list(): Observable<ProductType[]> {
    return this.http.get<ProductType[]>(this.base);
  }
}
