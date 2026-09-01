import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ClientService } from '../../../core/services/client.service';
import { Order } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Mes commandes</h1>
      <p class="subtitle">Suivez vos livraisons en temps réel</p>
    </div>
  </div>

  <div class="list-cards">
    <div class="list-card" *ngFor="let o of orders">
      <div class="list-card-row">
        <div class="list-card-main">
          <h3 class="list-card-title">{{ o.products }}</h3>
          <p class="list-card-meta">{{ o.createdAt | date:'mediumDate' }} · {{ o.amount }} DT</p>
        </div>
        <span class="badge" [ngClass]="o.status">{{ o.status }}</span>
      </div>
      <div class="list-card-details">
        <div class="meta-item">
          <span class="meta-label">Actions</span>
          <div class="list-card-actions">
            <a *ngIf="o.taskId" [routerLink]="['/client/delivery', o.taskId]" class="btn-sm">Suivre</a>
            <a *ngIf="needsConfirm(o)" [routerLink]="['/client/delivery', o.taskId]" class="btn-sm btn-confirm">Confirmer réception</a>
            <a [routerLink]="['/client/orders', o.id]" class="btn-sm">Détail</a>
            <span *ngIf="!o.taskId" class="text-muted">En préparation</span>
          </div>
        </div>
      </div>
    </div>
    <div class="empty-state" *ngIf="!orders.length">
      <p class="empty-title">Aucune commande</p>
      <p>Vos commandes apparaîtront ici.</p>
    </div>
  </div>
</div>`,
  styles: [`
.btn-confirm { background: var(--st-success); color: #fff; border-color: var(--st-success); }
.btn-confirm:hover { background: #047857; }
`]
})
export class ClientOrdersPageComponent implements OnInit {
  orders: Order[] = [];
  constructor(private svc: ClientService) {}
  ngOnInit(): void { this.svc.getOrders().subscribe(r => this.orders = r); }

  needsConfirm(o: Order): boolean {
    return !!o.taskId && o.status === 'DELIVERED' && o.taskStatus === 'COMPLETED' && !o.clientConfirmed;
  }
}
