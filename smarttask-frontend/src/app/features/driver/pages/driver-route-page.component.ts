import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DriverService } from '../../../core/services/driver.service';
import { DriverRouteOptimization } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Mon itinéraire</h1>
      <p class="subtitle">Ordre optimal suggéré par l'IA SmartTask</p>
    </div>
  </div>

  <div class="card ai-banner" *ngIf="route && route.stops.length">
    <div class="ai-banner-row">
      <span class="badge badge-ai">{{ route.aiPowered ? 'IA ML' : 'IA Règles' }}</span>
      <strong>Gain estimé : −{{ route.estimatedTimeSavedMinutes }} min</strong>
    </div>
    <p>{{ route.summary }}</p>
    <p class="meta">Manuel ~{{ route.manualTotalMinutes }} min → Optimisé ~{{ route.optimizedTotalMinutes }} min</p>
  </div>

  <div class="list-cards" *ngIf="route?.stops?.length; else empty">
    <div class="list-card" *ngFor="let s of route!.stops">
      <div class="list-card-row">
        <div class="list-card-main">
          <h3 class="list-card-title">{{ s.order }}. Mission #{{ s.taskId }} — {{ s.title }}</h3>
          <p class="list-card-meta">{{ s.zone || 'Zone N/A' }} · {{ s.deliveryAddress }}</p>
          <p class="list-card-meta">~{{ s.estimatedMinutes }} min</p>
        </div>
        <div class="list-card-actions">
          <span class="badge" [class.badge-danger]="s.urgencyLabel === 'URGENT'"
            [class.badge-warning]="s.urgencyLabel === 'PRIORITAIRE'">{{ s.urgencyLabel }}</span>
          <a [href]="mapsUrl(s.deliveryAddress)" target="_blank" class="btn-sm">Maps</a>
          <a [routerLink]="['/driver/tasks', s.taskId]" class="btn-sm">Détail</a>
        </div>
      </div>
    </div>
  </div>

  <ng-template #empty>
    <div class="empty-state"><p>Aucune livraison planifiée</p></div>
  </ng-template>

  <p class="hint" *ngIf="error">{{ error }}</p>
</div>`,
  styles: [`
    .ai-banner { background: linear-gradient(135deg, #eff6ff, #f0fdf4); border: 1px solid #bfdbfe; margin-bottom: 1rem; }
    .ai-banner-row { display: flex; align-items: center; gap: .75rem; margin-bottom: .5rem; }
    .meta { font-size: .85rem; color: #64748b; margin: .25rem 0 0; }
    .hint { color: #dc2626; margin-top: 1rem; }
    .badge-ai { background: #7c3aed; color: #fff; }
  `]
})
export class DriverRoutePageComponent implements OnInit {
  route: DriverRouteOptimization | null = null;
  error = '';

  constructor(private svc: DriverService) {}

  ngOnInit(): void {
    this.svc.getOptimizedRoute().subscribe({
      next: r => this.route = r,
      error: () => this.error = 'Impossible de charger l\'itinéraire IA'
    });
  }

  mapsUrl(a: string): string {
    return 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(a);
  }
}
