{{-- resources/views/vendor/filament-panels/components/logo.blade.php --}}
@php
    $brandName = filament()->getBrandName();
    $brandLogo = filament()->getBrandLogo();

    // Deteksi apakah ini halaman login atau register Filament
    // Sesuaikan nama rute jika berbeda di aplikasi Anda (misal: 'filament.auth.login')
    $isLoginPage =
        request()->routeIs('filament.admin.auth.login') || request()->routeIs('filament.admin.auth.register');

    // Tentukan tinggi logo (gambar) berdasarkan halaman
    $logoHeight = $isLoginPage ? '4rem' : '2rem'; // 4rem untuk login/register, 2rem untuk navbar
    $logoStyles = "height: {$logoHeight};";

    // Tentukan kelas CSS untuk teks nama brand
    $brandNameTextClasses = \Illuminate\Support\Arr::toCssClasses([
        'fi-brand-name-text',
        'font-bold',
        'leading-5',
        'tracking-tight',
        'text-gray-950', // Warna teks default
        'dark:text-white', // Warna teks untuk dark mode
        'text-xl' => $isLoginPage, // Ukuran teks lebih besar untuk login/register
        'text-base' => !$isLoginPage, // Ukuran teks normal untuk navbar
        'mt-2' => $isLoginPage, // Margin atas jika teks di bawah logo pada halaman login
        'ms-2' => !$isLoginPage, // Margin kiri jika teks di samping logo pada navbar
    ]);

    // Tentukan kelas untuk container utama logo & teks (yang akan mengatur flex-direction)
    $containerFlexClasses = \Illuminate\Support\Arr::toCssClasses([
        'items-center', // Selalu tengah secara cross-axis
        'gap-2', // Selalu ada jarak antar elemen
        'flex-col' => $isLoginPage, // Tata letak kolom: logo di atas, teks di bawah
        'flex-row' => !$isLoginPage, // Tata letak baris: logo di samping, teks di samping
    ]);

    $darkModeBrandLogo = filament()->getDarkModeBrandLogo();
    $hasDarkModeBrandLogo = filled($darkModeBrandLogo);

    // Ini adalah kelas yang diterapkan pada DIV terluar yang membungkus logo dan teks
    // Kita perlu memastikan ini selalu flex agar kelas $containerFlexClasses bisa bekerja
    $getLogoVisibilityClasses = fn(bool $isDarkMode): string => \Illuminate\Support\Arr::toCssClasses([
        'fi-logo',
        'flex', // Pastikan div ini selalu display: flex
        'dark:hidden' => $hasDarkModeBrandLogo && !$isDarkMode,
        'hidden dark:flex' => $hasDarkModeBrandLogo && $isDarkMode,
        $containerFlexClasses, // Masukkan kelas flex-direction kondisional ke sini
    ]);
@endphp

@capture($content, $logo, $isDarkMode = false)
    {{-- Div terluar yang akan mendapatkan kelas visibility dan flex-direction --}}
    <div {{ $attributes->class([$getLogoVisibilityClasses($isDarkMode)]) }}>
        @if ($logo instanceof \Illuminate\Contracts\Support\Htmlable)
            {{-- Jika logo adalah HTML, kita perlu membungkusnya agar height bisa diterapkan --}}
            <div style="{{ $logoStyles }}">
                {{ $logo }}
            </div>
        @elseif (filled($logo))
            {{-- Jika logo adalah URL gambar --}}
            <img alt="{{ __('filament-panels::layout.logo.alt', ['name' => $brandName]) }}" src="{{ $logo }}"
                style="{{ $logoStyles }}" class="shrink-0" {{-- Mencegah gambar menyusut --}} />
        @endif

        {{-- Teks Nama Brand --}}
        <span class="{{ $brandNameTextClasses }}">
            {{ $brandName }}
        </span>
    </div>
@endcapture

{{ $content($brandLogo) }}

@if ($hasDarkModeBrandLogo)
    {{ $content($darkModeBrandLogo, isDarkMode: true) }}
@endif
