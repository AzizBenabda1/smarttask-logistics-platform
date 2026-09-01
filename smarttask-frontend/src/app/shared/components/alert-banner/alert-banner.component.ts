import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert-banner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="visible"
         class="alert-banner"
         [class.alert-banner-success]="type === 'success'"
         [class.alert-banner-error]="type === 'error'"
         [class.alert-banner-info]="type === 'info'"
         [class.alert-banner-warning]="type === 'warning'"
         [class.alert-banner-ai]="type === 'ai'"
         role="alert">
      <span class="alert-banner-icon">{{ iconChar }}</span>
      <div class="alert-banner-body">
        <strong *ngIf="title">{{ title }}</strong>
        <p>{{ message }}</p>
      </div>
      <button *ngIf="dismissible" type="button" class="alert-banner-close" (click)="close()">&times;</button>
    </div>
  `
})
export class AlertBannerComponent {
  @Input() type: 'success' | 'error' | 'info' | 'warning' | 'ai' = 'info';
  @Input() title = '';
  @Input() message = '';
  @Input() dismissible = true;
  @Output() dismissed = new EventEmitter<void>();

  visible = true;

  get iconChar(): string {
    switch (this.type) {
      case 'success': return '✓';
      case 'error': return '✕';
      case 'warning': return '⚠';
      case 'ai': return '✦';
      default: return 'ℹ';
    }
  }

  close(): void {
    this.visible = false;
    this.dismissed.emit();
  }
}
