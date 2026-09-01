import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagerService } from '../../../core/services/manager.service';
import { TaskService } from '../../../core/services/task.service';
import { AiService } from '../../../core/services/ai.service';
import { AIModelStatus } from '../../../core/models/ai.models';
import { AIRecommendation } from '../../../core/models/manager.models';
import { AlertBannerComponent } from '../../../shared/components/alert-banner/alert-banner.component';
import { ViewToggleComponent, ViewMode } from '../../../shared/components/view-toggle/view-toggle.component';
import { ToastService } from '../../../shared/services/toast.service';

@Component({
  selector: 'app-manager-ai-page',
  standalone: true,
  imports: [CommonModule, AlertBannerComponent, ViewToggleComponent],
  templateUrl: './manager-ai-page.component.html'
})
export class ManagerAiPageComponent implements OnInit {
  recommendations: AIRecommendation[] = [];
  modelStatus: AIModelStatus | null = null;
  loading = true;
  message = '';
  aiError = '';
  viewMode: ViewMode = 'cards';

  constructor(
    private managerService: ManagerService,
    private taskService: TaskService,
    private aiService: AiService,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.loadRecommendations();
    this.aiService.modelStatus().subscribe({
      next: s => this.modelStatus = s,
      error: () => this.aiError = 'Microservice Python non disponible (port 8000)'
    });
  }

  loadRecommendations(): void {
    this.loading = true;
    this.managerService.getAiRecommendations().subscribe({
      next: r => { this.recommendations = r; this.loading = false; },
      error: () => this.loading = false
    });
  }

  refresh(taskId: number): void {
    this.aiService.recommendDriver(taskId).subscribe({
      next: ai => {
        const idx = this.recommendations.findIndex(x => x.taskId === taskId);
        const mapped: AIRecommendation = {
          taskId: ai.taskId,
          recommendedDriverId: ai.recommendedDriverId,
          recommendedDriverName: 'Chauffeur #' + ai.recommendedDriverId,
          scorePercent: ai.score,
          reasons: ai.reasons,
          ruleBased: false,
          disclaimer: 'SmartTask AI microservice'
        };
        if (idx >= 0) this.recommendations[idx] = mapped;
        this.toast.success(`Recommandation ML recalculee — tache #${taskId}`);
      },
      error: () => this.managerService.recommendDriver(taskId).subscribe(r => {
        const idx = this.recommendations.findIndex(x => x.taskId === taskId);
        if (idx >= 0) this.recommendations[idx] = r;
      })
    });
  }

  assign(r: AIRecommendation): void {
    this.taskService.assignRecommended(r.taskId).subscribe({
      next: () => {
        this.toast.success(`Tache #${r.taskId} assignee`);
        this.recommendations = this.recommendations.filter(x => x.taskId !== r.taskId);
      },
      error: e => this.toast.error(e.error?.message || 'Erreur assignation')
    });
  }

  assignDirect(r: AIRecommendation): void {
    this.taskService.assignDriver(r.taskId, r.recommendedDriverId).subscribe({
      next: () => {
        this.toast.success(`Tache #${r.taskId} assignee a ${r.recommendedDriverName}`);
        this.recommendations = this.recommendations.filter(x => x.taskId !== r.taskId);
      },
      error: e => this.toast.error(e.error?.message || 'Erreur assignation')
    });
  }
}
