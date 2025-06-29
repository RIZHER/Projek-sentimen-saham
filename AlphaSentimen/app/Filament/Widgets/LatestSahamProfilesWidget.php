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
                    ->label('Nama Perusahaan'),

                TextColumn::make('sentimen')
                    ->searchable()
                    ->sortable()
                    ->badge()
                    ->color(fn(string $state): string => match ($state) {
                        'Positif' => 'success',
                        'Netral' => 'warning',
                        'Negatif' => 'danger',
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
