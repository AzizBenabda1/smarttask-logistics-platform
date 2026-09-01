import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { OperatorService } from '../../../core/services/operator.service';
import { Order } from '../../../core/models/role.models';
import { ViewToggleComponent, ViewMode } from '../../../shared/components/view-toggle/view-toggle.component';
import { ToastService } from '../../../shared/services/toast.service';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink, ViewToggleComponent],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Commandes</h1>
      <p class="subtitle">{{ totalElements }} commande(s) au total</p>
    </div>
    <div class="page-actions">
      <app-view-toggle [mode]="viewMode" (modeChange)="viewMode = $event"></app-view-toggle>
      <a routerLink="/operator/orders/create" class="btn btn-primary">Nouvelle commande</a>
    </div>
  </div>

  <!-- Vue cartes -->
  <div class="card-grid" *ngIf="viewMode === 'cards'">
    <div class="tile-card" *ngFor="let o of orders">
      <div class="tile-header">
        <div>
          <h3 class="tile-title">Commande #{{ o.id }}</h3>
          <p class="tile-subtitle">{{ o.clientName }}</p>
        </div>
        <span class="badge" [ngClass]="o.status">{{ o.status }}</span>
      </div>
      <div class="tile-body">
        <div class="list-card-details" style="border:none;padding:0">
          <div class="meta-item">
            <span class="meta-label">Produit</span>
            <span class="meta-value">{{ o.productTypeName || 'Autre' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Montant</span>
            <span class="meta-value">{{ o.amount }} DT</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Priorite</span>
            <span class="meta-value"><span class="badge" [ngClass]="o.priority">{{ o.priority }}</span></span>
          </div>
        </div>
      </div>
      <div class="tile-footer">
        <button class="btn-sm" *ngIf="o.status==='PENDING'" (click)="verify(o)">Valider</button>
        <button class="btn-sm btn-ai" *ngIf="o.status==='VERIFIED'" (click)="prepare(o)">Preparer</button>
      </div>
    </div>
    <div class="empty-state" *ngIf="!orders.length" style="grid-column:1/-1">
      <p class="empty-title">Aucune commande</p>
      <p>Creez une nouvelle commande pour commencer.</p>
    </div>
  </div>

  <!-- Vue liste -->
  <div class="list-cards" *ngIf="viewMode === 'list'">
    <div class="list-card" *ngFor="let o of orders">
      <div class="list-card-row">
        <div class="list-card-main">
          <h3 class="list-card-title">Commande #{{ o.id }}</h3>
          <p class="list-card-meta">{{ o.clientName }} · {{ o.productTypeName || 'Autre' }} · {{ o.products }}</p>
        </div>
        <span class="badge" [ngClass]="o.status">{{ o.status }}</span>
        <span class="badge" [ngClass]="o.priority">{{ o.priority }}</span>
        <div class="list-card-actions">
          <span class="meta-value" style="font-weight:700">{{ o.amount }} DT</span>
          <button class="btn-sm" *ngIf="o.status==='PENDING'" (click)="verify(o)">Valider</button>
          <button class="btn-sm btn-ai" *ngIf="o.status==='VERIFIED'" (click)="prepare(o)">Preparer</button>
        </div>
      </div>
    </div>
    <div class="empty-state" *ngIf="!orders.length">
      <p class="empty-title">Aucune commande</p>
    </div>
  </div>

  <div class="pagination" *ngIf="totalPages > 1">
    <span class="pagination-info">Page {{ page + 1 }} sur {{ totalPages }}</span>
    <div class="pagination-controls">
      <button class="btn btn-secondary" (click)="prev()" [disabled]="page===0">Precedent</button>
      <button class="btn btn-secondary" (click)="next()" [disabled]="page >= totalPages - 1">Suivant</button>
    </div>
  </div>
</div>`
})
export class OperatorOrdersPageComponent implements OnInit {
  orders: Order[] = [];
  page = 0;
  totalPages = 0;
  totalElements = 0;
  viewMode: ViewMode = 'cards';

  constructor(private svc: OperatorService, private toast: ToastService) {}

  ngOnInit(): void { this.load(); }

  load(): void {
    this.svc.getOrdersPage(this.page, 15).subscribe(r => {
      this.orders = r.content;
      this.totalPages = r.totalPages;
      this.totalElements = r.totalElements;
    });
  }

  prev(): void { if (this.page > 0) { this.page--; this.load(); } }
  next(): void { if (this.page < this.totalPages - 1) { this.page++; this.load(); } }

  verify(o: Order): void {
    this.svc.verifyOrder(o.id).subscribe({
      next: () => { this.toast.success(`Commande #${o.id} verifiee`); this.load(); },
      error: e => this.toast.error(e.error?.message || 'Erreur validation')
    });
  }

  prepare(o: Order): void {
    this.svc.prepareTask(o.id).subscribe({
      next: () => { this.toast.success(`Tache preparee pour commande #${o.id}`); this.load(); },
      error: e => this.toast.error(e.error?.message || 'Erreur preparation')
    });
  }
}
