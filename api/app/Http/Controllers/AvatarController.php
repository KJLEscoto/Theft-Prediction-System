<?php

namespace App\Http\Controllers;

use App\Models\Avatars;
use Illuminate\Http\Request;

class AvatarController extends Controller
{
    public function index()
    {
        $avatars = Avatars::all();
        return response()->json($avatars);
    }

    public function set($id, Request $request)
    {
        $avatar = Avatars::findOrFail($id);

        // Validate the request to ensure avatar_count is provided
        $request->validate([
            'avatar_count' => 'required|integer',
        ]);

        // Update the avatar_count
        $avatar->avatar_count = $request->input('avatar_count');
        $avatar->save();

        return response()->json([
            'message' => 'Avatar count updated successfully',
            'avatar' => $avatar,
        ]);
    }
}
