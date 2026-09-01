import { Component } from '@angular/core';
import { DashboardComponent } from '../../shared/components/dashboard/dashboard.component';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [DashboardComponent],
  template: `<app-dashboard title="Administration" description="Gérez les utilisateurs, les rôles et la configuration de SmartTask."></app-dashboard>`
})
export class AdminDashboardComponent {}

@Component({
  selector: 'app-manager-dashboard',
  standalone: true,
  imports: [DashboardComponent],
  template: `<app-dashboard title="Espace Manager" description="Supervisez les opérations et les équipes."></app-dashboard>`
})
export class ManagerDashboardComponent {}

@Component({
  selector: 'app-operator-dashboard',
  standalone: true,
  imports: [DashboardComponent],
  template: `<app-dashboard title="Espace Opérateur" description="Gérez les tâches opérationnelles du jour."></app-dashboard>`
})
export class OperatorDashboardComponent {}

@Component({
  selector: 'app-driver-dashboard',
  standalone: true,
  imports: [DashboardComponent],
  template: `<app-dashboard title="Espace Chauffeur" description="Consultez vos missions et itinéraires."></app-dashboard>`
})
export class DriverDashboardComponent {}

@Component({
  selector: 'app-client-dashboard',
  standalone: true,
  imports: [DashboardComponent],
  template: `<app-dashboard title="Espace Client" description="Suivez vos demandes et services."></app-dashboard>`
})
export class ClientDashboardComponent {}
