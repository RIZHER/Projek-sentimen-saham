<?php

// database/migrations/xxxx_xx_xx_xxxxxx_create_saham_profiles_table.php

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
        Schema::create('saham_profile', function (Blueprint $table) {
            // Kolom Primary Key (PK)
            $table->id('saham_id'); // Otomatis menjadi unsignedBigInteger dan primary key

            // Kolom Lainnya
            $table->string('kode_saham')->unique(); // Misal: BBCA, TLKM
            $table->string('nama_saham'); // Misal: Bank Central Asia Tbk.
            $table->string('sentimen')->nullable(); // Misal: "Positif", "Negatif", "Netral"
            
            $table->timestamps(); // created_at dan updated_at
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('saham_profile');
    }
};