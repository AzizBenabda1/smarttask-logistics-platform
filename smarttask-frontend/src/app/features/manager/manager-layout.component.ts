import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { ChatWidgetComponent } from '../../shared/components/chat-widget/chat-widget.component';

interface NavItem {
  path: string;
  label: string;
  abbr: string;
}

@Component({
  selector: 'app-manager-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, ChatWidgetComponent],
  templateUrl: './manager-layout.component.html',
  styleUrls: ['./manager-layout.component.scss']
})
export class ManagerLayoutComponent {
  nav: NavItem[] = [
    { path: 'dashboard', label: 'Tableau de bord', abbr: 'TB' },
    { path: 'tasks', label: 'Tâches', abbr: 'TK' },
    { path: 'planning', label: 'Planning', abbr: 'PL' },
    { path: 'map', label: 'Carte', abbr: 'MP' },
    { path: 'drivers', label: 'Chauffeurs', abbr: 'CH' },
    { path: 'delays', label: 'Retards', abbr: 'RT' },
    { path: 'incidents', label: 'Incidents', abbr: 'IN' },
    { path: 'notifications', label: 'Notifications', abbr: 'NT' },
    { path: 'analytics', label: 'Analytique', abbr: 'AN' },
    { path: 'ai', label: 'SmartLogix AI', abbr: 'AI' },
    { path: 'automation', label: 'IA Automation', abbr: 'AU' },
    { path: 'settings', label: 'Paramètres', abbr: 'PR' }
  ];

  constructor(public auth: AuthService) {}

  logout(): void {
    this.auth.logout();
  }
}
