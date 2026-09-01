import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({ standalone: true, imports: [CommonModule, RouterLink],
  template: `<div class="page"><h1>Profil</h1><div class="card" *ngIf="auth.getCurrentUser() as u">
  <p>{{ u.firstName }} {{ u.lastName }}</p><a routerLink="/profile" class="btn btn-primary btn-sm">Modifier</a></div></div>` })
export class DriverSettingsPageComponent { constructor(public auth: AuthService) {} }
