<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Berita; // Import model Berita Anda
use App\Models\SahamProfile; // Import model SahamProfile Anda
use Illuminate\Support\Str; // Import Str untuk markdown (jika digunakan di view)

class PublicController extends Controller
{
    public function listNews(Request $request)
    {
        // Pastikan saham_id ada di request dan ambil nilainya
        $sahamId = $request->input('saham_id');

        // Temukan profil saham berdasarkan ID
        $saham = SahamProfile::find($sahamId);

        // Jika saham tidak ditemukan (sahamId tidak valid), tampilkan 404
        if (!$saham) {
            abort(404, 'Saham tidak ditemukan.');
        }

        // Ambil berita terkait saham ini
        // Urutkan dari yang terbaru dan tambahkan paginasi
        $beritas = Berita::where('saham_id', $sahamId)
            ->orderBy('created_at', 'desc')
            ->paginate(10);

        // --- Perbaikan: Tambahkan appends(request()->query()) untuk paginasi ---
        // Ini akan memastikan semua parameter query yang ada (termasuk saham_id)
        // diteruskan ke tautan paginasi halaman berikutnya.
        $beritas->appends(request()->query());

        // Tentukan heading yang sesuai dengan saham yang ditemukan
        $heading = 'Berita Saham: ' . $saham->nama_saham . ' (' . $saham->kode_saham . ')';

        // Kembalikan view dengan data berita, heading, dan profil saham
        return view('public.news-list', compact('beritas', 'heading', 'saham'));
    }
}
