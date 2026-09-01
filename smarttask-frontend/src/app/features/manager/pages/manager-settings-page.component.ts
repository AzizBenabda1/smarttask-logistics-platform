import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-manager-settings-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './manager-settings-page.component.html'
})
export class ManagerSettingsPageComponent {
  constructor(public auth: AuthService) {}
}
