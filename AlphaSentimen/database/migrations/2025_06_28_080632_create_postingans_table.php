<?php

// database/migrations/xxxx_xx_xx_xxxxxx_create_postingans_table.php

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
        Schema::create('postingan', function (Blueprint $table) {
            // Kolom Primary Key (PK)
            $table->id('postingan_id');

            // Kolom Foreign Keys (FK)
            // Menghubungkan ke tabel saham_profile
            $table->foreignId('saham_id')
                  ->constrained('saham_profile', 'saham_id')
                  ->onDelete('cascade'); // Jika saham dihapus, postingan ikut terhapus
            
            // Menghubungkan ke tabel users (pastikan tabel users sudah ada dan PK-nya 'id')
            $table->foreignId('user_id')
                  ->constrained('users') // Jika tidak menyebut kolom, defaultnya 'id'
                  ->onDelete('cascade'); // Jika user dihapus, postingannya ikut terhapus

            // Kolom Lainnya
            $table->string('judul_postingan');
            $table->longText('isi_postingan');
            $table->string('status')->default('public'); // Misal: "active", "inactive"
            
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('postingan');
    }
};