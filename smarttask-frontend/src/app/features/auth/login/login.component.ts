import { Component, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  encapsulation: ViewEncapsulation.None,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  form: FormGroup;
  error = '';
  loading = false;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    if (this.auth.isAuthenticated()) {
      const user = this.auth.getCurrentUser();
      if (user) this.router.navigate([this.auth.getDashboardRoute(user.role)]);
    }
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';
    this.auth.login(this.form.value).subscribe({
      next: (res) => this.router.navigate([this.auth.getDashboardRoute(res.user.role)]),
      error: (err) => {
        if (err.status === 0) {
          this.error = 'Impossible de contacter le backend. Vérifiez qu\'il est démarré sur le port 9090.';
        } else {
          this.error = err.error?.message || 'Identifiants invalides';
        }
        this.loading = false;
      },
      complete: () => this.loading = false
    });
  }
}
