import { Controller, Get, Param, Body, Post, Put, Delete } from '@nestjs/common';
import { CreateUserDto } from './CreateUserDto';
import { UpdateUserDto } from './UpdateUserDto';
import { UsersService } from './users.service';
import { User } from './interface/users.interface';

@Controller('users')
export class UsersController {

    constructor(private readonly usersService: UsersService) {};

    @Get()
    findAll(): User[] {
        return this.usersService.findAll();
    }

    @Get(':name')
    findOne(@Param('name') name: string): User | undefined {
        return this.usersService.findOne(name);
    }

    @Post()
    create(@Body() createUserDto: CreateUserDto) {
        return this.usersService.create(createUserDto);
    }

    @Put(':id')
    update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
        return `This action updates a #${id} user`;
    }

    @Delete(':id')
    remove(@Param('id') id: string) {
        return `This action removes a #${id} user`;
    }
}
