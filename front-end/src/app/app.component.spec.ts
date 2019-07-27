import {HttpClientModule} from '@angular/common/http';
import {async, ComponentFixture, fakeAsync, TestBed, tick} from '@angular/core/testing';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import {SearchComponent} from './components/search/search.component';
import {MaterialModule} from './material/material.module';
import {BrowserModule, By} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ApiService} from './services/api.service';
import {Observable, of} from 'rxjs';
import {Vehicle} from './models/vehicle';

class MockApiService {
  public mockVehicles = [
    {
      'customer': {
        'address': 'Cementvägen 8, 111 11 Södertälje',
        'id': 1,
        'name': 'Kalles Grustransporter AB'
      },
      'heartbeat_ts': null,
      'id': 'YS2R4X20005399401',
      'online': false,
      'reg_no': 'ABC123'
    },
    {
      'customer': {
        'address': 'Cementvägen 8, 111 11 Södertälje',
        'id': 1,
        'name': 'Kalles Grustransporter AB'
      },
      'heartbeat_ts': null,
      'id': 'VLUR4X20009093588',
      'online': false,
      'reg_no': 'DEF456'
    }
  ];

  // noinspection JSUnusedGlobalSymbols
  public search(customerName?: string, onlineStatus?: string): Observable<Vehicle[]> {
    return of(this.mockVehicles);
  }
}

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


describe('Integration test', () => {
  let fixture: ComponentFixture<AppComponent>;
  let customerNameEL;
  let onlineStatusEL;
  let searchComponent: SearchComponent;


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
      providers: [{provide: ApiService, useClass: MockApiService}]
    }).compileComponents();

  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);

    customerNameEL = fixture.debugElement.query(By.css('.vehicle__search-field input')).nativeElement;
    onlineStatusEL = fixture.debugElement.query(By.css('.vehicle__select-field mat-select')).nativeElement;
    searchComponent = fixture.debugElement.query(By.directive(SearchComponent)).componentInstance;

    fixture.detectChanges();
  });

  it('should show results when user types a customer name', async(() => {
    customerNameEL.value = 'test customer';
    customerNameEL.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    const tableEL = fixture.debugElement.query(By.css('mat-table'));
    const tableRowEls = fixture.debugElement.queryAll(By.css('mat-table mat-row'));

    expect(tableEL).toBeTruthy();
    expect(tableRowEls.length).toEqual(2);
  }));


  it('should show results when user selects online status and customer name', async(() => {
    customerNameEL.value = 'test customer';
    customerNameEL.dispatchEvent(new Event('input'));
    searchComponent.online = 'true';
    fixture.detectChanges();

    const tableEL = fixture.debugElement.query(By.css('mat-table'));
    const tableRowEls = fixture.debugElement.queryAll(By.css('mat-table mat-row'));

    expect(tableEL).toBeTruthy();
    expect(tableRowEls.length).toEqual(2);
  }));

});
