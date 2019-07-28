import {async, TestBed} from '@angular/core/testing';

import {ApiService} from './api.service';
import {HttpClient} from '@angular/common/http';
import {HttpClientTestingModule, HttpTestingController} from '@angular/common/http/testing';
import {RouterTestingModule} from '@angular/router/testing';
import {of} from 'rxjs';
import {environment} from '../../environments/environment';


describe('ApiService', () => {
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

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientTestingModule
      ],
      providers: [ApiService]
    });


    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);
  });

  it('should be created', () => {
    const service: ApiService = TestBed.get(ApiService);
    expect(service).toBeTruthy();
  });

  it('search with empty query string is should return an empty list', async(() => {
    const serviceSpy = spyOn(httpClient, 'get').and.returnValue(of([]));
    const apiBase = environment.apiBase;

    const service: ApiService = TestBed.get(ApiService);
    service.search().subscribe(
      result => expect(result).toEqual([]),
      fail
    );

    const url = apiBase + 'search';
    const queryParams = {};

    expect(serviceSpy).toHaveBeenCalledWith(url, {params: queryParams});
  }));

  it('search with customer name should call api with customer name as query parameters', async(() => {
    const serviceSpy = spyOn(httpClient, 'get').and.returnValue(of(mockVehicles));
    const apiBase = environment.apiBase;
    const customerName = 'first name';

    const service: ApiService = TestBed.get(ApiService);
    service.search(customerName).subscribe(
      result => expect(result).toEqual(mockVehicles),
      fail
    );

    const url = apiBase + 'search';
    const queryParams = {customer_name: customerName};

    expect(serviceSpy).toHaveBeenCalledWith(url, {params: queryParams});
  }));

  it('search with online status should call api with online as query parameters', async(() => {
    const serviceSpy = spyOn(httpClient, 'get').and.returnValue(of(mockVehicles));
    const apiBase = environment.apiBase;
    const online = 'true';

    const service: ApiService = TestBed.get(ApiService);
    service.search(undefined, online).subscribe(
      result => expect(result).toEqual(mockVehicles),
      fail
    );

    const url = apiBase + 'search';
    const queryParams = {online};

    expect(serviceSpy).toHaveBeenCalledWith(url, {params: queryParams});
  }));

  it('search with online status and customer name should call api with online and customer name as query parameters', async(() => {
    const serviceSpy = spyOn(httpClient, 'get').and.returnValue(of(mockVehicles));
    const apiBase = environment.apiBase;
    const online = 'true';
    const customerName = 'first name';

    const service: ApiService = TestBed.get(ApiService);
    service.search(customerName, online).subscribe(
      result => expect(result).toEqual(mockVehicles),
      fail
    );

    const url = apiBase + 'search';
    const queryParams = {online, customer_name: customerName};

    expect(serviceSpy).toHaveBeenCalledWith(url, {params: queryParams});
  }));
});
