import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AutomationService } from '../../../core/services/automation.service';
import { AutomationLog, AutomationStatus, ExpressChainResult } from '../../../core/models/automation.models';

@Component({
  selector: 'app-manager-automation-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manager-automation-page.component.html'
})
export class ManagerAutomationPageComponent implements OnInit {
  status: AutomationStatus | null = null;
  logs: AutomationLog[] = [];
  lastResult: ExpressChainResult | null = null;
  orderIdInput = '';
  loading = false;
  error = '';

  readonly chainSteps = [
    { n: 1, name: 'READ_ORDER', label: 'Lire la commande' },
    { n: 2, name: 'AUTO_VERIFY', label: 'Valider automatiquement' },
    { n: 3, name: 'CREATE_TASK', label: 'Créer la tâche' },
    { n: 4, name: 'AI_PRIORITIZE', label: 'Prioriser via IA' },
    { n: 5, name: 'AI_ASSIGN_DRIVER', label: 'Assigner chauffeur IA' },
    { n: 6, name: 'ESTIMATE_AND_NOTIFY', label: 'ETA + notifications' },
    { n: 7, name: 'LOG_COMPLETE', label: 'Journal final' }
  ];

  constructor(private automation: AutomationService) {}

  ngOnInit(): void {
    this.automation.status().subscribe(s => this.status = s);
    this.loadLogs();
  }

  loadLogs(): void {
    this.automation.logs().subscribe(l => this.logs = l);
  }

  runManual(): void {
    const id = +this.orderIdInput;
    if (!id) return;
    this.loading = true;
    this.error = '';
    this.automation.runExpress(id).subscribe({
      next: (r) => { this.lastResult = r; this.loading = false; this.loadLogs(); },
      error: (e) => { this.error = e.error?.message || 'Erreur'; this.loading = false; }
    });
  }
}
