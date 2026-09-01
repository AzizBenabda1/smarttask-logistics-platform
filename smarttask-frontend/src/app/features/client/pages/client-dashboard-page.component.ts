import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ClientService } from '../../../core/services/client.service';
import { ClientDashboard } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Mon espace client</h1>
      <p class="subtitle">Suivi de vos commandes et livraisons</p>
    </div>
  </div>

  <div *ngIf="!d" class="skeleton-grid">
    <div class="skeleton-block" *ngFor="let i of [1,2,3]"></div>
  </div>

  <ng-container *ngIf="d as x">
    <div class="stat-grid">
      <div class="stat-card stat-icon-card">
        <div class="stat-label">Commandes actives</div>
        <div class="stat-value">{{ x.activeOrders }}</div>
        <span class="stat-icon-wrap">📦</span>
      </div>
      <div class="stat-card stat-success stat-icon-card">
        <div class="stat-label">Livrees</div>
        <div class="stat-value">{{ x.deliveredOrders }}</div>
        <span class="stat-icon-wrap">✓</span>
      </div>
      <div class="stat-card stat-icon-card">
        <div class="stat-label">Prochaines livraisons</div>
        <div class="stat-value">{{ x.upcomingDeliveries }}</div>
        <span class="stat-icon-wrap">📅</span>
      </div>
    </div>

    <div class="grid-2">
      <div class="card" *ngIf="x.lastOrder as o">
        <div class="card-header"><h2>Derniere commande</h2></div>
        <div class="card-body">
          <p style="margin:0 0 0.75rem"><strong>#{{ o.id }}</strong> — {{ o.products }}</p>
          <span class="badge" [ngClass]="o.status">{{ o.status }}</span>
          <div class="quick-links mt-2">
            <a [routerLink]="['/client/orders', o.id]">Voir detail</a>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header"><h2>Navigation</h2></div>
        <div class="card-body">
          <div class="quick-links">
            <a routerLink="/client/orders">Mes commandes</a>
            <a routerLink="/client/notifications">Notifications</a>
            <a routerLink="/client/reviews">Mes avis</a>
          </div>
        </div>
      </div>
    </div>
  </ng-container>
</div>`
})
export class ClientDashboardPageComponent implements OnInit {
  d: ClientDashboard | null = null;
  constructor(private svc: ClientService) {}
  ngOnInit(): void { this.svc.getDashboard().subscribe(r => this.d = r); }
}
