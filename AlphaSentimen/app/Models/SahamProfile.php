<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class SahamProfile extends Model
{
    use HasFactory;

    // *** BARIS PENTING INI UNTUK MENENTUKAN NAMA TABEL SECARA EKSPLISIT ***
    protected $table = 'saham_profile'; 

    // *** BARIS PENTING INI UNTUK MENENTUKAN PRIMARY KEY JIKA BUKAN 'id' ***
    protected $primaryKey = 'saham_id'; 

    // Kolom yang bisa diisi secara massal
    protected $fillable = [
        'kode_saham',
        'nama_saham',
        'sentimen', // Pastikan 'sentimen' ada di fillable karena sudah ada di tabel
    ];

    // Jika Anda ingin menonaktifkan timestamps (created_at, updated_at) bisa set false
    // public $timestamps = true; // Defaultnya sudah true, jadi tidak perlu didefinisikan jika Anda ingin menggunakannya
}