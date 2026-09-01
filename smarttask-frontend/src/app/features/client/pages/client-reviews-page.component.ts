import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ClientService } from '../../../core/services/client.service';
import { Review } from '../../../core/models/role.models';

@Component({ standalone: true, imports: [CommonModule, ReactiveFormsModule],
  template: `<div class="page"><h1>Mes évaluations</h1>
<form [formGroup]="form" class="card" style="max-width:400px;margin-bottom:1.5rem">
  <div class="field"><label>Tâche ID</label><input type="number" formControlName="taskId" /></div>
  <div class="field"><label>Note (1-5)</label><input type="number" min="1" max="5" formControlName="rating" /></div>
  <div class="field"><label>Commentaire</label><input formControlName="comment" /></div>
  <button class="btn btn-primary" (click)="submit()" [disabled]="form.invalid">Évaluer</button>
</form>
<div class="card"><div *ngFor="let r of reviews">⭐ {{ r.rating }}/5 — {{ r.comment }} <small>{{ r.createdAt | date:'short' }}</small></div></div></div>`,
  styles: [`.field{margin-bottom:1rem}.field label{display:block;font-size:.875rem}.field input{width:100%;padding:.6rem;border:1px solid #cbd5e1;border-radius:6px}`]
})
export class ClientReviewsPageComponent implements OnInit {
  reviews: Review[] = [];
  form = this.fb.group({ taskId: [null as number | null, Validators.required], rating: [5, [Validators.min(1), Validators.max(5)]], comment: [''] });
  constructor(private fb: FormBuilder, private svc: ClientService) {}
  ngOnInit(): void { this.svc.getReviews().subscribe(r => this.reviews = r); }
  submit(): void { this.svc.createReview(this.form.value as any).subscribe(() => { this.form.reset({rating:5}); this.ngOnInit(); }); }
}
