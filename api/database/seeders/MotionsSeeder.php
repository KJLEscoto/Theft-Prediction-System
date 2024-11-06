<?php

namespace Database\Seeders;

use App\Models\Motions;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class MotionsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $motions = [
            [
                'name' => 'looking around',
                'description' => 'This action is looking around.',
                'video_path' => 'looking_around.mp4',   
                'threshold' => fake()->randomFloat(1, 60, 100),
            ],
            [
                'name' => 'reaching',
                'description' => 'This action is reaching.',
                'video_path' => 'reaching.mp4',
                'threshold' => fake()->randomFloat(1, 60, 100),
            ],
            [
                'name' => 'conceal',
                'description' => 'This action is conceal.',
                'video_path' => 'conceal.mp4',
                'threshold' => fake()->randomFloat(1, 60, 100),
            ],
        ];

        foreach ($motions as $motion) {
            Motions::create($motion);
        }
    }
}