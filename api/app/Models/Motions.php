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
        'description',
        'video_path',
        'threshold'
    ];
}
