import {Customer} from './customer';

export interface Vehicle {
  customer: Customer;
  id: string;
  reg_no: string;
  heartbeat_ts: number;
  online: boolean;
}
