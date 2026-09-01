import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { DriverService } from '../../../core/services/driver.service';
import { Task } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule],
  template: `
<div class="page"><h1>Mission #{{ task?.id }}</h1>
<div class="card" *ngIf="task as t">
  <p><strong>Client:</strong> {{ t.clientName }} — {{ t.clientPhone }}</p>
  <p><strong>Adresse:</strong> {{ t.deliveryAddress }}</p>
  <p><strong>Produits:</strong> {{ t.products || t.description }}</p>
  <p><strong>Statut:</strong> <span class="badge" [ngClass]="t.status">{{ t.status }}</span></p>
  <div style="display:flex;gap:.5rem;margin-top:1rem;flex-wrap:wrap">
    <button class="btn btn-primary btn-sm" *ngIf="t.status==='ASSIGNED'" (click)="act('accept')">Accepter</button>
    <button class="btn btn-primary btn-sm" *ngIf="t.status==='ACCEPTED'" (click)="act('start')">Commencer</button>
    <button class="btn btn-primary btn-sm" *ngIf="t.status==='IN_PROGRESS'" (click)="act('delivery')">En livraison</button>
    <button class="btn btn-primary btn-sm" *ngIf="t.status==='IN_DELIVERY'" (click)="act('complete')">Livrée</button>
    <button class="btn btn-primary btn-sm" *ngIf="isActive(t)" (click)="shareLocation()">GPS manuel</button>
    <button class="btn btn-primary btn-sm" *ngIf="isActive(t)" (click)="toggleAutoGps()">
      {{ autoGps ? 'Arrêter GPS auto' : 'GPS auto (30s)' }}
    </button>
    <label class="btn-sm" *ngIf="isActive(t)" style="cursor:pointer">
      📷 Preuve photo <input type="file" accept="image/*" hidden (change)="onPhoto($event)" />
    </label>
    <a *ngIf="t.deliveryAddress" [href]="mapsUrl(t.deliveryAddress)" target="_blank" class="btn-sm">Maps</a>
  </div>
  <p *ngIf="msg" style="color:#16a34a;margin-top:.5rem">{{ msg }}</p>
</div></div>`
})
export class DriverTaskDetailPageComponent implements OnInit, OnDestroy {
  task: Task | null = null;
  msg = '';
  autoGps = false;
  private id = 0;
  private gpsTimer?: ReturnType<typeof setInterval>;

  constructor(private route: ActivatedRoute, private svc: DriverService) {}

  ngOnInit(): void {
    this.id = +this.route.snapshot.paramMap.get('id')!;
    this.reload();
  }

  ngOnDestroy(): void { this.stopAutoGps(); }

  reload(): void { this.svc.getTask(this.id).subscribe(t => this.task = t); }

  isActive(t: Task): boolean {
    return t.status === 'IN_DELIVERY' || t.status === 'IN_PROGRESS' || t.status === 'ACCEPTED';
  }

  act(action: string): void {
    const m: Record<string, () => void> = {
      accept: () => this.svc.accept(this.id).subscribe(t => { this.task = t; }),
      start: () => this.svc.start(this.id).subscribe(t => { this.task = t; }),
      delivery: () => this.svc.inDelivery(this.id).subscribe(t => { this.task = t; this.toggleAutoGps(true); }),
      complete: () => this.svc.complete(this.id).subscribe(t => { this.task = t; this.stopAutoGps(); })
    };
    m[action]?.();
  }

  mapsUrl(addr: string): string {
    return 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(addr);
  }

  shareLocation(): void {
    if (!navigator.geolocation) { this.msg = 'GPS non disponible'; return; }
    navigator.geolocation.getCurrentPosition(pos => {
      this.svc.updateLocation(this.id, pos.coords.latitude, pos.coords.longitude).subscribe({
        next: () => this.msg = 'Position envoyée',
        error: () => this.msg = 'Erreur GPS'
      });
    }, () => this.msg = 'Autorisez la géolocalisation');
  }

  toggleAutoGps(forceOn = false): void {
    if (forceOn) { this.autoGps = true; }
    else { this.autoGps = !this.autoGps; }
    if (this.autoGps) {
      this.shareLocation();
      this.gpsTimer = setInterval(() => this.shareLocation(), 30000);
      this.msg = 'GPS automatique activé';
    } else {
      this.stopAutoGps();
    }
  }

  stopAutoGps(): void {
    this.autoGps = false;
    if (this.gpsTimer) clearInterval(this.gpsTimer);
  }

  onPhoto(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = (reader.result as string).split(',')[1] || '';
      this.svc.uploadProof(this.id, base64).subscribe({
        next: () => this.msg = 'Photo de preuve envoyée',
        error: () => this.msg = 'Erreur envoi photo'
      });
    };
    reader.readAsDataURL(file);
  }
}
