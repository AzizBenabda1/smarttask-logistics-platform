import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ClientService } from '../../../core/services/client.service';
import { Order } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <h1>Commande #{{ order?.id }}</h1>
  <div class="card" *ngIf="order as o">
    <p><strong>Produits:</strong> {{ o.products }} (x{{ o.quantity }})</p>
    <p><strong>Montant:</strong> {{ o.amount }} DT</p>
    <p><strong>Adresse:</strong> {{ o.deliveryAddress }}</p>
    <p><strong>Statut:</strong> <span class="badge" [ngClass]="o.status">{{ o.status }}</span></p>
    <p><strong>Instructions:</strong> {{ o.instructions || '—' }}</p>

    <div class="delivery-actions" *ngIf="o.taskId">
      <a [routerLink]="['/client/delivery', o.taskId]" class="btn-sm">Suivre la livraison</a>
      <a *ngIf="needsConfirm(o)" [routerLink]="['/client/delivery', o.taskId]" class="btn-sm btn-confirm">
        Confirmer la réception
      </a>
      <span *ngIf="o.clientConfirmed" class="ok">Réception déjà confirmée</span>
    </div>
    <p *ngIf="!o.taskId" class="hint">La livraison n'est pas encore lancée pour cette commande.</p>
  </div>
</div>`,
  styles: [`
.delivery-actions { margin-top:1.25rem; display:flex; flex-wrap:wrap; gap:.5rem; align-items:center; }
.btn-confirm { background:#16a34a; color:#fff; border-color:#16a34a; font-weight:600; }
.ok { color:#16a34a; font-weight:600; font-size:.875rem; }
.hint { color:#64748b; font-size:.875rem; margin-top:1rem; }
`]
})
export class ClientOrderDetailPageComponent implements OnInit {
  order: Order | null = null;
  constructor(private route: ActivatedRoute, private svc: ClientService) {}
  ngOnInit(): void {
    const id = +this.route.snapshot.paramMap.get('id')!;
    this.svc.getOrder(id).subscribe(o => this.order = o);
  }
  needsConfirm(o: Order): boolean {
    return o.status === 'DELIVERED' && o.taskStatus === 'COMPLETED' && !o.clientConfirmed;
  }
}
