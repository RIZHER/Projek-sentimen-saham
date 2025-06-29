<?php

namespace App\Filament\Widgets;

use App\Models\SahamProfile;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;
use Filament\Widgets\TableWidget as BaseWidget;
use Filament\Support\Enums\Alignment;

class LatestSahamProfilesWidget extends BaseWidget
{
    protected static ?string $heading = 'Data Profil Saham';
    protected static ?int $perPage = 10;

    public function table(Table $table): Table
    {
        return $table
            ->query(
                SahamProfile::query()
            )
            ->columns([
                TextColumn::make('kode_saham')
                    ->searchable()
                    ->sortable()
                    ->label('Kode Saham'),

                TextColumn::make('nama_saham')
                    ->searchable()
                    ->sortable()
                    ->label('Nama Perusahaan')
                    // Menggunakan helper route() untuk membuat link ke halaman berita publik
                    ->url(fn(SahamProfile $record): string => route('public.news.list', ['saham_id' => $record->saham_id])),

                TextColumn::make('sentimen')
                    ->searchable()
                    ->sortable()
                    ->badge()
                    ->color(fn(string $state): string => match (strtolower(trim($state))) {
                        // Tambahkan 'positive' di sini
                        'positif', 'positive' => 'success',
                        // Tambahkan 'neutral' di sini
                        'netral', 'neutral' => 'warning',
                        // Tambahkan 'negatif', 'negative' di sini
                        'negatif', 'negative' => 'danger',
                        default => 'gray',
                    })
                    ->label('Sentimen'),
            ])
            ->paginated();
    }

    // Mengontrol lebar kolom widget.
    // Perbaikan: Menghapus keyword 'static' dari deklarasi metode
    // agar kompatibel dengan metode non-static di kelas induk Filament\Widgets\Widget.
    public function getColumnSpan(): int | string | array
    {
        return 'full'; // Mengatur lebar widget menjadi penuh
    }
}
