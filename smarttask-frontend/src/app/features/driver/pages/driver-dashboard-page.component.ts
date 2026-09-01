import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DriverService } from '../../../core/services/driver.service';
import { DriverDashboard } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Dashboard Chauffeur</h1>
      <p class="subtitle">Missions, itineraire et alertes IA</p>
    </div>
  </div>

  <div class="feature-banner">
    <p class="feature-banner-title">IA Chauffeur active</p>
    <div class="feature-banner-tags">
      <span class="feature-tag">Itineraire optimise</span>
      <span class="feature-tag">Alertes proactives</span>
    </div>
  </div>

  <div *ngIf="!d" class="skeleton-grid">
    <div class="skeleton-block" *ngFor="let i of [1,2,3,4,5]"></div>
  </div>

  <ng-container *ngIf="d as x">
    <div class="stat-grid">
      <div class="stat-card stat-icon-card">
        <div class="stat-label">Missions aujourd'hui</div>
        <div class="stat-value">{{ x.missionsToday }}</div>
        <span class="stat-icon-wrap">📋</span>
      </div>
      <div class="stat-card stat-warning stat-icon-card">
        <div class="stat-label">A accepter</div>
        <div class="stat-value">{{ x.toAccept }}</div>
        <span class="stat-icon-wrap">✋</span>
      </div>
      <div class="stat-card stat-icon-card">
        <div class="stat-label">En cours</div>
        <div class="stat-value">{{ x.inProgress }}</div>
        <span class="stat-icon-wrap">🚚</span>
      </div>
      <div class="stat-card stat-success stat-icon-card">
        <div class="stat-label">Terminees</div>
        <div class="stat-value">{{ x.completed }}</div>
        <span class="stat-icon-wrap">✓</span>
      </div>
      <div class="stat-card stat-danger stat-icon-card" *ngIf="x.delayed > 0">
        <div class="stat-label">Retards</div>
        <div class="stat-value">{{ x.delayed }}</div>
        <span class="stat-icon-wrap">⏱</span>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="card-header"><h2>Actions rapides</h2></div>
        <div class="card-body">
          <div class="quick-links">
            <a routerLink="/driver/tasks">Mes missions</a>
            <a routerLink="/driver/route">Itineraire IA</a>
            <a routerLink="/driver/performance">Performance</a>
          </div>
        </div>
      </div>

      <div class="card" *ngIf="x.notifications?.length">
        <div class="card-header">
          <h2>Alertes IA recentes</h2>
          <span class="badge badge-ai">IA</span>
        </div>
        <div class="card-body">
          <div class="alert-list">
            <div class="alert-item unread" *ngFor="let n of x.notifications">
              <div class="title">{{ n.title }}</div>
              <div class="msg">{{ n.message }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ng-container>
</div>`
})
export class DriverDashboardPageComponent implements OnInit {
  d: DriverDashboard | null = null;
  constructor(private svc: DriverService) {}
  ngOnInit(): void { this.svc.getDashboard().subscribe(r => this.d = r); }
}
