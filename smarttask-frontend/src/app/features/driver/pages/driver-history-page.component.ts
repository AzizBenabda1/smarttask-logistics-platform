import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DriverService } from '../../../core/services/driver.service';
import { Task } from '../../../core/models/role.models';

@Component({ standalone: true, imports: [CommonModule],
  template: `<div class="page"><h1>Historique</h1>
<div class="card table-wrap"><table><thead><tr><th>Date</th><th>Client</th><th>Adresse</th><th>Statut</th></tr></thead>
<tbody><tr *ngFor="let t of tasks"><td>{{ t.deliveredAt || t.deadline | date:'short' }}</td>
<td>{{ t.clientName }}</td><td>{{ t.deliveryAddress }}</td><td>{{ t.status }}</td></tr></tbody></table></div></div>` })
export class DriverHistoryPageComponent implements OnInit {
  tasks: Task[] = [];
  constructor(private svc: DriverService) {}
  ngOnInit(): void { this.svc.getHistory().subscribe(r => this.tasks = r); }
}
