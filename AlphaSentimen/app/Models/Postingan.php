<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Builder;

class Postingan extends Model
{
    use HasFactory;

    // --- BARIS PENTING INI UNTUK MENENTUKAN NAMA TABEL SECARA EKSPLISIT ---
    protected $table = 'postingan'; 

    // Tentukan primary key jika bukan 'id' (sesuai skema Anda)
    protected $primaryKey = 'postingan_id'; 

    // Kolom-kolom yang dapat diisi secara massal (mass assignable)
    protected $fillable = [
        'saham_id',
        'user_id',
        'judul_postingan',
        'isi_postingan',
        'status', // 'public' atau 'private'
    ];

    /**
     * Definisikan relasi dengan model SahamProfile.
     */
    public function sahamProfile(): BelongsTo
    {
        return $this->belongsTo(SahamProfile::class, 'saham_id', 'saham_id');
    }

    /**
     * Definisikan relasi dengan model User.
     * Pastikan User::class di-import di bagian atas file jika belum.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id', 'id');
    }
}
