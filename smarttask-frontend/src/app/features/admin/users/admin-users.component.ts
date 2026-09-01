import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../../../core/services/user.service';
import { Role, User, UserRequest } from '../../../core/models/auth.models';

@Component({
  selector: 'app-admin-users',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss']
})
export class AdminUsersComponent implements OnInit {
  users: User[] = [];
  roles = Object.values(Role);
  Role = Role;
  search = '';
  filterRole: Role | '' = '';
  showForm = false;
  editingUser: User | null = null;
  form!: FormGroup;
  error = '';

  constructor(private userService: UserService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.initForm();
    this.loadUsers();
  }

  initForm(user?: User): void {
    this.form = this.fb.group({
      firstName: [user?.firstName || '', Validators.required],
      lastName: [user?.lastName || '', Validators.required],
      email: [user?.email || '', [Validators.required, Validators.email]],
      password: ['', user ? [] : [Validators.required, Validators.minLength(8)]],
      phone: [user?.phone || ''],
      role: [user?.role || Role.CLIENT, Validators.required],
      active: [user?.active ?? true]
    });
  }

  loadUsers(): void {
    this.userService.getAll(this.search || undefined, this.filterRole || undefined).subscribe({
      next: (users) => this.users = users
    });
  }

  openCreate(): void {
    this.editingUser = null;
    this.initForm();
    this.showForm = true;
  }

  openEdit(user: User): void {
    this.editingUser = user;
    this.initForm(user);
    this.showForm = true;
  }

  closeForm(): void {
    this.showForm = false;
    this.editingUser = null;
    this.error = '';
  }

  save(): void {
    if (this.form.invalid) return;
    const data: UserRequest = { ...this.form.value };
    if (this.editingUser && !data.password) delete data.password;

    const obs = this.editingUser
      ? this.userService.update(this.editingUser.id, data)
      : this.userService.create(data as UserRequest);

    obs.subscribe({
      next: () => { this.closeForm(); this.loadUsers(); },
      error: (err) => this.error = err.error?.message || 'Erreur'
    });
  }

  deleteUser(user: User): void {
    if (!confirm(`Supprimer ${user.firstName} ${user.lastName} ?`)) return;
    this.userService.delete(user.id).subscribe(() => this.loadUsers());
  }

  toggleStatus(user: User): void {
    this.userService.updateStatus(user.id, !user.active).subscribe(() => this.loadUsers());
  }

  changeRole(user: User, role: Role): void {
    this.userService.updateRole(user.id, role).subscribe(() => this.loadUsers());
  }
}
