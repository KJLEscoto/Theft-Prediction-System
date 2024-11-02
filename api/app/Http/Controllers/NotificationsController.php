<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreNotificationsRequest;
use App\Http\Requests\UpdateNotificationsRequest;
use Illuminate\Http\Request;
use App\Models\Notifications;
use App\Models\User;
use Illuminate\Support\Facades\Auth;

class NotificationsController extends Controller
{
    /**
     * Display a listing of the notifications.
     */
    public function index()
    {
        // Return all notifications with their related motion and user
        return Notifications::with(['motion', 'user'])->get();
    }



    /**
     * Store a newly created notification in storage.
     */
    public function store(StoreNotificationsRequest $request)
    {
        $notifications = Notifications::create($request->validated());
        return response()->json($notifications, 201);
    }

    /**
     * Display the specified notification.
     */
    public function show($id)
    {
        $notifications = Notifications::find($id);

        if (!$notifications) {
            return response()->json(['message' => 'Motion not found'], 404);
        }

        return response()->json($notifications);
    }

    /**
     * Update the specified notification in storage.
     */
    public function update(UpdateNotificationsRequest $request, Notifications $notifications)
    {
        $notifications->update($request->validated());
        return response()->json($notifications);
    }

    /**
     * Remove the specified notification from storage.
     */
    public function destroy($id)
    {

        $notifications = Notifications::find($id);

        if (!$notifications) {
            return response()->json(['message' => 'Motion not found'], 404);
        }

        $notifications->delete();

        return 'Successfully deleted!';
    }


    public function getSpecificNotification($username)
    {
        // Find the user by the provided username
        $user = User::where('username', $username)->first();

        // Check if the user exists
        if (!$user) {
            return response()->json(['message' => 'User not found'], 404);
        }

        // Get the user's ID
        $userId = $user->id;

        // Fetch the notifications for the user by their ID
        $notifications = Notifications::with(['motion', 'user'])
            ->where('user_id', $userId)
            ->get();

        // Return the notifications as a JSON response
        return response()->json($notifications);
    }
}
