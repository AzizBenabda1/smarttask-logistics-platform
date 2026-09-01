import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManagerService } from '../../../core/services/manager.service';
import { DelayedTask } from '../../../core/models/manager.models';

@Component({
  selector: 'app-manager-delays-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manager-delays-page.component.html'
})
export class ManagerDelaysPageComponent implements OnInit {
  delays: DelayedTask[] = [];

  constructor(private managerService: ManagerService) {}

  ngOnInit(): void {
    this.managerService.getDelays().subscribe(d => this.delays = d);
  }
}
