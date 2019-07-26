import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {MatTableDataSource} from '@angular/material';
import {Vehicle} from '../../models/vehicle';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  private listData: MatTableDataSource<any>;
  private customerName: string;
  private online: boolean;
  public displayedColumns: string[] = ['id', 'reg-no', 'customer', 'online'];


  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
  }

  applyFilter() {
    this.apiService.search(this.customerName, this.online).subscribe(
      (vehicles: Array<Vehicle>) => {
        console.log('data >> ', vehicles);
        this.listData = new MatTableDataSource<any>(vehicles);
      }
    );
  }
}
