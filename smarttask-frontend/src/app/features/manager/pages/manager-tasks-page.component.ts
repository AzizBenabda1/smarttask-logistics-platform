import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { TaskService } from '../../../core/services/task.service';
import { ManagerService } from '../../../core/services/manager.service';
import { AiService } from '../../../core/services/ai.service';
import { DriverRecommendationAI, DeliverySuccessPrediction, TaskAIAnalysis } from '../../../core/models/ai.models';
import { ToastService } from '../../../shared/services/toast.service';
import { Client, Driver, Priority, Task, TaskRequest, TaskStatus } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-tasks-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './manager-tasks-page.component.html'
})
export class ManagerTasksPageComponent implements OnInit {
  tasks: Task[] = [];
  clients: Client[] = [];
  drivers: Driver[] = [];
  statuses = Object.values(['PENDING', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'DELAYED'] as TaskStatus[]);
  priorities = Object.values(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as Priority[]);
  filterStatus: TaskStatus | '' = '';
  filterSearch = '';
  page = 0;
  totalPages = 0;
  totalElements = 0;
  showForm = false;
  editing: Task | null = null;
  form!: FormGroup;
  error = '';

  showAiModal = false;
  aiTask: Task | null = null;
  aiAnalysis: TaskAIAnalysis | null = null;
  aiDeliverySuccess: DeliverySuccessPrediction | null = null;
  aiDriverRec: DriverRecommendationAI | null = null;
  aiLoading = false;
  aiError = '';
  viewMode: 'cards' | 'table' = 'cards';

  constructor(
    private taskService: TaskService,
    private managerService: ManagerService,
    private aiService: AiService,
    private fb: FormBuilder,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.loadRefs();
    this.loadTasks();
  }

  initForm(task?: Task): void {
    const deadline = task?.deadline ? task.deadline.slice(0, 16) : '';
    this.form = this.fb.group({
      title: [task?.title || '', Validators.required],
      description: [task?.description || ''],
      clientId: [task?.clientId || null, Validators.required],
      driverId: [task?.driverId || null],
      deliveryAddress: [task?.deliveryAddress || '', Validators.required],
      zone: [task?.zone || ''],
      scheduledDate: [task?.scheduledDate || ''],
      scheduledTime: [task?.scheduledTime || ''],
      deadline: [deadline, Validators.required],
      priority: [task?.priority || 'MEDIUM', Validators.required],
      deliveryType: [task?.deliveryType || ''],
      weightQuantity: [task?.weightQuantity || ''],
      instructions: [task?.instructions || ''],
      estimatedMinutes: [task?.estimatedMinutes || null]
    });
  }

  loadRefs(): void {
    this.managerService.getClients().subscribe(c => this.clients = c);
    this.managerService.getDrivers().subscribe(d => this.drivers = d);
  }

  loadTasks(): void {
    this.taskService.getPage({
      status: this.filterStatus || undefined,
      search: this.filterSearch || undefined,
      page: this.page,
      size: 15
    }).subscribe(p => {
      this.tasks = p.content;
      this.totalPages = p.totalPages;
      this.totalElements = p.totalElements;
    });
  }

  prevPage(): void { if (this.page > 0) { this.page--; this.loadTasks(); } }
  nextPage(): void { if (this.page < this.totalPages - 1) { this.page++; this.loadTasks(); } }

  assignRecommended(task: Task): void {
    this.taskService.assignRecommended(task.id).subscribe({
      next: () => { this.toast.success(`Tache #${task.id} assignee (IA)`); this.loadTasks(); },
      error: e => this.toast.error(e.error?.message || 'Assignation IA impossible')
    });
  }

  openCreate(): void {
    this.editing = null;
    this.initForm();
    this.showForm = true;
  }

  openEdit(task: Task): void {
    this.editing = task;
    this.initForm(task);
    this.showForm = true;
  }

  closeForm(): void {
    this.showForm = false;
    this.error = '';
  }

  save(): void {
    if (this.form.invalid) return;
    const raw = this.form.value;
    const data: TaskRequest = {
      ...raw,
      deadline: raw.deadline.length === 16 ? raw.deadline + ':00' : raw.deadline
    };
    const obs = this.editing
      ? this.taskService.update(this.editing.id, data)
      : this.taskService.create(data);
    obs.subscribe({
      next: () => { this.closeForm(); this.loadTasks(); },
      error: (e) => this.error = e.error?.message || 'Erreur'
    });
  }

  deleteTask(task: Task): void {
    if (!confirm(`Supprimer "${task.title}" ?`)) return;
    this.taskService.delete(task.id).subscribe(() => this.loadTasks());
  }

  assign(task: Task, driverId: number): void {
    this.taskService.assignDriver(task.id, driverId).subscribe(() => this.loadTasks());
  }

  changeStatus(task: Task, status: TaskStatus): void {
    this.taskService.updateStatus(task.id, status).subscribe(() => this.loadTasks());
  }

  openAiModal(task: Task): void {
    this.aiTask = task;
    this.aiAnalysis = null;
    this.aiDeliverySuccess = null;
    this.aiDriverRec = null;
    this.aiError = '';
    this.showAiModal = true;
  }

  closeAiModal(): void {
    this.showAiModal = false;
    this.aiTask = null;
    this.aiAnalysis = null;
    this.aiDeliverySuccess = null;
    this.aiDriverRec = null;
    this.aiError = '';
  }

  analyzeWithAi(): void {
    if (!this.aiTask) return;
    this.aiLoading = true;
    this.aiError = '';
    this.aiService.analyzeTask(this.aiTask.id).subscribe({
      next: r => { this.aiAnalysis = r; this.aiLoading = false; },
      error: e => {
        this.aiLoading = false;
        this.aiError = e.error?.message || 'Service IA indisponible. Démarrez smarttask-ai sur le port 8000.';
      }
    });
  }

  analyzeDeliverySuccess(): void {
    if (!this.aiTask) return;
    this.aiLoading = true;
    this.aiError = '';
    this.aiService.predictDeliverySuccess(this.aiTask.id).subscribe({
      next: r => { this.aiDeliverySuccess = r; this.aiLoading = false; this.toast.info(`Reussite livraison : ${this.successPercent()}%`); },
      error: e => {
        this.aiLoading = false;
        this.aiError = e.error?.message || 'Prediction reussite livraison indisponible.';
      }
    });
  }

  successPercent(): number {
    return this.aiDeliverySuccess
      ? Math.round(this.aiDeliverySuccess.successProbability * 100) : 0;
  }

  findBestDriver(): void {
    if (!this.aiTask) return;
    this.aiLoading = true;
    this.aiError = '';
    this.aiService.recommendDriver(this.aiTask.id).subscribe({
      next: r => { this.aiDriverRec = r; this.aiLoading = false; },
      error: e => {
        this.aiLoading = false;
        this.aiError = e.error?.message || 'Impossible d\'obtenir une recommandation chauffeur.';
      }
    });
  }

  acceptAiDriver(): void {
    if (!this.aiTask || !this.aiDriverRec) return;
    this.taskService.assignDriver(this.aiTask.id, this.aiDriverRec.recommendedDriverId).subscribe({
      next: () => { this.closeAiModal(); this.loadTasks(); },
      error: e => this.aiError = e.error?.message || 'Erreur assignation'
    });
  }

  driverNameById(id: number): string {
    const d = this.drivers.find(x => x.id === id);
    return d ? `${d.firstName} ${d.lastName}` : `Chauffeur #${id}`;
  }

  delayPercent(): number {
    return this.aiAnalysis ? Math.round(this.aiAnalysis.delayProbability * 100) : 0;
  }
}
