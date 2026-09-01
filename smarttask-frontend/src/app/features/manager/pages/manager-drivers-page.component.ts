import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagerService } from '../../../core/services/manager.service';
import { Driver } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-drivers-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manager-drivers-page.component.html'
})
export class ManagerDriversPageComponent implements OnInit {
  drivers: Driver[] = [];

  constructor(private managerService: ManagerService) {}

  ngOnInit(): void {
    this.managerService.getDrivers().subscribe(d => this.drivers = d);
  }

  countByStatus(status: string): number {
    return this.drivers.filter(d => d.status === status).length;
  }
}
