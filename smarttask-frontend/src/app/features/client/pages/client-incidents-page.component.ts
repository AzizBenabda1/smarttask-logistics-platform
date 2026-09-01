import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ClientService } from '../../../core/services/client.service';

@Component({ standalone: true, imports: [CommonModule, ReactiveFormsModule],
  template: `<div class="page"><h1>Signaler un problème</h1>
<form [formGroup]="form" class="card" style="max-width:480px">
  <div class="field"><label>Commande ID</label><input type="number" formControlName="orderId" /></div>
  <div class="field"><label>Type</label><select formControlName="type">
    <option value="MISSING_PRODUCT">Produit manquant</option><option value="DAMAGED_PRODUCT">Produit endommagé</option>
    <option value="DELAY">Retard</option><option value="OTHER">Autre</option></select></div>
  <div class="field"><label>Description</label><input formControlName="description" /></div>
  <button class="btn btn-primary" (click)="submit()" [disabled]="form.invalid">Envoyer</button>
</form></div>`,
  styles: [`.field{margin-bottom:1rem}.field label{display:block;font-size:.875rem}.field input,.field select{width:100%;padding:.6rem;border:1px solid #cbd5e1;border-radius:6px}`]
})
export class ClientIncidentsPageComponent {
  form = this.fb.group({ orderId: [null as number | null], type: ['OTHER', Validators.required], description: ['', Validators.required], priority: ['MEDIUM'] });
  constructor(private fb: FormBuilder, private svc: ClientService) {}
  submit(): void { this.svc.createIncident(this.form.value as any).subscribe(() => this.form.reset({type:'OTHER',priority:'MEDIUM'})); }
}
