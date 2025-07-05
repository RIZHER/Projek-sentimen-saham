<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $heading }}</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Gaya dasar untuk mode terang */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
            /* Warna abu-abu muda */
            color: #1f2937;
            /* Default warna teks gelap untuk body */
        }

        .container {
            max-width: 960px;
            /* Lebar maksimal konten */
            margin-left: auto;
            margin-right: auto;
        }

        .card {
            background-color: #ffffff;
            border-radius: 0.5rem;
            /* Rounded corners */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .table-header {
            background-color: #e2e8f0;
            /* Warna header tabel */
        }

        .table-row:nth-child(even) {
            background-color: #f8fafc;
            /* Warna baris genap */
        }

        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            /* Full rounded */
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-flex;
            /* Agar bisa pakai align-items */
            align-items: center;
            /* Vertically align text */
            justify-content: center;
            /* Horizontally align text */
        }

        .badge-success {
            background-color: #d1fae5;
            color: #065f46;
        }

        .badge-warning {
            background-color: #fef3c7;
            color: #92400e;
        }

        .badge-danger {
            background-color: #fee2e2;
            color: #991b1b;
        }

        .badge-gray {
            background-color: #e5e7eb;
            color: #4b5563;
        }

        /* Modal Styling */
        .modal {
            display: none;
            /* Hidden by default */
            position: fixed;
            /* Stay in place */
            z-index: 1000;
            /* Sit on top */
            left: 0;
            top: 0;
            width: 100%;
            /* Full width */
            height: 100%;
            /* Full height */
            overflow: auto;
            /* Enable scroll if needed */
            background-color: rgba(0, 0, 0, 0.4);
            /* Black w/ opacity */
            backdrop-filter: blur(5px);
            /* Efek blur pada background */
            -webkit-backdrop-filter: blur(5px);
            /* For Safari */
            justify-content: center;
            /* Centering for flexbox */
            align-items: center;
            /* Centering for flexbox */
        }

        .modal-content {
            background-color: #fefefe;
            padding: 20px;
            border: 1px solid #888;
            width: min(calc(100vw - 40px), 800px);
            /* Adaptif lebar modal */
            border-radius: 0.75rem;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
            position: relative;
            animation: fadeIn 0.3s;
            max-height: 90vh;
            /* Tinggi maksimal modal */
            display: flex;
            flex-direction: column;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .close-button {
            color: #aaa;
            align-self: flex-end;
            /* Pindahkan tombol ke kanan atas */
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }

        .close-button:hover,
        .close-button:focus {
            color: black;
            text-decoration: none;
        }

        .prose {
            max-width: none;
            /* Override default prose max-width */
            overflow-y: auto;
            /* Scrollable content for long text */
            flex-grow: 1;
            /* Ambil sisa ruang */
            padding-right: 10px;
            /* Ruang untuk scrollbar */
        }

        .prose img {
            max-width: 100%;
            height: auto;
            border-radius: 0.5rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        .prose h1,
        .prose h2,
        .prose h3,
        .prose h4,
        .prose h5,
        .prose h6 {
            font-weight: bold;
            /* Ensure headings are bold */
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }

        /* --- Gaya untuk Dark Mode --- */
        html.dark body {
            background-color: #111827;
            /* Darker background */
            color: #d1d5db;
            /* Light text */
        }

        html.dark .card {
            background-color: #1f2937;
            /* Darker card background */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        html.dark .table-header {
            background-color: #374151;
            color: #f9fafb;
            /* Text color for dark header */
        }

        html.dark .table-row {
            color: #d1d5db;
            /* Default text color for table rows */
        }

        html.dark .table-row:nth-child(even) {
            background-color: #1f2937;
        }

        html.dark .table-row:nth-child(odd) {
            /* Added for odd rows in dark mode */
            background-color: #111827;
        }

        html.dark .table-row.hover\:bg-gray-50:hover {
            /* Hover state for dark mode rows */
            background-color: #374151;
        }

        html.dark .divide-y.divide-gray-200>*:not([hidden])~*:not([hidden]) {
            /* Table dividers */
            border-color: #374151;
            /* Darker border for table dividers */
        }

        /* --- Perbaikan Warna Teks untuk Mode Terang (Default) dan Mode Gelap --- */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            /* Target semua heading */
            color: #1f2937;
            /* Default warna gelap untuk mode terang */
        }

        html.dark h1,
        html.dark h2,
        html.dark h3,
        html.dark .text-gray-800 {
            color: #f9fafb;
            /* Warna terang untuk dark mode */
        }

        /* Teks abu-abu lainnya yang mungkin tidak terlihat */
        .text-gray-600 {
            /* Contoh: p.text-gray-600 */
            color: #4b5563;
            /* Default warna gelap */
        }

        html.dark .text-gray-600 {
            color: #d1d5db;
            /* Warna terang di dark mode */
        }

        .text-gray-700 {
            /* Contoh: label form, prose content */
            color: #374151;
            /* Default warna gelap */
        }

        html.dark .text-gray-700 {
            color: #d1d5db;
            /* Warna terang di dark mode */
        }

        .text-gray-900 {
            /* Default warna hitam untuk mode terang */
            color: #000000;
        }

        html.dark .text-gray-900 {
            color: #f9fafb;
            /* Warna terang untuk dark mode */
        }

        .text-gray-500 {
            /* Default warna abu-abu untuk mode terang */
            color: #6b7280;
        }

        html.dark .text-gray-500 {
            color: #9ca3af;
            /* Warna terang di dark mode */
        }

        /* Styling untuk form input di Light Mode (lebih netral, border saja) */
        .form-input,
        .form-textarea,
        .form-select {
            display: block;
            width: 100%;
            padding: 0.625rem 0.75rem;
            font-size: 1rem;
            line-height: 1.5;
            border-width: 1px;
            border-color: #d1d5db;
            /* Lebih netral: border-gray-300 */
            border-radius: 0.375rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            background-color: #ffffff;
            /* Latar belakang tetap putih */
            color: #1f2937;
            /* Warna teks hitam/gelap */
            transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }

        .form-input:focus,
        .form-textarea:focus,
        .form-select:focus {
            outline: none;
            border-color: #4f46e5;
            /* border-indigo-500 */
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.5);
            /* ring-indigo-200 / ring-indigo-500 */
        }

        .form-input::placeholder,
        .form-textarea::placeholder {
            color: #6b7280;
            /* placeholder color gray-500 */
        }

        .form-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            color: #1f2937;
            /* Default hitam/gelap untuk label */
            margin-bottom: 0.5rem;
        }

        /* Styling untuk form input di Dark Mode */
        html.dark .form-input,
        html.dark .form-textarea,
        html.dark .form-select {
            background-color: #374151;
            /* bg-gray-700 */
            border-color: #4b5563;
            /* border-gray-600 */
            color: #f9fafb;
            /* text-white */
        }

        html.dark .form-input::placeholder,
        html.dark .form-textarea::placeholder {
            color: #9ca3af;
            /* placeholder color gray-400 */
        }

        html.dark .form-input:focus,
        html.dark .form-textarea:focus,
        html.dark .form-select:focus {
            border-color: #60a5fa;
            /* border-blue-400/500 */
            box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.5);
            /* ring-blue-500 */
        }

        html.dark .form-label {
            color: #d1d5db;
            /* text-gray-300 */
        }

        /* --- Styling untuk Tombol Hapus Postingan --- */
        .delete-button {
            display: inline-flex;
            align-items: center;
            /* Perubahan: Ukuran normal */
            padding: 0.5rem 1rem;
            /* px-4 py-2 */
            font-size: 0.875rem;
            /* text-sm */
            font-weight: 600;
            /* Medium bold */
            color: #ffffff;
            /* Warna teks putih */
            background-color: #dc2626;
            /* bg-red-600 */
            border: none;
            border-radius: 0.375rem;
            /* rounded-md */
            cursor: pointer;
            transition: background-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }

        .delete-button:hover {
            background-color: #b91c1c;
            /* hover:bg-red-700 */
        }

        .delete-button:focus {
            outline: none;
            box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.5);
            /* focus:ring-red-500 */
        }

        /* Dark Mode untuk Tombol Hapus */
        html.dark .delete-button {
            background-color: #ef4444;
            /* bg-red-500 */
            color: #ffffff;
        }

        html.dark .delete-button:hover {
            background-color: #dc2626;
            /* hover:bg-red-600 */
        }

        html.dark .delete-button:focus {
            box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.5);
        }
    </style>
    <script>
        // Script untuk mendeteksi dan menerapkan tema dari Filament
        function applyTheme() {
            const htmlElement = document.documentElement;
            let theme = localStorage.getItem('theme') || 'system'; // Default ke 'system' jika tidak ada

            if (theme === 'system') {
                // Deteksi preferensi sistem
                if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    htmlElement.classList.add('dark');
                } else {
                    htmlElement.classList.remove('dark');
                }
            } else if (theme === 'dark') {
                htmlElement.classList.add('dark');
            } else { // theme === 'light'
                htmlElement.classList.remove('dark');
            }
        }

        // Jalankan saat halaman dimuat
        applyTheme();

        // Tambahkan event listener untuk perubahan tema di local storage
        // Ini memastikan halaman publik berubah jika tema di admin panel diubah di tab lain
        window.addEventListener('storage', (event) => {
            if (event.key === 'theme') {
                applyTheme();
            }
        });

        // Tambahkan event listener untuk perubahan preferensi sistem (jika tema 'system')
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (event) => {
            if (localStorage.getItem('theme') === 'system') {
                applyTheme();
            }
        });
    </script>
