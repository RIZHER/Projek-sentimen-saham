<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Redirect;
use Filament\Pages\Auth\Register as AuthRegister;

// Arahkan root ke halaman admin
Route::get('/', function () {
    return Redirect::to('/admin');
});