import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DriverService } from '../../../core/services/driver.service';
import { Task } from '../../../core/models/role.models';

@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Mes missions</h1>
      <p class="subtitle">{{ tasks.length }} mission(s) assignée(s)</p>
    </div>
  </div>

  <div class="card-grid">
    <div class="tile-card" *ngFor="let t of tasks">
      <div class="tile-header">
        <div>
          <h3 class="tile-title">Mission #{{ t.id }}</h3>
          <p class="tile-subtitle">{{ t.clientName }}</p>
        </div>
        <span class="badge" [ngClass]="t.priority">{{ t.priority }}</span>
      </div>
      <div class="tile-body">
        <div class="meta-item">
          <span class="meta-label">Adresse</span>
          <span class="meta-value">{{ t.deliveryAddress }}</span>
        </div>
        <div class="meta-item mt-1">
          <span class="meta-label">Statut</span>
          <span class="badge" [ngClass]="t.status">{{ t.status }}</span>
        </div>
      </div>
      <div class="tile-footer">
        <a [routerLink]="['/driver/tasks', t.id]" class="btn btn-primary">Voir le détail</a>
      </div>
    </div>
    <div class="empty-state" *ngIf="!tasks.length" style="grid-column:1/-1">
      <p class="empty-title">Aucune mission</p>
      <p>Vos missions apparaîtront ici une fois assignées.</p>
    </div>
  </div>
</div>`
})
export class DriverTasksPageComponent implements OnInit {
  tasks: Task[] = [];
  constructor(private svc: DriverService) {}
  ngOnInit(): void { this.svc.getTasks().subscribe(r => this.tasks = r); }
}
