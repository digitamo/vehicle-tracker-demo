import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/internal/Observable';
import {Vehicle} from '../models/vehicle';
import {environment} from '../../environments/environment';

@Injectable()
export class ApiService {
  private apiBase: string;

  constructor(private http: HttpClient) {
    this.apiBase = environment.apiBase;
  }

  public search(customerName?: string, onlineStatus?: string): Observable<Vehicle[]> {
    const url = this.apiBase + 'search';

    const data = {};
    if (customerName !== undefined) {
      data['customer_name'] = customerName;
    }
    if (onlineStatus !== undefined) {
      data['online'] = onlineStatus;
    }
    return this.http.get<Vehicle[]>(url, {params: data});
  }

}
