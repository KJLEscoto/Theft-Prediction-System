<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateUserRequest extends FormRequest
{
    public function authorize()
    {
        return true; // You can implement authorization logic here
    }

    public function rules()
    {
        return [
            'first_name' => 'sometimes|string|max:255',
            'last_name' => 'sometimes|string|max:255',
            'middle_initial' => 'sometimes|nullable|string|regex:/^[A-Za-z]$/|max:1',
            'gender' => 'sometimes|string|in:male,female,other',
            'phone_number' => 'sometimes|string|size:10|regex:/^[0-9]{10}$/',
            'email' => 'sometimes|email|max:255|unique:users,email,' . $this->user()->id,
            'username' => 'sometimes|string|max:255|unique:users,username,' . $this->user()->id,
            'password' => 'sometimes|string|min:6',
            'avatar' => 'sometimes|string|nullable'
        ];
    }
}