</head>

<body class="p-6">
    <div class="container">
        <a href="{{ url('/admin') }}" class="text-blue-600 hover:underline mb-6 inline-block">← Kembali ke Dashboard
            Admin</a>

        <h1 class="text-3xl font-bold text-gray-800 mb-6">{{ $heading }}</h1>
        @if ($saham)
            <p class="text-lg text-gray-600 mb-8">Sentimen Global Saham: <span
                    class="px-2 py-1 rounded-full text-sm font-medium 
                @if (strtolower(trim($saham->sentimen)) == 'positif' || strtolower(trim($saham->sentimen)) == 'positive') bg-green-100 text-green-800
                @elseif(strtolower(trim($saham->sentimen)) == 'netral' || strtolower(trim($saham->sentimen)) == 'neutral') bg-yellow-100 text-yellow-800
                @elseif(strtolower(trim($saham->sentimen)) == 'negatif' || strtolower(trim($saham->sentimen)) == 'negative') bg-red-100 text-red-800
                @else badge-gray @endif">
                    {{ $saham->sentimen }}
                </span></p>
        @endif

        <div class="card p-0 overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="table-header">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Judul
                            Berita</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
                            Sentimen</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Aksi
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    @forelse ($beritas as $berita)
                        <tr class="table-row hover:bg-gray-50 cursor-pointer" onclick="showNewsDetail(this)"
                            data-judul="{{ $berita->judul_berita }}" data-url="{{ $berita->url }}"
                            data-isi="{{ base64_encode(Str::markdown($berita->isi_berita)) }}" {{-- Encode Markdown to base64 --}}
                            data-sentimen="{{ $berita->sentimen }}"
                            data-saham="{{ $berita->sahamProfile->nama_saham ?? 'N/A' }}">
                            <td class="px-6 py-4 whitespace-normal text-sm font-medium text-gray-900">
                                {{ $berita->judul_berita }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    class="badge 
                                    @if (strtolower(trim($berita->sentimen)) == 'positif' || strtolower(trim($berita->sentimen)) == 'positive') badge-success
                                    @elseif(strtolower(trim($berita->sentimen)) == 'netral' || strtolower(trim($berita->sentimen)) == 'neutral') badge-warning
                                    @elseif(strtolower(trim($berita->sentimen)) == 'negatif' || strtolower(trim($berita->sentimen)) == 'negative') badge-danger
                                    @else badge-gray @endif">
                                    {{ $berita->sentimen }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                <button class="text-blue-600 hover:text-blue-900 font-semibold focus:outline-none">Lihat
                                    Detail</button>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500">Belum ada berita yang
                                tersedia.</td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>

        <!-- Paginasi -->
        <div class="mt-8">
            {{ $beritas->links('pagination::tailwind') }}
        </div>

        {{-- Bagian Kolom Komentar/Tweet --}}
        <div class="card mt-8">
            {{-- Perbaikan: Pastikan heading terlihat di light mode --}}
            <h2 class="text-2xl font-bold mb-4 text-gray-900">Buat Postingan Baru</h2>

            @if ($errors->any())
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4 dark:bg-red-900 dark:border-red-700 dark:text-red-300"
                    role="alert">
                    <strong class="font-bold">Oops!</strong>
                    <span class="block sm:inline">Ada masalah dengan input Anda.</span>
                    <ul class="mt-3 list-disc list-inside text-sm">
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif

            @if (session('success_post'))
                <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4 dark:bg-green-900 dark:border-green-700 dark:text-green-300"
                    role="alert">
                    <strong class="font-bold">Sukses!</strong>
                    <span class="block sm:inline">{{ session('success_post') }}</span>
                </div>
            @endif

            @if ($isAuthenticated)
                <form action="{{ route('public.post.store') }}" method="POST">
                    @csrf
                    <input type="hidden" name="saham_id" value="{{ $saham->saham_id }}">

                    <div class="mb-4">
                        <label for="judul_postingan" class="form-label">Judul Postingan</label>
                        <input type="text" name="judul_postingan" id="judul_postingan" class="form-input"
                            value="{{ old('judul_postingan') }}" required>
                    </div>

                    <div class="mb-4">
                        <label for="isi_postingan" class="form-label">Isi Postingan (Mendukung Markdown)</label>
                        <textarea name="isi_postingan" id="isi_postingan" rows="5" class="form-textarea" required>{{ old('isi_postingan') }}</textarea>
                    </div>

                    <div class="mb-4">
                        <label for="status" class="form-label">Visibilitas</label>
                        <select name="status" id="status" class="form-select" required>
                            <option value="public" {{ old('status') == 'public' ? 'selected' : '' }}>Publik (Dapat
                                Dilihat Semua Orang)</option>
                            <option value="private" {{ old('status') == 'private' ? 'selected' : '' }}>Privat (Hanya
                                Saya yang Melihat)</option>
                        </select>
                    </div>

                    <button type="submit"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        Kirim Postingan
                    </button>
                </form>
            @else
                <div class="text-center py-4 text-gray-600 dark:text-gray-400">
                    Silakan <a href="{{ url('/admin/login') }}" class="text-blue-600 hover:underline">login</a> untuk
                    membuat postingan.
                </div>
            @endif
        </div>

        <div class="card mt-8">
            {{-- Perbaikan: Pastikan heading terlihat di light mode --}}
            <h2 class="text-2xl font-bold mb-4 text-gray-900">Postingan Komunitas</h2>
            @forelse ($postingans as $post)
                <div
                    class="border-b border-gray-200 dark:border-gray-700 pb-4 mb-4 last:border-b-0 last:pb-0 last:mb-0">
                    {{-- Perbaikan: Judul Postingan di daftar --}}
                    <h3 class="text-xl font-semibold text-gray-900 mb-1">{{ $post->judul_postingan }}</h3>
                    <p class="text-gray-700 text-sm mb-2">
                        Diposting oleh: <span
                            class="font-medium">{{ $post->user->name ?? 'Pengguna Tidak Dikenal' }}</span> pada
                        {{ $post->created_at->format('d F Y, H:i') }}
                        <span
                            class="ml-2 px-2 py-1 rounded-full text-xs font-medium 
                            @if ($post->status == 'public') bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300
                            @else bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 @endif">
                            {{ $post->status == 'public' ? 'Publik' : 'Privat' }}
                        </span>
                    </p>
                    {{-- Konten isi postingan --}}
                    <div class="prose max-w-none text-gray-800 leading-relaxed">
                        {!! Str::markdown($post->isi_postingan) !!}
                    </div>
                    {{-- Tombol Hapus dipindahkan ke sini, di bawah konten postingan, di kiri --}}
                    @if ($isAuthenticated && $currentUserId == $post->user_id)
                        <div class="mt-4 text-left"> {{-- Tombol hapus rata kiri --}}
                            <form action="{{ route('public.post.delete', $post->postingan_id) }}" method="POST"
                                class="inline-block"
                                onsubmit="return confirm('Apakah Anda yakin ingin menghapus postingan ini?');">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="delete-button">Hapus</button>
                            </form>
                        </div>
                    @endif
                </div>
            @empty
                <p class="text-center text-gray-500">Belum ada postingan untuk saham ini.</p>
            @endforelse
        </div>
    </div>

    <!-- The Modal (News Detail Pop-up) -->
    <div id="newsDetailModal" class="modal">
        <!-- Modal content -->
        <div class="modal-content">
            <span class="close-button" onclick="closeNewsDetail()">&times;</span>
            <h2 id="modal-judul" class="text-2xl font-bold mb-2"></h2>
            <p class="text-gray-500 text-sm mb-3">
                Saham: <span id="modal-saham"></span> | Sentimen:
                <span id="modal-sentimen" class="badge"></span>
            </p>
            <p class="text-blue-600 hover:underline mb-4">
                <a id="modal-url" href="#" target="_blank" rel="noopener noreferrer"
                    class="font-semibold flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 6H6a2 2 0 00-2 2v10a2 0 002 2h10a2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                    </svg>
                    Baca Artikel Asli
                </a>
            </p>
            <div id="modal-isi" class="prose max-w-none text-gray-700 leading-relaxed">
                <!-- Isi berita akan dimuat di sini -->
            </div>
        </div>
    </div>

    <script>
        const newsDetailModal = document.getElementById('newsDetailModal');
        const modalJudul = document.getElementById('modal-judul');
        const modalSaham = document.getElementById('modal-saham');
        const modalSentimen = document.getElementById('modal-sentimen');
        const modalUrl = document.getElementById('modal-url');
        const modalIsi = document.getElementById('modal-isi');

        function showNewsDetail(row) {
            modalJudul.textContent = row.dataset.judul;
            modalSaham.textContent = row.dataset.saham;
            modalUrl.href = row.dataset.url;

            // Perbarui sentimen badge
            modalSentimen.textContent = row.dataset.sentimen;
            modalSentimen.className = 'badge ' + getBadgeClass(row.dataset.sentimen);

            // Decode base64 dan set innerHTML
            try {
                modalIsi.innerHTML = decodeURIComponent(escape(atob(row.dataset.isi)));
            } catch (e) {
                console.error("Error decoding base64:", e);
                modalIsi.textContent = "Error loading content.";
            }

            newsDetailModal.style.display = 'flex'; // Use flex to center
        }

        function closeNewsDetail() {
            newsDetailModal.style.display = 'none';
        }

        // Close the modal when clicking outside of it
        window.onclick = function(event) {
            if (event.target == newsDetailModal) {
                newsDetailModal.style.display = 'none';
            }
        }

        // Helper untuk mendapatkan kelas badge sesuai sentimen
        function getBadgeClass(sentimen) {
            const lowerCaseSentimen = sentimen.toLowerCase().trim();
            if (lowerCaseSentimen === 'positif' || lowerCaseSentimen === 'positive') {
                return 'badge-success';
            } else if (lowerCaseSentimen === 'netral' || lowerCaseSentimen === 'neutral') {
                return 'badge-warning';
            } else if (lowerCaseSentimen === 'negatif' || lowerCaseSentimen === 'negative') {
                return 'badge-danger';
            } else {
                return 'badge-gray';
            }
        }
    </script>
</body>

</html>
