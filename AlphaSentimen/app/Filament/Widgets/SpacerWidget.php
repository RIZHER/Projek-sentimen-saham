<?php

namespace App\Filament\Widgets;

use Filament\Widgets\Widget;

class SpacerWidget extends Widget
{
    // Tentukan file view untuk widget ini
    protected static string $view = 'filament.widgets.spacer-widget';

    // Hapus heading agar tidak ada judul yang ditampilkan
    protected static ?string $heading = null;

    // Atur urutan agar widget ini muncul paling awal
    protected static ?int $sort = 1;

    // Metode ini menentukan berapa banyak kolom grid yang akan diambil widget ini.
    // Nilai ini bisa disesuaikan. 'lg' => 2 berarti di layar besar akan mengambil 2 kolom.
    // 'full' di tabel profil saham akan mengambil seluruh baris setelah widget ini.
    public function getColumnSpan(): int | string | array
    {
        return ['md' => 1, 'lg' => 2]; // Sesuaikan nilai ini jika AccountWidget belum cukup ke kanan
    }
}
