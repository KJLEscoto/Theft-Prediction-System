<?php

namespace Database\Seeders;

use App\Models\User;
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $users = [
            [
                'first_name' => 'kent',
                'last_name' => 'escoto',
                'middle_initial' => 'l',
                'gender' => 'male',
                'phone_number' => '9507541450',
                'status' => 'active',
                'role' => 'superadmin',
                'avatar' => '53',
                'username' => 'kentoy',
                'password' => 'password', 
                'email' => 'kentescoto24@gmail.com',
            ],
            [
                'first_name' => 'luis',
                'last_name' => 'suizo',
                'middle_initial' => 'g',
                'gender' => 'male',
                'phone_number' => '9507541450',
                'status' => 'active',
                'role' => 'admin',
                'avatar' => '3',
                'username' => 'luis',
                'password' => 'password', 
                'email' => 'lsuizo72@gmail.com',
            ],
            [
                'first_name' => 'rochy',
                'last_name' => 'cocjin',
                'middle_initial' => 'r',
                'gender' => 'female',
                'phone_number' => '9507541450',
                'status' => 'active',
                'role' => 'client',
                'username' => 'rochyyy',
                'password' => 'password', 
                'email' => 'rochyyy@gmail.com',
            ],
        ];

        foreach ($users as $user) {
            User::create($user);
        }
        
        // User::factory(10)->create();

        $this->call(MotionsSeeder::class);
    }
}