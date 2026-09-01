import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../../core/services/user.service';
import { AuthService } from '../../core/auth/auth.service';
import { User } from '../../core/models/auth.models';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User | null = null;
  profileForm!: FormGroup;
  passwordForm!: FormGroup;
  message = '';
  error = '';

  constructor(
    private userService: UserService,
    public auth: AuthService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.profileForm = this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      phone: ['']
    });
    this.passwordForm = this.fb.group({
      currentPassword: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    });
    this.loadProfile();
  }

  loadProfile(): void {
    this.userService.getProfile().subscribe({
      next: (user) => {
        this.user = user;
        this.profileForm.patchValue({
          firstName: user.firstName,
          lastName: user.lastName,
          phone: user.phone || ''
        });
      }
    });
  }

  saveProfile(): void {
    if (this.profileForm.invalid) return;
    this.userService.updateProfile(this.profileForm.value).subscribe({
      next: (user) => {
        this.user = user;
        this.message = 'Profil mis à jour';
        this.auth.refreshCurrentUser().subscribe();
      },
      error: (err) => this.error = err.error?.message || 'Erreur'
    });
  }

  changePassword(): void {
    if (this.passwordForm.invalid) return;
    const val = this.passwordForm.value;
    if (val.newPassword !== val.confirmPassword) {
      this.error = 'Les mots de passe ne correspondent pas';
      return;
    }
    this.userService.changePassword(val).subscribe({
      next: () => {
        this.message = 'Mot de passe modifié';
        this.passwordForm.reset();
      },
      error: (err) => this.error = err.error?.message || 'Erreur'
    });
  }
}
