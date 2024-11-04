<?php

namespace Database\Seeders;

use App\Models\Avatars;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class AvatarSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $avatars = [
            [
                'avatar_count' => '30',
            ],
        ];

        foreach ($avatars as $avatar) {
            Avatars::create($avatar);
        }
    }
}
