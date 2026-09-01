import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClientService } from '../../../core/services/client.service';
import { NotificationItem } from '../../../core/models/role.models';

@Component({ standalone: true, imports: [CommonModule],
  template: `<div class="page"><h1>Notifications</h1>
<div class="card"><div class="alert-item" *ngFor="let n of items" [class.unread]="!n.read">
<strong>{{ n.title }}</strong><div class="msg">{{ n.message }}</div><small>{{ n.createdAt | date:'medium' }}</small></div>
<div *ngIf="!items.length" class="empty">Aucune notification</div></div></div>` })
export class ClientNotificationsPageComponent implements OnInit {
  items: NotificationItem[] = [];
  constructor(private svc: ClientService) {}
  ngOnInit(): void { this.svc.getNotifications().subscribe(r => this.items = r); }
}
