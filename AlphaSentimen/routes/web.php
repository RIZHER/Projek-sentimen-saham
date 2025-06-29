<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Redirect;
use App\Http\Controllers\PublicController; // Import controller Anda

// Arahkan root ke halaman admin
Route::get('/', function () {
    return Redirect::to('/admin');
});

// Rute untuk halaman daftar berita publik
// Bisa menerima parameter saham_id untuk filter
Route::get('/news', [PublicController::class, 'listNews'])->name('public.news.list');