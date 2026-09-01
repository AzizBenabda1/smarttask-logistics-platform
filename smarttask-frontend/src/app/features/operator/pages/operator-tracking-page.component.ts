import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OperatorService } from '../../../core/services/operator.service';
import { Task } from '../../../core/models/role.models';

@Component({ standalone: true, imports: [CommonModule],
  template: `<div class="page"><h1>Suivi livraisons</h1>
<div class="card table-wrap"><table><thead><tr><th>Tâche</th><th>Client</th><th>Chauffeur</th><th>Statut</th><th>Retard</th></tr></thead>
<tbody><tr *ngFor="let t of tasks"><td>{{ t.title }}</td><td>{{ t.clientName }}</td><td>{{ t.driverName||'—' }}</td>
<td><span class="badge" [ngClass]="t.status">{{ t.status }}</span></td><td>{{ t.delayed ? 'OUI' : 'NON' }}</td></tr></tbody></table></div></div>` })
export class OperatorTrackingPageComponent implements OnInit {
  tasks: Task[] = [];
  constructor(private svc: OperatorService) {}
  ngOnInit(): void { this.svc.getTasks().subscribe(r => this.tasks = r); }
}
