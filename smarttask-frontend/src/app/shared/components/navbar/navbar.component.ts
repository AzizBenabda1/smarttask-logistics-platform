import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { Role } from '../../../core/models/auth.models';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  Role = Role;

  constructor(public auth: AuthService, private router: Router) {}

  logout(): void {
    this.auth.logout();
  }

  dashboardLink(): string {
    const user = this.auth.getCurrentUser();
    return user ? this.auth.getDashboardRoute(user.role) : '/login';
  }
}
