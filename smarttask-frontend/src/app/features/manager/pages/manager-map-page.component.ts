import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TaskService } from '../../../core/services/task.service';
import { Task } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-map-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manager-map-page.component.html'
})
export class ManagerMapPageComponent implements OnInit, OnDestroy {
  tasks: Task[] = [];
  zones: { name: string; count: number }[] = [];
  gpsTasks: Task[] = [];
  private timer?: ReturnType<typeof setInterval>;

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.load();
    this.timer = setInterval(() => this.load(), 30000);
  }

  ngOnDestroy(): void {
    if (this.timer) clearInterval(this.timer);
  }

  load(): void {
    this.taskService.getAll().subscribe(tasks => {
      this.tasks = tasks.filter(t => t.status !== 'COMPLETED' && t.status !== 'CANCELLED');
      this.gpsTasks = this.tasks.filter(t => t.latitude != null && t.longitude != null);
      const map = new Map<string, number>();
      this.tasks.forEach(t => {
        const z = t.zone || 'Non défini';
        map.set(z, (map.get(z) || 0) + 1);
      });
      this.zones = Array.from(map.entries()).map(([name, count]) => ({ name, count }));
    });
  }

  gpsLeft(t: Task): number {
    const lng = Number(t.longitude);
    return Math.min(95, Math.max(5, ((lng + 180) / 360) * 100));
  }

  gpsTop(t: Task): number {
    const lat = Number(t.latitude);
    return Math.min(90, Math.max(10, ((90 - lat) / 180) * 100));
  }
}
