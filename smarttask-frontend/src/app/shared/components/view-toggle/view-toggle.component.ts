import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

export type ViewMode = 'cards' | 'list';

@Component({
  selector: 'app-view-toggle',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="view-toggle" role="group" aria-label="Mode d'affichage">
      <button type="button"
              [class.active]="mode === 'cards'"
              (click)="setMode('cards')"
              title="Vue cartes">
        ▦ Cartes
      </button>
      <button type="button"
              [class.active]="mode === 'list'"
              (click)="setMode('list')"
              title="Vue liste">
        ☰ Liste
      </button>
    </div>
  `
})
export class ViewToggleComponent {
  @Input() mode: ViewMode = 'cards';
  @Output() modeChange = new EventEmitter<ViewMode>();

  setMode(m: ViewMode): void {
    this.mode = m;
    this.modeChange.emit(m);
  }
}
