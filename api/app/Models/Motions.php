<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Motions extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'motions';

    protected $fillable = [
        'name',
        'notification_id',
        'video_path',
        'threshold',
    ];

    public function notification()
    {
        return $this->belongsTo(Notifications::class, 'notification_id');
    }
}
