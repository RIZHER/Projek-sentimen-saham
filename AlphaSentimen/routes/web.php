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

// Rute untuk menyimpan postingan baru, dilindungi oleh middleware 'auth'
Route::post('/posts', [PublicController::class, 'storePost'])
    ->middleware('auth') // Hanya user terautentikasi yang bisa memposting
    ->name('public.post.store');

// Rute untuk menghapus postingan, dilindungi oleh middleware 'auth'
Route::delete('/posts/{postinganId}', [PublicController::class, 'deletePost'])
    ->middleware('auth') // Hanya user terautentikasi yang bisa menghapus
    ->name('public.post.delete');
