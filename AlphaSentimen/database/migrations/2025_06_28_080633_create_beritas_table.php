<?php

// database/migrations/xxxx_xx_xx_xxxxxx_create_beritas_table.php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('berita', function (Blueprint $table) {
            // Kolom Primary Key (PK)
            $table->id('berita_id');

            // Kolom Foreign Key (FK)
            // Menghubungkan ke tabel saham_profile
            $table->foreignId('saham_id')
                  ->constrained('saham_profile', 'saham_id')
                  ->onDelete('cascade'); // Jika saham dihapus, berita juga ikut terhapus

            // Kolom Lainnya
            $table->string('url')->unique();
            $table->string('judul_berita');
            $table->longText('isi_berita'); // Menggunakan longText untuk teks panjang
            $table->string('sentimen')->nullable(); // Misal: "Positif", "Negatif", "Netral"
            
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('berita');
    }
};