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
                'first_name' => 'monkey',
                'last_name' => 'luffy',
                'middle_initial' => 'd',
                'gender' => 'male',
                'phone_number' => '9507541450',
                'status' => 'active',
                'role' => 'superadmin',
                'avatar' => '25',
                'username' => 'superadmin',
                'password' => 'superadmin123', 
                'email' => 'dummy.superadmin@gmail.com',
            ],
            [
                'first_name' => 'roronoa',
                'last_name' => 'zoro',
                'middle_initial' => 'g',
                'gender' => 'male',
                'phone_number' => '9507541450',
                'status' => 'active',
                'role' => 'admin',
                'avatar' => '5',
                'username' => 'admin',
                'password' => 'admin123', 
                'email' => 'dummy.admin@gmail.com',
            ],
            [
                'first_name' => 'nico',
                'last_name' => 'robin',
                'middle_initial' => 'r',
                'gender' => 'female',
                'phone_number' => '9507541450',
                'status' => 'active',
                'avatar' => '10',
                'role' => 'client',
                'username' => 'client',
                'password' => 'client123', 
                'email' => 'dummy.client@gmail.com',
            ],
        ];

        foreach ($users as $user) {
            User::create($user);
        }
        
        User::factory(10)->create();

        // $this->call(NotificationsSeeder::class);
        $this->call(AvatarSeeder::class);
    }
}