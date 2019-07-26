import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import * as Material from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    Material.MatToolbarModule,
    Material.MatGridListModule,
    Material.MatFormFieldModule,
    Material.MatInputModule,
    Material.MatButtonModule,
    Material.MatTableModule,
    Material.MatSortModule,
    Material.MatCheckboxModule,
    Material.MatIconModule
  ],
  exports: [
    Material.MatToolbarModule,
    Material.MatGridListModule,
    Material.MatFormFieldModule,
    Material.MatInputModule,
    Material.MatButtonModule,
    Material.MatTableModule,
    Material.MatSortModule,
    Material.MatCheckboxModule,
    Material.MatIconModule
  ],
  declarations: []
})
export class MaterialModule {
}
