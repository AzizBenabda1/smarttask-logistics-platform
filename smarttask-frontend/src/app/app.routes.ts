import { Routes } from '@angular/router';
import { authGuard } from './core/auth/auth.guard';
import { roleGuard } from './core/auth/role.guard';
import { Role } from './core/models/auth.models';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent) },
  { path: 'access-denied', loadComponent: () => import('./features/access-denied/access-denied.component').then(m => m.AccessDeniedComponent) },

  {
    path: 'admin/dashboard',
    canActivate: [authGuard, roleGuard],
    data: { roles: [Role.ADMIN] },
    loadComponent: () => import('./features/dashboards/role-dashboards.component').then(m => m.AdminDashboardComponent)
  },
  {
    path: 'admin/users',
    canActivate: [authGuard, roleGuard],
    data: { roles: [Role.ADMIN] },
    loadComponent: () => import('./features/admin/users/admin-users.component').then(m => m.AdminUsersComponent)
  },
  {
    path: 'manager',
    canActivate: [authGuard, roleGuard],
    data: { roles: [Role.MANAGER] },
    loadComponent: () => import('./features/manager/manager-layout.component').then(m => m.ManagerLayoutComponent),
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', loadComponent: () => import('./features/manager/pages/manager-dashboard-page.component').then(m => m.ManagerDashboardPageComponent) },
      { path: 'tasks', loadComponent: () => import('./features/manager/pages/manager-tasks-page.component').then(m => m.ManagerTasksPageComponent) },
      { path: 'planning', loadComponent: () => import('./features/manager/pages/manager-planning-page.component').then(m => m.ManagerPlanningPageComponent) },
      { path: 'map', loadComponent: () => import('./features/manager/pages/manager-map-page.component').then(m => m.ManagerMapPageComponent) },
      { path: 'drivers', loadComponent: () => import('./features/manager/pages/manager-drivers-page.component').then(m => m.ManagerDriversPageComponent) },
      { path: 'delays', loadComponent: () => import('./features/manager/pages/manager-delays-page.component').then(m => m.ManagerDelaysPageComponent) },
      { path: 'incidents', loadComponent: () => import('./features/manager/pages/manager-incidents-page.component').then(m => m.ManagerIncidentsPageComponent) },
      { path: 'notifications', loadComponent: () => import('./features/manager/pages/manager-notifications-page.component').then(m => m.ManagerNotificationsPageComponent) },
      { path: 'analytics', loadComponent: () => import('./features/manager/pages/manager-analytics-page.component').then(m => m.ManagerAnalyticsPageComponent) },
      { path: 'ai', loadComponent: () => import('./features/manager/pages/manager-ai-page.component').then(m => m.ManagerAiPageComponent) },
      { path: 'automation', loadComponent: () => import('./features/manager/pages/manager-automation-page.component').then(m => m.ManagerAutomationPageComponent) },
      { path: 'settings', loadComponent: () => import('./features/manager/pages/manager-settings-page.component').then(m => m.ManagerSettingsPageComponent) }
    ]
  },
  {
    path: 'operator',
    canActivate: [authGuard, roleGuard],
    data: { roles: [Role.OPERATOR] },
    loadComponent: () => import('./features/operator/operator-layout.component').then(m => m.OperatorLayoutComponent),
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', loadComponent: () => import('./features/operator/pages/operator-dashboard-page.component').then(m => m.OperatorDashboardPageComponent) },
      { path: 'orders', loadComponent: () => import('./features/operator/pages/operator-orders-page.component').then(m => m.OperatorOrdersPageComponent) },
      { path: 'orders/pending', loadComponent: () => import('./features/operator/pages/operator-pending-page.component').then(m => m.OperatorPendingPageComponent) },
      { path: 'tasks', loadComponent: () => import('./features/operator/pages/operator-tasks-page.component').then(m => m.OperatorTasksPageComponent) },
      { path: 'tasks/tracking', loadComponent: () => import('./features/operator/pages/operator-tracking-page.component').then(m => m.OperatorTrackingPageComponent) },
      { path: 'incidents', loadComponent: () => import('./features/operator/pages/operator-incidents-page.component').then(m => m.OperatorIncidentsPageComponent) },
      { path: 'settings', loadComponent: () => import('./features/operator/pages/operator-settings-page.component').then(m => m.OperatorSettingsPageComponent) }
    ]
  },
  {
    path: 'driver',
    canActivate: [authGuard, roleGuard],
    data: { roles: [Role.DRIVER] },
    loadComponent: () => import('./features/driver/driver-layout.component').then(m => m.DriverLayoutComponent),
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', loadComponent: () => import('./features/driver/pages/driver-dashboard-page.component').then(m => m.DriverDashboardPageComponent) },
      { path: 'tasks', loadComponent: () => import('./features/driver/pages/driver-tasks-page.component').then(m => m.DriverTasksPageComponent) },
      { path: 'tasks/:id', loadComponent: () => import('./features/driver/pages/driver-task-detail-page.component').then(m => m.DriverTaskDetailPageComponent) },
      { path: 'route', loadComponent: () => import('./features/driver/pages/driver-route-page.component').then(m => m.DriverRoutePageComponent) },
      { path: 'incidents', loadComponent: () => import('./features/driver/pages/driver-incidents-page.component').then(m => m.DriverIncidentsPageComponent) },
      { path: 'history', loadComponent: () => import('./features/driver/pages/driver-history-page.component').then(m => m.DriverHistoryPageComponent) },
      { path: 'performance', loadComponent: () => import('./features/driver/pages/driver-performance-page.component').then(m => m.DriverPerformancePageComponent) },
      { path: 'settings', loadComponent: () => import('./features/driver/pages/driver-settings-page.component').then(m => m.DriverSettingsPageComponent) }
    ]
  },
  {
    path: 'client',
    canActivate: [authGuard, roleGuard],
    data: { roles: [Role.CLIENT] },
    loadComponent: () => import('./features/client/client-layout.component').then(m => m.ClientLayoutComponent),
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', loadComponent: () => import('./features/client/pages/client-dashboard-page.component').then(m => m.ClientDashboardPageComponent) },
      { path: 'orders', loadComponent: () => import('./features/client/pages/client-orders-page.component').then(m => m.ClientOrdersPageComponent) },
      { path: 'orders/create', loadComponent: () => import('./features/client/pages/client-order-create-page.component').then(m => m.ClientOrderCreatePageComponent) },
      { path: 'orders/:id', loadComponent: () => import('./features/client/pages/client-order-detail-page.component').then(m => m.ClientOrderDetailPageComponent) },
      { path: 'delivery/:id', loadComponent: () => import('./features/client/pages/client-delivery-page.component').then(m => m.ClientDeliveryPageComponent) },
      { path: 'notifications', loadComponent: () => import('./features/client/pages/client-notifications-page.component').then(m => m.ClientNotificationsPageComponent) },
      { path: 'reviews', loadComponent: () => import('./features/client/pages/client-reviews-page.component').then(m => m.ClientReviewsPageComponent) },
      { path: 'incidents', loadComponent: () => import('./features/client/pages/client-incidents-page.component').then(m => m.ClientIncidentsPageComponent) },
      { path: 'settings', loadComponent: () => import('./features/client/pages/client-settings-page.component').then(m => m.ClientSettingsPageComponent) }
    ]
  },
  {
    path: 'profile',
    canActivate: [authGuard],
    loadComponent: () => import('./features/profile/profile.component').then(m => m.ProfileComponent)
  },
  { path: '**', redirectTo: 'login' }
];
