import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OperatorService } from '../../../core/services/operator.service';
import { Order } from '../../../core/models/role.models';

@Component({
  standalone: true, imports: [CommonModule],
  template: `
<div class="page"><h1>Vérification commandes</h1>
<div class="card table-wrap"><table>
<thead><tr><th>Client</th><th>Produits</th><th>Adresse</th><th>Téléphone</th><th>Actions</th></tr></thead>
<tbody><tr *ngFor="let o of orders">
  <td>{{ o.clientName }}</td><td>{{ o.products }} (x{{ o.quantity }})</td><td>{{ o.deliveryAddress }}</td><td>{{ o.phone }}</td>
  <td><button class="btn-sm" (click)="verify(o)">Valider</button></td>
</tr></tbody></table>
<div *ngIf="!orders.length" class="empty">Aucune commande en attente</div></div></div>`
})
export class OperatorPendingPageComponent implements OnInit {
  orders: Order[] = [];
  constructor(private svc: OperatorService) {}
  ngOnInit(): void { this.svc.getPendingOrders().subscribe(r => this.orders = r); }
  verify(o: Order): void { this.svc.verifyOrder(o.id).subscribe(() => this.ngOnInit()); }
}
