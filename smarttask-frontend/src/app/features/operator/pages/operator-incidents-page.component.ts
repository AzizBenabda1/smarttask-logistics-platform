import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { OperatorService } from '../../../core/services/operator.service';
import { Incident } from '../../../core/models/role.models';

@Component({
  standalone: true, imports: [CommonModule, ReactiveFormsModule],
  template: `
<div class="page"><h1>Incidents</h1>
<form [formGroup]="form" class="card" style="max-width:480px;margin-bottom:1.5rem">
  <div class="field"><label>Type</label><select formControlName="type">
    <option value="WRONG_ADDRESS">Adresse incorrecte</option><option value="CLIENT_UNREACHABLE">Client injoignable</option>
    <option value="MISSING_PRODUCT">Produit manquant</option><option value="OTHER">Autre</option></select></div>
  <div class="field"><label>Description</label><input formControlName="description" /></div>
  <div class="field"><label>Priorité</label><select formControlName="priority">
    <option value="LOW">LOW</option><option value="MEDIUM">MEDIUM</option><option value="HIGH">HIGH</option><option value="CRITICAL">CRITICAL</option></select></div>
  <button class="btn btn-primary" (click)="submit()" [disabled]="form.invalid">Signaler</button>
</form>
<div class="card"><div *ngFor="let i of incidents" class="alert-item"><strong>{{ i.type }}</strong> — {{ i.description }}
<small>{{ i.createdAt | date:'short' }}</small></div></div></div>`,
  styles: [`.field{margin-bottom:1rem}.field label{display:block;font-size:.875rem}.field input,.field select{width:100%;padding:.6rem;border:1px solid #cbd5e1;border-radius:6px}`]
})
export class OperatorIncidentsPageComponent implements OnInit {
  incidents: Incident[] = [];
  form = this.fb.group({ type: ['OTHER', Validators.required], description: ['', Validators.required], priority: ['MEDIUM', Validators.required] });
  constructor(private fb: FormBuilder, private svc: OperatorService) {}
  ngOnInit(): void { this.load(); }
  load(): void { this.svc.getIncidents().subscribe(r => this.incidents = r); }
  submit(): void { this.svc.createIncident(this.form.value as any).subscribe(() => { this.form.reset({type:'OTHER',priority:'MEDIUM'}); this.load(); }); }
}
