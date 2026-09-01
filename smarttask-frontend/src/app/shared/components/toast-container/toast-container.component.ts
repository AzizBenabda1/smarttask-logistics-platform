import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastMessage, ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="toast-stack" aria-live="polite">
      <div *ngFor="let t of toasts"
           class="toast-item"
           [class.toast-success]="t.type === 'success'"
           [class.toast-error]="t.type === 'error'"
           [class.toast-info]="t.type === 'info'"
           [class.toast-warning]="t.type === 'warning'"
           (click)="dismiss(t.id)">
        <span class="toast-icon">{{ icon(t) }}</span>
        <span class="toast-text">{{ t.text }}</span>
        <button type="button" class="toast-close" aria-label="Fermer">&times;</button>
      </div>
    </div>
  `
})
export class ToastContainerComponent {
  toasts: ToastMessage[] = [];

  constructor(private toast: ToastService) {
    this.toast.toasts$.subscribe(list => this.toasts = list);
  }

  dismiss(id: number): void {
    this.toast.dismiss(id);
  }

  icon(t: ToastMessage): string {
    switch (t.type) {
      case 'success': return '✓';
      case 'error': return '!';
      case 'warning': return '⚠';
      default: return 'i';
    }
  }
}
