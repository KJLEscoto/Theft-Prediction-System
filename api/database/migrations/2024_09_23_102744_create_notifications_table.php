<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('notifications', function (Blueprint $table) {
            $table->id();
            $table->bigInteger('motion_id')->unsigned();
            $table->bigInteger('user_id')->unsigned();
            $table->string('screenshots');
            $table->timestamps();
            $table->softDeletes();

            // Set foreign keys
            $table->foreign('motion_id')->references('id')->on('motions')->onDelete('cascade');
            $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('notifications', function (Blueprint $table) {
            $table->dropForeign(['motion_id']);
            $table->dropForeign(['user_id']);
        });

        Schema::dropIfExists('notifications');
    }
};
