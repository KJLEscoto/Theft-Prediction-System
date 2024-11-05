<?php

namespace App\Http\Controllers;

use App\Http\Requests\UpdateAvatarRequest;
use App\Models\Avatars;
use Illuminate\Http\Request;

class AvatarController extends Controller
{
    public function index()
    {
        $avatars = Avatars::all();
        return response()->json($avatars);
    }

    public function set($id, UpdateAvatarRequest $request)
    {
        $avatar = Avatars::findOrFail($id);

        // Update the avatar_count with validated data
        $avatar->avatar_count = $request->validated()['avatar_count'];
        $avatar->save();

        return response()->json([
            'message' => 'Avatar count updated successfully',
            'avatar' => $avatar,
        ]);
    }
}
