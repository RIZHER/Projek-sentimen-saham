<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Berita extends Model
{
    use HasFactory;
    protected $table = 'berita';
    protected $primaryKey = 'berita_id';
    protected $fillable = [
        'saham_id',
        'url',
        'judul_berita',
        'isi_berita',
        'sentimen',
    ];
    public function sahamProfile(): BelongsTo
    {
        return $this->belongsTo(SahamProfile::class, 'saham_id', 'saham_id');
    }
}
