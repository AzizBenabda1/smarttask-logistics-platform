import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-access-denied',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="page">
      <div class="card">
        <h1>403 — Accès refusé</h1>
        <p>Vous n'avez pas les permissions nécessaires pour accéder à cette page.</p>
        <a routerLink="/login" class="btn btn-primary">Retour à la connexion</a>
      </div>
    </div>
  `,
  styles: [`
    .page { min-height: 80vh; display: flex; align-items: center; justify-content: center; }
    .card { text-align: center; padding: 3rem; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    h1 { color: #dc2626; margin-bottom: 1rem; }
    p { color: #64748b; margin-bottom: 2rem; }
  `]
})
export class AccessDeniedComponent {}
