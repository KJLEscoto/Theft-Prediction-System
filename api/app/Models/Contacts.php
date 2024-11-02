<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Contacts extends Model
{
    use HasFactory;

    protected $primaryKey = 'contact_id';

    protected $fillable = [
        'user_id',
        'contact_number',
        'is_enabled',
    ];

    // Define relationship to the User model
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
