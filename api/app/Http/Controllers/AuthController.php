<?php

namespace App\Http\Controllers;

use App\Http\Requests\AuthenticateUserRequest;
use App\Http\Requests\AuthRequest;
use Illuminate\Http\Request;
use App\Http\Requests\LoginRequest; // Ensure correct import
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\AuthenticatedUserResource;
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Response;
use Illuminate\Validation\ValidationException as ValidationValidationException;

class AuthController extends Controller
{

    public function authenticateUser(AuthenticateUserRequest $payload)
    {
        $username = $payload->username;
        $password = $payload->password;

        $user = User::where('username', $username)->first();

        // Check if the user exists and if the password is correct
        if (!$user || $password !== $user->password) {
            throw ValidationValidationException::withMessages([
                'username' => ['Invalid login credentials.'],
            ]);
        }

        // Check if the user's status is inactive
        if ($user->status === 'inactive') {
            throw ValidationValidationException::withMessages([
                'username' => ['Your account is inactive. Please contact support.'],
            ]);
        }

        // Check if the user is admin or superadmin and block access
        if (in_array($user->role, ['admin', 'superadmin'])) {
            throw ValidationValidationException::withMessages([
                'username' => ['Access denied. Clients only.'],
            ]);
        }

        // Create token for authenticated client user
        $response = (object) [
            'user' => $user,
            'token' => $user->createToken('auth-token')->plainTextToken
        ];

        return new AuthenticatedUserResource($response);
    }



    public function updateMainUser(UpdateUserRequest $request)
    {
        // Retrieve the authenticated user
        $user = $request->user();

        // Update the user with validated data from the request
        $user->update($request->validated());

        // Return a success response
        return response()->json([
            'user' => $user,
            'message' => 'User updated successfully.'
        ]);
    }



    public function register(AuthRequest $request)
    {
        $user = User::create($request->validated());

        return response()->json([
            'user' => $user
        ]);
    }

    public function login(LoginRequest $request)
    {
        $user = User::where('username', $request->username)->first();

        // Check if the user exists and the password matches
        if (!$user || !Hash::check($request->password, $user->password)) {
            return response()->json([
                'message' => 'The provided credentials are incorrect.'
            ], 401); // Return 401 Unauthorized
        }

        // Create a token for the authenticated user
        $token = $user->createToken($request->username)->plainTextToken;

        return response()->json([
            'user' => $user,
            'token' => $token
        ]);
    }

    public function logout(Request $request)
    {
        $request->user()->tokens()->delete();

        return response()->json([
            'message' => 'You are logged out.'
        ]);
    }

    public function getUser(Request $request)
    {
        $user = $request->user();
        $user->makeVisible('password'); // Temporarily unhide the password
        return response()->json($user);
    }

    public function loginAdmin(LoginRequest $request)
    {
        $user = User::where('username', $request->username)->first();

        // Check if the user exists (without checking the password)
        if (!$user) {
            return response()->json([
                'message' => 'The provided credentials are incorrect.'
            ], 401); // Return 401 Unauthorized
        }

        // Check if the user's status is inactive
        if ($user->status === 'inactive') {
            return response()->json([
                'message' => 'Your account is inactive. Please contact support.'
            ], 403); // Return 403 Forbidden for inactive status
        }

        // Check if the user is an admin or superadmin
        if (!in_array($user->role, ['admin', 'superadmin'])) {
            return response()->json([
                'message' => 'Access denied. Admins only.'
            ], 403); // Return 403 Forbidden
        }

        // Create a token for the authenticated admin user
        $token = $user->createToken($request->username)->plainTextToken;

        return response()->json([
            'user' => $user,
            'token' => $token
        ]);
    }


    public function logoutUser(Request $request)
    {
        $user = $request->user();
        $user->tokens()->delete();
        return 'Success';
    }

    public function updateUser(UpdateUserRequest $request, $username)
    {
        // Find the user by username
        $user = User::where('username', $username)->first();

        if (!$user) {
            return response()->json(['message' => 'User not found.'], 404);
        }

        // Update the user with validated data from the request
        $user->update($request->validated());

        return response()->json([
            'user' => $user,
            'message' => 'User updated successfully.'
        ]);
    }


    public function getAllUsers()
    {
        $users = User::where('id', '!=', Auth::id())->get(); // Fetch all users except the current authenticated user
        return response()->json($users);
    }

    public function getUserById($username)
    {
        // Find the user by username
        $user = User::where('username', $username)->first();

        if (!$user) {
            return response()->json(['message' => 'User not found'], 404);
        }

        return response()->json([
            'user' => $user,
            'message' => 'User retrieved successfully.'
        ]);
    }

    public function setStatus(Request $request, $id)
    {
        $user = User::find($id);

        if (!$user) {
            return response()->json(['message' => 'User not found.'], 404);
        }

        // Toggle the status
        $user->status = $user->status === 'active' ? 'inactive' : 'active';
        $user->save();

        return response()->json([
            'user' => $user,
            'message' => 'User status updated successfully.',
        ]);
    }

    public function deleteUser($username)
    {
        // Find the user by username
        $user = User::where('username', $username)->first();

        if (!$user) {
            return response()->json(['message' => 'User not found.'], 404);
        }

        // Delete the user
        $user->delete();

        return response()->json(['message' => 'User deleted successfully.']);
    }

    public function getActive()
    {
        $activeUsers = User::where('status', 'active')->get();
        return response()->json($activeUsers);
    }

    public function getInactive()
    {
        $inactiveUsers = User::where('status', 'inactive')->get();
        return response()->json($inactiveUsers);
    }
}
