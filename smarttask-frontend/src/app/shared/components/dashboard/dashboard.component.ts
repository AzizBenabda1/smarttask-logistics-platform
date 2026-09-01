import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page">
      <div class="card">
        <h1>{{ title }}</h1>
        <p class="welcome">Bienvenue, {{ auth.getCurrentUser()?.firstName }} {{ auth.getCurrentUser()?.lastName }}</p>
        <p class="role">Rôle : <strong>{{ auth.getCurrentUser()?.role }}</strong></p>
        <p class="desc">{{ description }}</p>
      </div>
    </div>
  `,
  styles: [`
    .page { padding: 2rem; }
    .card {
      background: #fff;
      border-radius: 12px;
      padding: 2rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      max-width: 600px;
    }
    h1 { margin: 0 0 1rem; color: #1e293b; }
    .welcome { font-size: 1.1rem; color: #334155; }
    .role { color: #64748b; }
    .desc { margin-top: 1.5rem; color: #475569; }
  `]
})
export class DashboardComponent {
  @Input() title = 'Dashboard';
  @Input() description = '';

  constructor(public auth: AuthService) {}
}
