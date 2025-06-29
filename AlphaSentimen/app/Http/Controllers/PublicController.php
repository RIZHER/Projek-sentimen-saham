<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Berita;
use App\Models\SahamProfile;
use App\Models\Postingan; // Import model Postingan
use App\Models\User; // Import model User
use Illuminate\Support\Str; // Import Str for markdown
use Illuminate\Support\Facades\Auth; // Import Auth Facade

class PublicController extends Controller
{
    public function listNews(Request $request)
    {
        $sahamId = $request->input('saham_id');
        
        $saham = SahamProfile::find($sahamId);

        if (!$saham) {
            abort(404, 'Saham tidak ditemukan.');
        }

        $beritas = Berita::where('saham_id', $sahamId)
                         ->orderBy('created_at', 'desc')
                         ->paginate(10); 
        
        $beritas->appends(request()->query());

        // Ambil postingan terkait saham ini
        $postingans = Postingan::where('saham_id', $sahamId)
                               ->orderBy('created_at', 'desc')
                               ->get(); 
        
        // --- Logic untuk filter postingan public/private berdasarkan user yang login ---
        $filteredPostings = $postingans->filter(function ($post) {
            return $post->status === 'public' || (Auth::check() && $post->user_id === Auth::id());
        });

        $heading = 'Berita Saham: ' . $saham->nama_saham . ' (' . $saham->kode_saham . ')';

        // Teruskan status autentikasi ke view
        return view('public.news-list', [
            'beritas' => $beritas,
            'heading' => $heading,
            'saham' => $saham,
            'postingans' => $filteredPostings, // Gunakan postingan yang sudah difilter
            'isAuthenticated' => Auth::check(), // Cek apakah user login
            'currentUserId' => Auth::id(), // Teruskan ID user yang login untuk verifikasi di view
        ]);
    }

    public function storePost(Request $request)
    {
        // Pastikan pengguna sudah login untuk membuat postingan
        if (!Auth::check()) {
            return back()->withErrors(['auth_error' => 'Anda harus login untuk membuat postingan.']);
        }

        // Validasi input
        $request->validate([
            'saham_id' => 'required|exists:saham_profile,saham_id',
            'judul_postingan' => 'required|string|max:255',
            'isi_postingan' => 'required|string',
            'status' => 'required|in:public,private',
        ]);
        
        Postingan::create([
            'saham_id' => $request->saham_id,
            'user_id' => Auth::id(), // Menggunakan ID user yang sedang login
            'judul_postingan' => $request->judul_postingan,
            'isi_postingan' => $request->isi_postingan,
            'status' => $request->status,
        ]);

        return back()->with('success_post', 'Postingan berhasil ditambahkan!');
    }

    public function deletePost($postinganId)
    {
        // Pastikan pengguna sudah login
        if (!Auth::check()) {
            return back()->withErrors(['delete_error' => 'Anda harus login untuk menghapus postingan.']);
        }

        // Temukan postingan berdasarkan ID
        $postingan = Postingan::find($postinganId);

        // Jika postingan tidak ditemukan
        if (!$postingan) {
            return back()->withErrors(['delete_error' => 'Postingan tidak ditemukan.']);
        }

        // Verifikasi bahwa user yang mencoba menghapus adalah pemilik postingan
        if ($postingan->user_id !== Auth::id()) {
            return back()->withErrors(['delete_error' => 'Anda tidak memiliki izin untuk menghapus postingan ini.']);
        }

        try {
            $postingan->delete();
            return back()->with('success_post', 'Postingan berhasil dihapus!');
        } catch (\Exception $e) {
            return back()->withErrors(['delete_error' => 'Gagal menghapus postingan: ' . $e->getMessage()]);
        }
    }
}
