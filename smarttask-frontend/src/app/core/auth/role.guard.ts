import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { Role } from '../models/auth.models';

export const roleGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const allowedRoles = route.data['roles'] as Role[];
  const user = auth.getCurrentUser();

  if (user && allowedRoles.includes(user.role)) {
    return true;
  }

  router.navigate(['/access-denied']);
  return false;
};
