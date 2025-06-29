<?php

namespace App\Filament\Resources;

use App\Filament\Resources\NewsResource\Pages;
use App\Models\Berita; // Impor model Berita Anda
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Tables\Columns\TextColumn; // Impor TextColumn untuk tabel
use Filament\Forms\Components\TextInput; // Impor TextInput (meskipun form kosong)
use Filament\Forms\Components\MarkdownEditor; // Impor MarkdownEditor (untuk infolist)
use Filament\Forms\Components\Select; // Impor Select
use Filament\Forms\Components\Group; // Impor Group
use Filament\Infolists\Components\TextEntry; // Impor TextEntry untuk detail page
use Filament\Infolists\Components\Grid; // Impor Grid untuk tata letak detail page
use Filament\Infolists\Infolist; // Impor Infolist
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;


class NewsResource extends Resource
{
    protected static ?string $model = Berita::class; // Kaitkan dengan model Berita

    protected static ?string $navigationIcon = 'heroicon-o-newspaper'; // Ikon untuk navigasi sidebar
    // Perbaikan: Mengubah label navigasi dari 'Beritas' menjadi 'Berita'
    protected static ?string $navigationLabel = 'Berita'; // Label navigasi sidebar
    protected static ?string $modelLabel = 'Berita'; // Label singular model

    // Metode ini mendefinisikan struktur form untuk membuat dan mengedit berita.
    // Dibiarkan kosong karena kita menghilangkan Create/Edit.
    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                // Form ini kosong karena tidak ada operasi Create/Edit
            ]);
    }

    // Metode ini mendefinisikan struktur tabel untuk menampilkan daftar berita
    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                // Kolom untuk Judul Berita
                TextColumn::make('judul_berita')
                    ->searchable() // Mengizinkan pencarian
                    ->sortable() // Mengizinkan pengurutan
                    ->wrap() // Membungkus teks jika terlalu panjang
                    ->label('Judul Berita'),

                // Kolom untuk Sentimen Berita
                TextColumn::make('sentimen')
                    ->searchable()
                    ->sortable()
                    ->badge() // Menampilkan sebagai badge dengan warna berbeda
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
            ->filters([
                // Filter berdasarkan Saham
                Tables\Filters\SelectFilter::make('saham_id')
                    ->relationship('sahamProfile', 'nama_saham')
                    ->label('Filter Berdasarkan Saham'),

                // Filter berdasarkan Sentimen
                Tables\Filters\SelectFilter::make('sentimen')
                    ->options([
                        'Positif' => 'Positif',
                        'Netral' => 'Netral',
                        'Negatif' => 'Negatif',
                    ])
                    ->query(function (Builder $query, array $data): Builder {
                        // Ambil nilai yang dipilih dari filter
                        $selectedOption = $data['value'] ?? null;

                        // Jika tidak ada opsi yang dipilih, jangan lakukan filter
                        if (!$selectedOption) {
                            return $query;
                        }

                        // Petakan opsi yang dipilih ke semua kemungkinan nilai di database
                        $sentimenValues = match ($selectedOption) {
                            'Positif' => ['Positif', 'positif', 'positive', 'POSITIVE'],
                            'Netral' => ['Netral', 'netral', 'neutral'],
                            'Negatif' => ['Negatif', 'negatif', 'negative', 'NEGATIVE'],
                            default => [], // Jika tidak ada yang cocok, kembalikan array kosong
                        };

                        // Lakukan filter menggunakan `whereIn` untuk mencocokkan salah satu nilai di array
                        return $query->whereIn('sentimen', $sentimenValues);
                    })
                    ->label('Filter Berdasarkan Sentimen'),
            ])
            ->actions([
                // Hanya izinkan ViewAction
                Tables\Actions\ViewAction::make(),
            ])
            ->bulkActions([
                // Aksi massal dihilangkan
            ]);
    }

    // Metode ini mendefinisikan tampilan detail berita (read-only)
    public static function infolist(Infolist $infolist): Infolist
    {
        return $infolist
            ->schema([
                Grid::make(2) // Tata letak dalam 2 kolom
                    ->schema([
                        // Menampilkan Judul Berita
                        TextEntry::make('judul_berita')
                            ->columnSpan('full') // Ambil lebar penuh
                            ->label('Judul Berita'),

                        // Menampilkan Link Asli (URL)
                        TextEntry::make('url')
                            ->url(fn(Berita $record): string => $record->url) // Membuat URL bisa diklik
                            ->openUrlInNewTab() // Membuka di tab baru
                            ->label('Link Asli'),

                        // Menampilkan Sentimen
                        TextEntry::make('sentimen')
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

                        // Menampilkan Nama Saham terkait
                        TextEntry::make('sahamProfile.nama_saham')
                            ->label('Nama Saham'),

                        // Menampilkan Isi Berita
                        TextEntry::make('isi_berita')
                            ->markdown() // Render sebagai Markdown jika isi berita dalam format Markdown
                            ->columnSpan('full')
                            ->label('Isi Berita'),
                    ]),
            ]);
    }

    // Metode ini mendefinisikan halaman-halaman yang terkait dengan Resource ini
    public static function getPages(): array
    {
        return [
            'index' => Pages\ListNews::route('/'), // Halaman daftar berita
            // 'view' => Pages\ViewNews::route('/{record}'), // Halaman detail berita
            // Baris berikut dihapus untuk menghilangkan tombol "New Berita" dan akses ke halaman Create/Edit
            // 'create' => Pages\CreateNews::route('/create'),
            // 'edit' => Pages\EditNews::route('/{record}/edit'),
        ];
    }

    // Metode ini mendefinisikan Relation Managers (jika ada relasi kompleks lainnya)
    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    // --- BARIS TAMBAHAN UNTUK MENGHILANGKAN TOMBOL "NEW BERITA" ---
    public static function canCreate(): bool
    {
        return false; // Mengembalikan false untuk mencegah pembuatan data baru
    }
}
