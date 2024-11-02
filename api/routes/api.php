<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\AvatarController;
use App\Http\Controllers\ContactController;
use App\Http\Controllers\MotionsController;
use App\Http\Controllers\NotificationsController;
use App\Http\Controllers\SmsController;

Route::post('register', [AuthController::class, 'register']);
Route::post('login', [AuthController::class, 'login']);

Route::post('auth/login', [AuthController::class, 'authenticateUser']);
Route::post('login/admin', [AuthController::class, 'loginAdmin']);
Route::middleware('auth:sanctum')->get('/user', [AuthController::class, 'getUser']);
Route::middleware('auth:sanctum')->post('/user/logout', [AuthController::class, 'logoutUser']);
Route::middleware('auth:sanctum')->put('/user/update', [AuthController::class, 'updateMainUser']);
Route::post('logout', [AuthController::class, 'logout'])->middleware('auth:sanctum');


Route::apiResource('motions', MotionsController::class);

Route::delete('/delete/{username}', [AuthController::class, 'deleteUser']);

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('notifications', NotificationsController::class);
});

Route::get('notification/{username}', [NotificationsController::class, 'getSpecificNotification']);

Route::middleware('auth:sanctum')->group(function () {
    Route::get('/users', [AuthController::class, 'getAllUsers']); // Get all users
    Route::get('/users/{username}', [AuthController::class, 'getUserById']); // Get a specific user by ID
    Route::put('/users/{username}', [AuthController::class, 'updateUser']); // Update a specific user
});

Route::put('status/{id}', [AuthController::class, 'setStatus']);

//otp
Route::post('/otp-email', [SmsController::class, 'sendEmail']);
Route::post('/otp-sms', [SmsController::class, 'sendSms']);

//warning
Route::post('/alert-sms', [SmsController::class, 'sendBulkSms']);
Route::post('/alert-emails', [SmsController::class, 'sendBulkEmail']);

Route::get('/avatars', [AvatarController::class, 'index']);
Route::put('/avatars/{id}', [AvatarController::class, 'set']);

Route::middleware('auth:sanctum')->get('/user/contact', [ContactController::class, 'index']);
Route::middleware('auth:sanctum')->post('/user/contact', [ContactController::class, 'store']);
Route::middleware('auth:sanctum')->delete('/user/contact/{contact_id}', [ContactController::class, 'destroy']);
Route::middleware('auth:sanctum')->put('/user/contact/{contact_id}', [ContactController::class, 'toggleEnable']);

Route::get('/active', [AuthController::class, 'getActive']);
Route::get('/inactive', [AuthController::class, 'getInactive']);
