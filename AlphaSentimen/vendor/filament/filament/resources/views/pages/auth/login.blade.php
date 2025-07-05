<x-filament-panels::page.simple>
    {{-- Bagian @if (filament()->hasRegistration()) dihapus.
         Ini memastikan hanya link kustom Anda yang akan ditampilkan. --}}

    {{ \Filament\Support\Facades\FilamentView::renderHook(\Filament\View\PanelsRenderHook::AUTH_LOGIN_FORM_BEFORE, scopes: $this->getRenderHookScopes()) }}

    <x-filament-panels::form id="form" wire:submit="authenticate">
        {{ $this->form }}

        <x-filament-panels::form.actions
            :actions="$this->getCachedFormActions()"
            :full-width="$this->hasFullWidthFormActions()"
        />
    </x-filament-panels::form>

    {{-- Kode link Register kustom Anda tetap ada di sini --}}
    <div class="mt-4 text-center">
        Belum punya akun?
        <a href="{{ route('register') }}" class="text-primary-600 hover:underline">
            Register di sini
        </a>
    </div>

    {{ \Filament\Support\Facades\FilamentView::renderHook(\Filament\View\PanelsRenderHook::AUTH_LOGIN_FORM_AFTER, scopes: $this->getRenderHookScopes()) }}
</x-filament-panels::page.simple>