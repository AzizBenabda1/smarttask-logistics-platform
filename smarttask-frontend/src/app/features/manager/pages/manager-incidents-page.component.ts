import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ManagerService } from '../../../core/services/manager.service';
import { IncidentItem, IncidentStatus } from '../../../core/models/manager.models';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manager-incidents-page.component.html'
})
export class ManagerIncidentsPageComponent implements OnInit {
  incidents: IncidentItem[] = [];
  filterStatus: IncidentStatus | '' = '';
  page = 0;
  totalPages = 0;
  loading = true;
  statuses: IncidentStatus[] = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'];

  constructor(private managerService: ManagerService) {}

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    this.managerService.getIncidents(this.filterStatus || undefined, this.page).subscribe({
      next: r => {
        this.incidents = r.content;
        this.totalPages = r.totalPages;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  resolve(incident: IncidentItem, status: IncidentStatus): void {
    this.managerService.updateIncident(incident.id, status).subscribe(() => this.load());
  }

  prev(): void { if (this.page > 0) { this.page--; this.load(); } }
  next(): void { if (this.page < this.totalPages - 1) { this.page++; this.load(); } }
}
