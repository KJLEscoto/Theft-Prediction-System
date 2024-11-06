<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreContactRequest;
use Illuminate\Http\Request;
use App\Models\Contacts;
use Illuminate\Support\Facades\Auth;

class ContactController extends Controller
{
    /**
     * Display a listing of the contacts for the authenticated user.
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function index()
    {
        $contacts = Contacts::where('user_id', Auth::id())->get();
        return response()->json($contacts);
    }

    /**
     * Store a new contact for the authenticated user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function store(StoreContactRequest $request)
    {
        // Check if the user already has 3 contacts
        $contactCount = Contacts::where('user_id', Auth::id())->count();

        // if ($contactCount >= 3) {
        //     return response()->json(['message' => 'You can only have up to 3 contacts.'], 400);
        // }

        $contact = Contacts::create([
            'user_id' => Auth::id(),
            'contact_number' => $request->contact_number,
            'is_enabled' => $request->is_enabled,
        ]);

        return response()->json($contact, 201);
    }



    /**
     * Remove a contact of the authenticated user.
     *
     * @param  int  $id
     * @return \Illuminate\Http\JsonResponse
     */
    public function destroy($contact_id)
    {
        // Find the contact by contact_id and ensure it belongs to the authenticated user
        $contact = Contacts::where('user_id', Auth::id())
            ->where('contact_id', $contact_id)
            ->firstOrFail(); // This will throw a 404 if not found

        // Delete the contact
        $contact->delete();

        return response()->json(['message' => 'Contact deleted successfully.']);
    }


    /**
     * Toggle the enable/disable status of a contact for the authenticated user.
     *
     * @param  int  $id
     * @return \Illuminate\Http\JsonResponse
     */
    public function toggleEnable($contact_id)
    {
        // Find the contact by contact_id
        $contact = Contacts::where('contact_id', $contact_id)->firstOrFail();

        // Toggle the is_enabled status
        $contact->is_enabled = !$contact->is_enabled;
        $contact->save();

        return response()->json(['message' => 'Contact status updated successfully.', 'contact' => $contact]);
    }

    public function fetchEnabled()
    {
        $enabledContacts = Contacts::where('user_id', Auth::id())
                                ->where('is_enabled', 1)
                                ->get();
        
        return response()->json($enabledContacts);
    }

}
