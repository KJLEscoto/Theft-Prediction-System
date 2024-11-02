<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Http;

class SmsController extends Controller
{
    // email OTP
    public function sendEmail(Request $request)
    {
        // Validate the email input
        $validator = Validator::make($request->all(), [
            'email' => 'required|email',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Invalid email address',
            ], 400);
        }

        $otp = rand(100000, 999999);

        $mail = new PHPMailer(true);

        try {
            // Server settings
            $mail->isSMTP();
            $mail->Host = env('GMAIL_HOST');
            $mail->SMTPAuth = true;
            $mail->Username = env('GMAIL_USERNAME');
            $mail->Password = env('GMAIL_PASSWORD');
            $mail->SMTPSecure = env('GMAIL_SMTPSecure');
            $mail->Port = env('PORT');

            // Recipients
            $mail->setFrom(env('GMAIL_USERNAME'), env('APP_NAME'));
            $mail->addAddress($request->email);

            // Content
            $mail->isHTML(false);
            $mail->Subject = 'Verification';
            $mail->Body    = "Your OTP code is: $otp";

            $mail->send();

            // Return the OTP in the response for verification on the frontend
            return response()->json([
                'status' => 'success',
                'otp' => $otp,
            ], 200);
        } catch (Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Sending failed. Mailer Error: ' . $mail->ErrorInfo,
            ], 500);
        }
    }

    public function sendBulkEmail(Request $request)
    {
        // Validate the input
        $validator = Validator::make($request->all(), [
            'emails' => 'required',
            'emails.*' => 'required',
            'message' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Invalid input',
                'errors' => $validator->errors(),
            ], 400);
        }

        // Get the list of email addresses and the message from the request
        $emails = $request->emails;
        $messageContent = $request->message;

        // Variable to track failed emails
        $failedEmails = [];

        // Create a new PHPMailer instance
        $mail = new PHPMailer(true);

        try {
            // Server settings
            $mail->isSMTP();
            $mail->Host = env('GMAIL_HOST');
            $mail->SMTPAuth = true;
            $mail->Username = env('GMAIL_USERNAME');
            $mail->Password = env('GMAIL_PASSWORD');
            $mail->SMTPSecure = env('GMAIL_SMTPSecure');
            $mail->Port = env('PORT');

            // Set the sender's information
            $mail->setFrom(env('GMAIL_USERNAME'), env('APP_NAME'));

            // Loop through each email address
            foreach ($emails as $email) {
                // Clear all recipients and add the new one
                $mail->clearAddresses();
                $mail->addAddress($email);

                // Content
                $mail->isHTML(false);
                $mail->Subject = 'Notification';
                $mail->Body    = $messageContent;

                // Try sending the email
                try {
                    $mail->send();
                } catch (Exception $e) {
                    // If sending fails, store the failed email
                    $failedEmails[] = $email;
                }
            }

            // If any emails failed, return a partial success response
            if (count($failedEmails) > 0) {
                return response()->json([
                    'status' => 'partial_success',
                    'message' => 'Some emails failed to send',
                    'failed_emails' => $failedEmails,
                ], 207);
            }

            // All emails were sent successfully
            return response()->json([
                'status' => 'success',
                'message' => 'All emails sent successfully',
            ], 200);
        } catch (Exception $e) {
            // Catch any errors with the mail setup or sending
            return response()->json([
                'status' => 'error',
                'message' => 'Mail sending failed. Error: ' . $e->getMessage(),
            ], 500);
        }
    }

    // sms otp
    public function sendSms(Request $request)
    {
        // Validate the phone number input
        $validator = Validator::make($request->all(), [
            'phone_number' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Invalid phone number',
            ], 400);
        }

        // Generate a random 6-digit OTP
        $otp = rand(100000, 999999);

        // Traccar SMS Gateway URL
        $url = env('SMS_GATEWAY');

        // Prepare the data for the request body
        $postData = [
            'to' => $request->phone_number,
            'message' => "Your Verification Code is: '$otp'",
        ];

        try {
            // Send the request to the SMS gateway
            $response = Http::withHeaders([
                'Authorization' => env('SMS_AUTHORIZATION'),
            ])->post($url, $postData);

            // Check if the SMS was sent successfully
            if ($response->successful()) {
                return response()->json([
                    'status' => 'success',
                    'otp' => $otp,
                ], 200);
            } else {
                return response()->json([
                    'status' => 'error',
                    'message' => 'Failed to send SMS: ' . $response->body(),
                ], 500);
            }
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'SMS sending failed. Error: ' . $e->getMessage(),
            ], 500);
        }
    }

    // send bulk
    public function sendBulkSms(Request $request)
    {
        // Validate the input
        $validator = Validator::make($request->all(), [
            'phone_numbers' => 'required|array',
            'phone_numbers.*' => 'required',
            'message' => 'required',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Invalid input',
                'errors' => $validator->errors(),
            ], 400);
        }

        // Get the list of phone numbers and the message from the request
        $phoneNumbers = $request->phone_numbers;
        $message = $request->message;

        // Traccar SMS Gateway URL
        $url = env('SMS_GATEWAY');

        // Variable to track failed numbers
        $failedNumbers = [];

        // Loop through each phone number
        foreach ($phoneNumbers as $phoneNumber) {
            // Prepare the data for the request body for each number
            $postData = [
                'to' => $phoneNumber,
                'message' => $message,
            ];

            try {
                // Send the request to the SMS gateway
                $response = Http::withHeaders([
                    'Authorization' => env('SMS_AUTHORIZATION'),
                ])->post($url, $postData);

                // Check if the SMS was sent successfully
                if (!$response->successful()) {
                    // If sending fails, store the failed number
                    $failedNumbers[] = $phoneNumber;
                }
            } catch (\Exception $e) {
                // If an exception occurs, store the failed number
                $failedNumbers[] = $phoneNumber;
            }
        }

        // If any numbers failed, return an error message
        if (count($failedNumbers) > 0) {
            return response()->json([
                'status' => 'partial_success',
                'message' => 'Some messages failed to send',
                'failed_numbers' => $failedNumbers,
            ], 207); // HTTP 207 Multi-Status for partial success
        }

        // All messages were sent successfully
        return response()->json([
            'status' => 'success',
            'message' => 'All messages sent successfully',
        ], 200);
    }
}
