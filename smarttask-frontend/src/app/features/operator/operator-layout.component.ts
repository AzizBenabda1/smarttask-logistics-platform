import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { ChatWidgetComponent } from '../../shared/components/chat-widget/chat-widget.component';

@Component({
  selector: 'app-operator-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, ChatWidgetComponent],
  template: `
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><span class="logo">SL</span><div><strong>SmartLogix</strong><small>Espace Opérateur</small></div></div>
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
export class OperatorLayoutComponent {
  nav = [
    { path: 'dashboard', label: 'Dashboard', abbr: 'DB' },
    { path: 'orders', label: 'Commandes', abbr: 'CM' },
    { path: 'orders/create', label: 'Nouvelle commande', abbr: 'NC' },
    { path: 'orders/pending', label: 'Vérification', abbr: 'VR' },
    { path: 'tasks', label: 'Tâches', abbr: 'TK' },
    { path: 'tasks/tracking', label: 'Suivi livraisons', abbr: 'SL' },
    { path: 'incidents', label: 'Incidents', abbr: 'IN' },
    { path: 'settings', label: 'Paramètres', abbr: 'PR' }
  ];
  constructor(public auth: AuthService) {}
}
