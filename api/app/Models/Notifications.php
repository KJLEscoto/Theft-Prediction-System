<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Notifications extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'notifications';

    protected $fillable = [
        'user_id',
        'screenshots',
    ];

    public function user()
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function motions()
    {
        return $this->hasMany(Motions::class, 'notification_id');
    }
}
