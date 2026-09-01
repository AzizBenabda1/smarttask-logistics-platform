import { Component } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { ToastContainerComponent } from './shared/components/toast-container/toast-container.component';
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, ToastContainerComponent, CommonModule],
  template: `
    <app-toast-container></app-toast-container>
    <app-navbar *ngIf="showNavbar"></app-navbar>
    <main [class.full]="!showNavbar">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [`
    main { min-height: calc(100vh - 56px); background: var(--st-bg, #f4f6f9); }
    main.full { min-height: 100vh; }
  `]
})
export class AppComponent {
  showNavbar = true;

  constructor(private router: Router) {
    this.router.events.pipe(filter(e => e instanceof NavigationEnd)).subscribe(() => {
      this.showNavbar = !['/manager', '/operator', '/driver', '/client'].some(p => this.router.url.startsWith(p));
    });
  }
}
