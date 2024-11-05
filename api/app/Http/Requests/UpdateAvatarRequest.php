<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateAvatarRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'avatar_count' => 'required|integer|min:0|max:500',
        ];
    }

    /**
     * Get the error messages for the defined validation rules.
     */
    public function messages(): array
    {
        return [
            'avatar_count.required' => 'The avatar count is required.',
            'avatar_count.integer' => 'The avatar count must be an integer.',
            'avatar_count.min' => 'The avatar count must be at least 0.',
            'avatar_count.max' => 'The avatar count may not be greater than 500.',
        ];
    }
}
