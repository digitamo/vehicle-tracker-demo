import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {SearchComponent} from './search.component';
import {ApiService} from '../../services/api.service';
import {BrowserModule} from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HttpClientModule} from '@angular/common/http';
import {MaterialModule} from '../../material/material.module';
import Spy = jasmine.Spy;
import {of} from 'rxjs';

describe('SearchComponent', () => {
  const mockVehicles = [
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

  let component: SearchComponent;
  let fixture: ComponentFixture<SearchComponent>;
  let apiService: ApiService;
  let searchSpy: Spy;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        BrowserModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
        HttpClientModule,
        FormsModule,
        MaterialModule,
      ],
      providers: [ApiService],
      declarations: [SearchComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchComponent);
    component = fixture.componentInstance;

    apiService = TestBed.get(ApiService);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('apply filter should call api service search function', async(() => {
    searchSpy = spyOn(apiService, 'search').and.returnValue(of([]));
    component.applyFilter();

    expect(searchSpy).toHaveBeenCalledWith(component.customerName, component.online);
    expect(component.listData.data).toEqual([]);
  }));

  it('apply customer filter should call api service search function with customer name', async(() => {
    searchSpy = spyOn(apiService, 'search').and.returnValue(of(mockVehicles));
    component.customerName = 'first name';
    component.applyFilter();

    expect(searchSpy).toHaveBeenCalledWith(component.customerName, component.online);
    expect(component.listData.data).toEqual(mockVehicles);
  }));

  it('apply online filter should call api service search function with online status', async(() => {
    searchSpy = spyOn(apiService, 'search').and.returnValue(of(mockVehicles));
    component.online = 'true';
    component.applyFilter();

    expect(searchSpy).toHaveBeenCalledWith(component.customerName, component.online);
    expect(component.listData.data).toEqual(mockVehicles);
  }));

  it('apply online and customer filter should call api service search function with online status and customer name',
    async(() => {
      searchSpy = spyOn(apiService, 'search').and.returnValue(of(mockVehicles));
      component.online = 'true';
      component.customerName = 'first name';
      component.applyFilter();

      expect(searchSpy).toHaveBeenCalledWith(component.customerName, component.online);
      expect(component.listData.data).toEqual(mockVehicles);
    }));
});
