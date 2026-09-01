import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { ChatWidgetComponent } from '../../shared/components/chat-widget/chat-widget.component';

@Component({
  selector: 'app-driver-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, ChatWidgetComponent],
  template: `
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><span class="logo">SL</span><div><strong>SmartLogix</strong><small>Espace Chauffeur</small></div></div>
    <nav>
      <a *ngFor="let i of nav" [routerLink]="i.path" routerLinkActive="active">
        <span class="icon">{{ i.abbr }}</span>{{ i.label }}
      </a>
    </nav>
    <div class="footer" *ngIf="auth.getCurrentUser() as u">
      <div class="user">{{ u.firstName }} {{ u.lastName }}</div>
      <button class="btn btn-outline btn-sm" (click)="auth.logout()">Déconnexion</button>
    </div>
  </aside>
  <div class="content"><router-outlet></router-outlet></div>
  <app-chat-widget></app-chat-widget>
</div>`
})
export class DriverLayoutComponent {
  nav = [
    { path: 'dashboard', label: 'Dashboard', abbr: 'DB' },
    { path: 'tasks', label: 'Mes missions', abbr: 'MS' },
    { path: 'route', label: 'Mon itinéraire', abbr: 'IT' },
    { path: 'incidents', label: 'Signaler problème', abbr: 'SG' },
    { path: 'history', label: 'Historique', abbr: 'HS' },
    { path: 'performance', label: 'Performance', abbr: 'PF' },
    { path: 'settings', label: 'Profil', abbr: 'PR' }
  ];
  constructor(public auth: AuthService) {}
}
