<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Notifications extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'motion_id',
        'user_id',
        'screenshots',
    ];

    public function motion()
    {
        return $this->belongsTo(Motions::class, 'motion_id'); // Adjust the foreign key if needed
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
