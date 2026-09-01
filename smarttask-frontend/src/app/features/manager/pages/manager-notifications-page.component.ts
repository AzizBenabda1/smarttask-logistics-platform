import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagerService } from '../../../core/services/manager.service';
import { NotificationItem } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-notifications-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manager-notifications-page.component.html'
})
export class ManagerNotificationsPageComponent implements OnInit {
  notifications: NotificationItem[] = [];

  constructor(private managerService: ManagerService) {}

  ngOnInit(): void { this.load(); }

  load(): void {
    this.managerService.getNotifications().subscribe(n => this.notifications = n);
  }

  markRead(n: NotificationItem): void {
    if (n.read) return;
    this.managerService.markNotificationRead(n.id).subscribe(() => {
      n.read = true;
    });
  }
}
