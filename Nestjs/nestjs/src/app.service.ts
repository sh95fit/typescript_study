import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Get Hello';
  }

  postHello(): string {
    return 'Post Hello';
  }
}
