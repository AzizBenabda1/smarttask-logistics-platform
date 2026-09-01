import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ClientService } from '../../../core/services/client.service';
import { DeliveryTracking } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
<div class="page">
  <h1>Suivi livraison <span class="live" *ngIf="liveConnected">● LIVE</span></h1>
  <div class="card" *ngIf="d as x">
    <p><strong>Statut:</strong> <span class="badge" [ngClass]="x.currentStatus">{{ x.currentStatus }}</span></p>
    <p><strong>Chauffeur:</strong> {{ x.driverName || 'Non affecté' }}</p>
    <p><strong>Arrivée estimée:</strong> {{ x.estimatedArrival | date:'short' }}</p>
    <p *ngIf="x.latitude != null"><strong>Position GPS:</strong> {{ x.latitude }}, {{ x.longitude }}</p>
    <p *ngIf="x.hasProofOfDelivery" class="ok-msg">📷 Preuve de livraison reçue du chauffeur</p>
    <p *ngIf="lastEvent" class="hint">Dernière mise à jour: {{ lastEvent }}</p>
    <div style="margin:1.5rem 0">
      <div *ngFor="let s of x.timeline" style="padding:.5rem 0;border-left:3px solid"
        [style.borderColor]="s.completed ? '#22c55e' : '#e2e8f0'" [style.paddingLeft]="'1rem'">
        {{ s.label }} {{ s.current ? '← actuel' : '' }}
      </div>
    </div>
    <div *ngIf="canConfirm(x)" class="confirm-box">
      <h2>Confirmer la réception</h2>
      <input [formControl]="comment" placeholder="Commentaire (optionnel)" class="confirm-input" />
      <button class="btn btn-primary" (click)="confirm()" [disabled]="confirming">Confirmer la réception</button>
      <p *ngIf="error" class="error">{{ error }}</p>
    </div>
    <p *ngIf="x.clientConfirmed" class="ok-msg">Réception confirmée (RECEIVED)</p>
    <p *ngIf="x.clientConfirmed"><a routerLink="/client/reviews" class="btn btn-primary btn-sm">Évaluer</a></p>
  </div>
  <p *ngIf="loadError" class="error">{{ loadError }}</p>
</div>`,
  styles: [`
.live { color:#16a34a; font-size:.85rem; font-weight:600; }
.confirm-box { margin-top:1rem; padding:1rem; background:#f0fdf4; border-radius:8px; }
.confirm-input { width:100%; padding:.5rem; margin:.75rem 0; box-sizing:border-box; }
.ok-msg { color:#16a34a; font-weight:600; }
.hint { color:#64748b; font-size:.85rem; }
.error { color:#dc2626; }
`]
})
export class ClientDeliveryPageComponent implements OnInit, OnDestroy {
  d: DeliveryTracking | null = null;
  comment!: ReturnType<FormBuilder['control']>;
  confirming = false;
  error = '';
  loadError = '';
  liveConnected = false;
  lastEvent = '';
  private taskId = 0;
  private eventSource?: EventSource;

  constructor(private route: ActivatedRoute, private svc: ClientService, private fb: FormBuilder) {
    this.comment = this.fb.control('');
  }

  ngOnInit(): void {
    this.taskId = +this.route.snapshot.paramMap.get('id')!;
    this.refresh();
    this.eventSource = this.svc.openDeliveryStream(this.taskId, u => {
      this.liveConnected = true;
      this.lastEvent = u.message || u.status;
      if (this.d) {
        this.d = {
          ...this.d,
          currentStatus: u.status,
          clientConfirmed: u.clientConfirmed,
          hasProofOfDelivery: u.hasProofOfDelivery,
          latitude: u.latitude ?? this.d.latitude,
          longitude: u.longitude ?? this.d.longitude
        };
      } else {
        this.refresh();
      }
      if (u.status === 'COMPLETED' || u.clientConfirmed) this.refresh();
    });
    this.eventSource.onopen = () => this.liveConnected = true;
  }

  ngOnDestroy(): void { this.eventSource?.close(); }

  refresh(): void {
    this.svc.getDelivery(this.taskId).subscribe({
      next: r => this.d = r,
      error: () => this.loadError = 'Impossible de charger le suivi.'
    });
  }

  canConfirm(x: DeliveryTracking): boolean {
    return x.currentStatus === 'COMPLETED' && !x.clientConfirmed;
  }

  confirm(): void {
    this.confirming = true;
    const c = this.comment.value;
    this.svc.confirmDelivery(this.taskId, typeof c === 'string' ? c : undefined).subscribe({
      next: () => { this.confirming = false; this.refresh(); },
      error: e => { this.confirming = false; this.error = e?.error?.message || 'Erreur'; }
    });
  }
}
