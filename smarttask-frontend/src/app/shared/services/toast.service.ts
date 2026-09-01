import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastMessage {
  id: number;
  text: string;
  type: ToastType;
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  private seq = 0;
  private readonly messages$ = new BehaviorSubject<ToastMessage[]>([]);
  readonly toasts$ = this.messages$.asObservable();

  show(text: string, type: ToastType = 'info', durationMs = 4500): void {
    const id = ++this.seq;
    const next = [...this.messages$.value, { id, text, type }];
    this.messages$.next(next);
    if (durationMs > 0) {
      setTimeout(() => this.dismiss(id), durationMs);
    }
  }

  success(text: string): void { this.show(text, 'success'); }
  error(text: string): void { this.show(text, 'error', 6000); }
  info(text: string): void { this.show(text, 'info'); }
  warning(text: string): void { this.show(text, 'warning', 5500); }

  dismiss(id: number): void {
    this.messages$.next(this.messages$.value.filter(t => t.id !== id));
  }
}
