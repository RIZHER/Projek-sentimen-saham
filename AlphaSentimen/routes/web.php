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

Route::post('/posts', [PublicController::class, 'storePost'])
    ->middleware('auth') // Hanya user terautentikasi yang bisa memposting
    ->name('public.post.store');
