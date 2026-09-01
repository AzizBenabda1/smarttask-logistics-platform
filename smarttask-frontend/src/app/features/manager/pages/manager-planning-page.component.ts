import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TaskService } from '../../../core/services/task.service';
import { Task } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-planning-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manager-planning-page.component.html'
})
export class ManagerPlanningPageComponent implements OnInit {
  tasks: Task[] = [];
  selectedDate = new Date().toISOString().slice(0, 10);

  constructor(private taskService: TaskService) {}

  ngOnInit(): void { this.load(); }

  load(): void {
    this.taskService.getAll({ date: this.selectedDate }).subscribe(t => this.tasks = t);
  }
}
