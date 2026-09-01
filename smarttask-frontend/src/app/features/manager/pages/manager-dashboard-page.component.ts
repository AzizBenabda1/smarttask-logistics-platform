import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagerService } from '../../../core/services/manager.service';
import { ChartPoint, ManagerDashboard } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-dashboard-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manager-dashboard-page.component.html'
})
export class ManagerDashboardPageComponent implements OnInit {
  data: ManagerDashboard | null = null;
  loading = true;

  constructor(private managerService: ManagerService) {}

  ngOnInit(): void {
    this.managerService.getDashboard().subscribe({
      next: (d) => { this.data = d; this.loading = false; },
      error: () => this.loading = false
    });
  }

  barWidth(point: ChartPoint, points: ChartPoint[]): number {
    const max = Math.max(...points.map(p => p.value), 1);
    return (point.value / max) * 100;
  }
}
