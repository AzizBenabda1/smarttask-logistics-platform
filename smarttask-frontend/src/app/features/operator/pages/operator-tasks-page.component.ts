import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OperatorService } from '../../../core/services/operator.service';
import { Task } from '../../../core/models/role.models';

@Component({
  standalone: true, imports: [CommonModule],
  template: `
<div class="page"><h1>Tâches opérationnelles</h1>
<div class="card table-wrap"><table>
<thead><tr><th>Tâche</th><th>Client</th><th>Chauffeur</th><th>Statut</th><th>Deadline</th></tr></thead>
<tbody><tr *ngFor="let t of tasks">
  <td>{{ t.title }}</td><td>{{ t.clientName }}</td><td>{{ t.driverName || '—' }}</td>
  <td><span class="badge" [ngClass]="t.status">{{ t.status }}</span></td><td>{{ t.deadline | date:'short' }}</td>
</tr></tbody></table></div></div>`
})
export class OperatorTasksPageComponent implements OnInit {
  tasks: Task[] = [];
  constructor(private svc: OperatorService) {}
  ngOnInit(): void { this.svc.getTasks().subscribe(r => this.tasks = r); }
}
