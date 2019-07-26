import {HttpClientModule} from '@angular/common/http';
import {async, TestBed} from '@angular/core/testing';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import {SearchComponent} from './components/search/search.component';
import {MaterialModule} from './material/material.module';
import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ApiService} from './services/api.service';

describe('AppComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        SearchComponent
      ],
      imports: [
        BrowserModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
        HttpClientModule,
        FormsModule,
        MaterialModule,
      ],
      providers: [ApiService]
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

});
