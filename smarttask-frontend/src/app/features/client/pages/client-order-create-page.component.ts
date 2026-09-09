import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ClientService } from '../../../core/services/client.service';
import { ProductType, ProductTypeService } from '../../../core/services/product-type.service';
import { DeliverySuccessPrediction } from '../../../core/models/ai.models';
import { OrderRequest } from '../../../core/models/role.models';
import { AlertBannerComponent } from '../../../shared/components/alert-banner/alert-banner.component';
import { ToastService } from '../../../shared/services/toast.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink, AlertBannerComponent],
  template: `
<div class="page">
  <div class="page-header">
    <div>
      <h1>Nouvelle commande</h1>
      <p class="subtitle">Votre commande sera vérifiée par un opérateur avant traitement</p>
    </div>
    <a routerLink="/client/orders" class="btn btn-secondary">Retour</a>
  </div>

  <app-alert-banner
    type="info"
    title="Validation opérateur"
    message="Après envoi, un opérateur vérifiera et validera ou annulera votre commande avant qu'elle soit transmise au manager."
    [dismissible]="true">
  </app-alert-banner>

  <form [formGroup]="form" class="card form-card">
    <div class="form-grid">
      <div class="form-field">
        <label>Type de produit *</label>
        <select formControlName="productTypeSelection">
          <option [ngValue]="null">— Choisir —</option>
          <option *ngFor="let t of productTypes" [ngValue]="t.id">{{ t.name }}</option>
          <option [ngValue]="OTHER">Autre (preciser)</option>
        </select>
      </div>

      <div class="form-field" *ngIf="isOtherType" style="grid-column:1/-1">
        <label>Autre type *</label>
        <input formControlName="customProductType" placeholder="Ex. Materiel medical specialise" />
      </div>

      <div class="form-field" style="grid-column:1/-1">
        <label>Details (optionnel)</label>
        <input formControlName="products" placeholder="Precisions sur le contenu" />
      </div>

      <div class="form-field"><label>Quantite</label><input type="number" formControlName="quantity" /></div>
      <div class="form-field"><label>Montant *</label><input type="number" formControlName="amount" /></div>
      <div class="form-field"><label>Telephone</label><input formControlName="phone" /></div>
      <div class="form-field" style="grid-column:1/-1"><label>Adresse *</label><input formControlName="deliveryAddress" /></div>
      <div class="form-field"><label>Date</label><input type="date" formControlName="scheduledDate" /></div>
      <div class="form-field">
        <label>Priorite</label>
        <select formControlName="priority">
          <option value="LOW">LOW</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="HIGH">HIGH</option>
          <option value="CRITICAL">CRITICAL</option>
        </select>
      </div>
      <div class="form-field" style="grid-column:1/-1">
        <label>Instructions</label>
        <input formControlName="instructions" />
      </div>
    </div>

    <div class="success-ai-panel" *ngIf="successPreview as sp">
      <h3>Score reussite livraison</h3>
      <div class="flex items-center gap-sm flex-wrap">
        <span class="success-score">{{ successPercent() }}%</span>
        <span class="badge" [ngClass]="sp.riskLevel">{{ sp.riskLevel }}</span>
      </div>
      <ul><li *ngFor="let f of sp.factors">{{ f }}</li></ul>
    </div>

    <app-alert-banner *ngIf="error" type="error" [title]="'Erreur'" [message]="error" (dismissed)="error = ''"></app-alert-banner>

    <div class="form-actions">
      <button type="button" class="btn btn-secondary btn-ai" (click)="analyzeSuccess()" [disabled]="form.invalid || analyzing">
        {{ analyzing ? 'Analyse...' : 'Analyser reussite IA' }}
      </button>
      <button type="button" class="btn btn-primary" (click)="save()" [disabled]="form.invalid">Envoyer la commande</button>
    </div>
  </form>
</div>`
})
export class ClientOrderCreatePageComponent implements OnInit {
  readonly OTHER = 'OTHER';
  productTypes: ProductType[] = [];
  error = '';
  analyzing = false;
  successPreview: DeliverySuccessPrediction | null = null;

  form = this.fb.group({
    productTypeSelection: [null as number | string | null, Validators.required],
    customProductType: [''],
    products: [''],
    quantity: [1, Validators.min(1)],
    amount: [0, Validators.required],
    phone: [''],
    deliveryAddress: ['', Validators.required],
    scheduledDate: [''],
    priority: ['MEDIUM', Validators.required],
    instructions: ['']
  });

  constructor(
    private fb: FormBuilder,
    private svc: ClientService,
    private productTypesSvc: ProductTypeService,
    private router: Router,
    private toast: ToastService
  ) {}

  ngOnInit(): void {
    this.productTypesSvc.list().subscribe({
      next: t => this.productTypes = t,
      error: () => this.error = 'Impossible de charger les types de produit.'
    });
    this.form.get('productTypeSelection')?.valueChanges.subscribe(v => {
      const ctrl = this.form.get('customProductType');
      if (v === this.OTHER) {
        ctrl?.setValidators([Validators.required, Validators.maxLength(150)]);
      } else {
        ctrl?.clearValidators();
        ctrl?.setValue('');
      }
      ctrl?.updateValueAndValidity();
    });
  }

  get isOtherType(): boolean { return this.form.value.productTypeSelection === this.OTHER; }

  save(): void {
    if (this.form.invalid) return;
    this.svc.createOrder(this.buildPayload()).subscribe({
      next: () => {
        this.toast.success('Commande envoyee — en attente de validation operateur');
        this.router.navigate(['/client/orders']);
      },
      error: e => this.error = e.error?.message || 'Erreur lors de la creation'
    });
  }

  analyzeSuccess(): void {
    if (this.form.invalid) return;
    this.analyzing = true;
    this.error = '';
    this.svc.previewDeliverySuccess(this.buildPayload()).subscribe({
      next: r => {
        this.successPreview = r;
        this.analyzing = false;
        this.toast.info(`Score reussite : ${Math.round(r.successProbability * 100)}%`);
      },
      error: e => {
        this.analyzing = false;
        this.error = e.error?.message || 'Service IA indisponible';
      }
    });
  }

  successPercent(): number {
    return this.successPreview ? Math.round(this.successPreview.successProbability * 100) : 0;
  }

  private buildPayload(): OrderRequest {
    const v = this.form.value;
    const payload: OrderRequest = {
      products: v.products || undefined,
      quantity: v.quantity!,
      amount: v.amount!,
      phone: v.phone || undefined,
      deliveryAddress: v.deliveryAddress!,
      scheduledDate: v.scheduledDate || undefined,
      priority: v.priority!,
      instructions: v.instructions || undefined
    };
    if (v.productTypeSelection === this.OTHER) {
      payload.customProductType = v.customProductType ?? undefined;
    } else if (v.productTypeSelection != null && v.productTypeSelection !== this.OTHER) {
      payload.productTypeId = Number(v.productTypeSelection);
    }
    return payload;
  }
}
