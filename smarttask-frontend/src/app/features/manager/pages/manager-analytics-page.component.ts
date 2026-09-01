import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagerService } from '../../../core/services/manager.service';
import { Analytics, ChartPoint } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-analytics-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manager-analytics-page.component.html'
})
export class ManagerAnalyticsPageComponent implements OnInit {
  data: Analytics | null = null;

  constructor(private managerService: ManagerService) {}

  ngOnInit(): void {
    this.managerService.getAnalytics().subscribe(d => this.data = d);
  }

  exportCsv(): void {
    this.managerService.exportAnalytics().subscribe(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'smarttask-analytics.csv';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  barWidth(point: ChartPoint, points: ChartPoint[]): number {
    const max = Math.max(...points.map(p => p.value), 1);
    return (point.value / max) * 100;
  }
}
