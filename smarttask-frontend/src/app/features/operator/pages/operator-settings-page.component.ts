import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({ standalone: true, imports: [CommonModule, RouterLink],
  template: `<div class="page"><h1>Paramètres</h1><div class="card" *ngIf="auth.getCurrentUser() as u">
  <p>{{ u.firstName }} {{ u.lastName }} — {{ u.email }}</p>
  <a routerLink="/profile" class="btn btn-primary btn-sm">Modifier le profil</a></div></div>` })
export class OperatorSettingsPageComponent { constructor(public auth: AuthService) {} }
