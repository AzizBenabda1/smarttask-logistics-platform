import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DriverService } from '../../../core/services/driver.service';
import { DriverPerformance } from '../../../core/models/role.models';

@Component({ standalone: true, imports: [CommonModule],
  template: `<div class="page"><h1>Ma performance</h1>
<ng-container *ngIf="p as x"><div class="kpi-grid">
<div class="kpi"><div class="label">Livraisons</div><div class="value">{{ x.totalDeliveries }}</div></div>
<div class="kpi ok"><div class="label">À l'heure</div><div class="value">{{ x.onTimeDeliveries }}</div></div>
<div class="kpi warn"><div class="label">Retards</div><div class="value">{{ x.delayedDeliveries }}</div></div>
<div class="kpi"><div class="label">Taux réussite</div><div class="value">{{ x.successRate | number:'1.0-0' }}%</div></div>
<div class="kpi"><div class="label">Durée moy.</div><div class="value">{{ x.averageMinutes | number:'1.0-0' }} min</div></div>
</div></ng-container></div>` })
export class DriverPerformancePageComponent implements OnInit {
  p: DriverPerformance | null = null;
  constructor(private svc: DriverService) {}
  ngOnInit(): void { this.svc.getPerformance().subscribe(r => this.p = r); }
}
