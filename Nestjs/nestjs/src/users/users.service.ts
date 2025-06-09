import { Injectable } from '@nestjs/common';
import { User } from './interface/users.interface';

@Injectable()
export class UsersService {

    private readonly users: User[] = [];

    findAll(): User[] {
        return this.users;
    }

    findOne(name: string): User | undefined {
        return this.users.find(user => user.name === name);
    }

    create(user: User): User {
        this.users.push(user);
        return user;
    }   
}
