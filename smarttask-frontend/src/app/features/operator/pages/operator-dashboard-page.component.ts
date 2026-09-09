import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { OperatorService } from '../../../core/services/operator.service';
import { OperatorDashboard } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Dashboard Operateur</h1>
      <p class="subtitle">Operations et commandes du jour</p>
    </div>
    <div class="page-actions">
      <a routerLink="/operator/orders/pending" class="btn btn-primary">Verifier commandes</a>
    </div>
  </div>

  <div class="feature-banner">
    <p class="feature-banner-title">Flux commande</p>
    <div class="feature-banner-tags">
      <span class="feature-tag">Client cree</span>
      <span class="feature-tag">Operateur valide ou annule</span>
      <span class="feature-tag">Manager prepare et affecte</span>
    </div>
  </div>

  <div *ngIf="!d" class="skeleton-grid">
    <div class="skeleton-block" *ngFor="let i of [1,2,3,4,5,6]"></div>
  </div>

  <ng-container *ngIf="d as x">
    <div class="stat-grid">
      <div class="stat-card stat-icon-card">
        <div class="stat-label">Commandes aujourd'hui</div>
        <div class="stat-value">{{ x.ordersToday }}</div>
        <span class="stat-icon-wrap">📦</span>
      </div>
      <div class="stat-card stat-warning stat-icon-card">
        <div class="stat-label">En attente</div>
        <div class="stat-value">{{ x.pendingOrders }}</div>
        <span class="stat-icon-wrap">⏳</span>
      </div>
      <div class="stat-card stat-icon-card">
        <div class="stat-label">Verifiees</div>
        <div class="stat-value">{{ x.verifiedOrders }}</div>
        <span class="stat-icon-wrap">✓</span>
      </div>
      <div class="stat-card stat-success stat-icon-card">
        <div class="stat-label">Pretes</div>
        <div class="stat-value">{{ x.readyOrders }}</div>
        <span class="stat-icon-wrap">🚀</span>
      </div>
      <div class="stat-card stat-icon-card">
        <div class="stat-label">Livraisons en cours</div>
        <div class="stat-value">{{ x.deliveriesInProgress }}</div>
        <span class="stat-icon-wrap">🚚</span>
      </div>
      <div class="stat-card stat-danger stat-icon-card" *ngIf="x.openIncidents > 0">
        <div class="stat-label">Incidents ouverts</div>
        <div class="stat-value">{{ x.openIncidents }}</div>
        <span class="stat-icon-wrap">⚠</span>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h2>Actions rapides</h2></div>
      <div class="card-body">
        <div class="quick-links">
          <a routerLink="/operator/orders/pending">
            Verifier commandes
            <span>{{ x.pendingOrders }} en attente</span>
          </a>
          <a routerLink="/operator/orders">
            Toutes les commandes
            <span>Suivi complet</span>
          </a>
          <a routerLink="/operator/tasks">
            Taches
            <span>Suivi livraisons</span>
          </a>
          <a routerLink="/operator/incidents">
            Incidents
            <span *ngIf="x.openIncidents">{{ x.openIncidents }} ouvert(s)</span>
            <span *ngIf="!x.openIncidents">Aucun incident</span>
          </a>
        </div>
      </div>
    </div>
  </ng-container>
</div>`
})
export class OperatorDashboardPageComponent implements OnInit {
  d: OperatorDashboard | null = null;
  constructor(private svc: OperatorService) {}
  ngOnInit(): void { this.svc.getDashboard().subscribe(r => this.d = r); }
}
