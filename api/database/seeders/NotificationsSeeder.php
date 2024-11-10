<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Notification;
use App\Models\Motion;
use App\Models\Motions;
use App\Models\Notifications;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Faker\Factory as Faker;

class NotificationsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $faker = Faker::create();

        // Fetch the available motion IDs (assuming you have 3)
        $motionIds = Motions::pluck('id')->take(3)->toArray();

        // Fetch client users only
        $clientUsers = User::where('role', 'client')->pluck('id')->toArray();

        // Generate 30 notification records
        for ($i = 0; $i < 30; $i++) {
            Notifications::create([
                'motion_id' => $faker->randomElement($motionIds),
                'user_id' => $faker->randomElement($clientUsers),
                'screenshots' => '1731062006_potential_theft.jpg', // Static file path
                'created_at' => now(),
            ]);
        }
    }
}
