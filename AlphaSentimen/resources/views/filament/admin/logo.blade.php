{{-- resources/views/filament/admin/logo.blade.php --}}

@php
    $isAuthPage = request()->routeIs('filament.auth.*');

    $logoHeightAuth = 'h-24'; // 6rem
    $logoHeightNavbar = 'h-8';  // 2rem

    $textSizeAuth = 'text-2xl';
    $textSizeNavbar = 'text-xl';
@endphp

@if ($isAuthPage)
    {{-- Halaman Login/Register (logo di atas, teks di bawah) --}}
    <div id="auth-logo-container"> {{-- Tambahkan ID untuk target CSS spesifik --}}
        <img
            src="{{ asset('images/logo-cakra-io-dark.svg') }}"
            alt="Cakra Finance Logo"
            class="{{ $logoHeightAuth }}" {{-- Hapus flex/block/mx-auto di sini --}}
            style="object-fit: contain;"
        />
        <span
            class="font-bold text-center {{ $textSizeAuth }} text-gray-950 dark:text-white" {{-- Hapus block --}}
        >
            Cakra Finance
        </span>
    </div>
@else
    {{-- Navbar (logo di kiri, teks di kanan) --}}
    <div id="navbar-logo-container"> {{-- Tambahkan ID untuk target CSS spesifik --}}
        <img
            src="{{ asset('images/logo-cakra-io-dark.svg') }}"
            alt="Cakra Finance Logo"
            class="{{ $logoHeightNavbar }}"
            style="object-fit: contain;"
        />
        <span class="font-semibold {{ $textSizeNavbar }} text-gray-950 dark:text-white whitespace-nowrap">
            Cakra Finance
        </span>
    </div>
@endif