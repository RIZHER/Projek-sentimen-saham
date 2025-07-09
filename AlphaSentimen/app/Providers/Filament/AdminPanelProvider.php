<?php

namespace App\Providers\Filament;

use Filament\Http\Middleware\Authenticate;
use Filament\Http\Middleware\DisableBladeIconComponents;
use Filament\Http\Middleware\DispatchServingFilamentEvent;
use Filament\Pages;
use Filament\Panel;
use Filament\PanelProvider;
use Filament\Support\Colors\Color;
use Filament\Widgets;
use App\Filament\Widgets\LatestSahamProfilesWidget; // Import widget tabel Anda
use App\Filament\Widgets\SpacerWidget; // Import widget spacer yang baru
use Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse;
use Illuminate\Cookie\Middleware\EncryptCookies;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;
use Illuminate\Routing\Middleware\SubstituteBindings;
use Illuminate\Session\Middleware\AuthenticateSession;
use Illuminate\Session\Middleware\StartSession;
use Illuminate\View\Middleware\ShareErrorsFromSession;
use Filament\Navigation\NavigationItem;
use Filament\Pages\Dashboard;

class AdminPanelProvider extends PanelProvider
{
    public function panel(Panel $panel): Panel
    {
        return $panel
            ->navigationItems([
                NavigationItem::make('User Prfile')
                    ->url(fn(): string => Dashboard::getUrl())
                    ->icon('heroicon-o-cog-6-tooth')
                    ->group('Settings')
                    ->sort(3),
            ])

            ->brandLogo(asset('images/logo-cakra-io.svg'))
            ->darkModeBrandLogo(asset('images/logo-cakra-io-dark.svg'))
            ->brandName('Cakra Finance')
            ->brandLogoHeight('8rem')
            

            ->default()
            ->id('admin')
            ->path('admin')
            ->login()
            ->registration() // <--- PASTIKAN BARIS INI ADA DAN TIDAK DIKOMENTARI
            ->colors([
                'primary' => Color::Amber,
            ])
            ->discoverResources(in: app_path('Filament/Resources'), for: 'App\\Filament\\Resources')
            ->discoverPages(in: app_path('Filament/Pages'), for: 'App\\Filament\\Pages')
            ->pages([
                Pages\Dashboard::class,
            ])
            ->discoverWidgets(in: app_path('Filament/Widgets'), for: 'App\\Filament\\Widgets')
            ->widgets([

                // AccountWidget akan muncul setelah SpacerWidget, di kanan atas
                Widgets\FilamentInfoWidget::class,
                Widgets\AccountWidget::class,

                // Widget tabel Anda akan mengambil seluruh lebar di baris baru.
                // Pastikan getColumnSpan() di LatestSahamProfilesWidget mengembalikan 'full' atau int 12.
                LatestSahamProfilesWidget::class,
            ])
            ->middleware([
                EncryptCookies::class,
                AddQueuedCookiesToResponse::class,
                StartSession::class,
                AuthenticateSession::class,
                ShareErrorsFromSession::class,
                VerifyCsrfToken::class,
                SubstituteBindings::class,
                DisableBladeIconComponents::class,
                DispatchServingFilamentEvent::class,
            ])
            ->authMiddleware([
                Authenticate::class,
            ]);
    }
}
