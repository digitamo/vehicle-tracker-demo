import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/internal/Observable';
import {Vehicle} from '../models/vehicle';

@Injectable()
export class ApiService {

  private url = 'http://localhost:5000/search';

  constructor(private http: HttpClient) {
  }

  public search(customerName?: string, onlineStatus?: boolean): Observable<any> {
    const data = {};

    if (customerName !== undefined) {
      data.customer_name = customerName;
    }
    if (onlineStatus !== undefined) {
      data.online = onlineStatus;
    }


    return this.http.get<Array<Vehicle>>(this.url, {params: data});
  }

}
