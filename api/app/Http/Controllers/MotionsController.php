<?php

namespace App\Http\Controllers;

use App\Models\Motions;
use App\Http\Requests\StoreMotionsRequest;
use App\Http\Requests\UpdateMotionsRequest;

class MotionsController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return Motions::all();
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreMotionsRequest $request)
    {
        $fields = $request->validated();

        $motions = Motions::create($fields);

        return $motions;
    }

    /**
     * Display the specified resource.
     */
    public function show($id)
    {
        $motion = Motions::find($id);
        
        if (!$motion) {
            return response()->json(['message' => 'Motion not found'], 404);
        }
        
        return response()->json($motion);
    }


    /**
     * Update the specified resource in storage.
     */
    public function update(UpdateMotionsRequest $request, $id)
    {
        $motion = Motions::find($id);

        if (!$motion) {
            return response()->json(['message' => 'Motion not found'], 404);
        }

        // Validate and update the motion with the validated fields
        $motion->update($request->validated());

        return response()->json($motion);
    }


    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {

        $motion = Motions::find($id);

        if (!$motion) {
            return response()->json(['message' => 'Motion not found'], 404);
        }

        $motion->delete();

        return $motion; 
    }


}
