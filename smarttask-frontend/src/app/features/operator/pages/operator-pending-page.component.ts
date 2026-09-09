import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OperatorService } from '../../../core/services/operator.service';
import { Order } from '../../../core/models/role.models';
import { ToastService } from '../../../shared/services/toast.service';

@Component({
  standalone: true, imports: [CommonModule],
  template: `
<div class="page">
  <h1>Verification commandes</h1>
  <p class="subtitle">Validez ou annulez les commandes clients avant transmission au manager</p>
  <div class="card table-wrap"><table>
    <thead><tr><th>Client</th><th>Produits</th><th>Adresse</th><th>Telephone</th><th>Actions</th></tr></thead>
    <tbody><tr *ngFor="let o of orders">
      <td>{{ o.clientName }}</td><td>{{ o.products }} (x{{ o.quantity }})</td><td>{{ o.deliveryAddress }}</td><td>{{ o.phone }}</td>
      <td class="list-card-actions">
        <button class="btn-sm" (click)="verify(o)">Valider</button>
        <button class="btn-sm btn-danger" (click)="cancel(o)">Annuler</button>
      </td>
    </tr></tbody></table>
    <div *ngIf="!orders.length" class="empty">Aucune commande en attente</div>
  </div>
</div>`
})
export class OperatorPendingPageComponent implements OnInit {
  orders: Order[] = [];
  constructor(private svc: OperatorService, private toast: ToastService) {}
  ngOnInit(): void { this.load(); }
  load(): void { this.svc.getPendingOrders().subscribe(r => this.orders = r); }

  verify(o: Order): void {
    this.svc.verifyOrder(o.id).subscribe({
      next: () => { this.toast.success(`Commande #${o.id} validee`); this.load(); },
      error: e => this.toast.error(e.error?.message || 'Erreur')
    });
  }

  cancel(o: Order): void {
    if (!confirm(`Annuler la commande #${o.id} ?`)) return;
    this.svc.cancelOrder(o.id).subscribe({
      next: () => { this.toast.success(`Commande #${o.id} annulee`); this.load(); },
      error: e => this.toast.error(e.error?.message || 'Erreur')
    });
  }
}
