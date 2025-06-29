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
            /* Warna teks gelap */
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
            width: 90%;
            /* Could be more or less, depending on screen size */
            max-width: 800px;
            /* Lebar maksimal modal */
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

        /* Gaya untuk Dark Mode */
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

        html.dark .text-gray-800 {
            color: #f9fafb;
        }

        html.dark .text-gray-900 {
            color: #f9fafb;
        }

        html.dark .text-gray-600 {
            color: #d1d5db;
        }

        html.dark .text-gray-500 {
            color: #9ca3af;
        }

        html.dark .text-blue-600 {
            color: #60a5fa;
        }

        html.dark .close-button {
            color: #d1d5db;
        }

        html.dark .badge-gray {
            background-color: #374151;
            color: #d1d5db;
        }

        /* Modal dark mode adjustments */
        html.dark .modal-content {
            background-color: #1f2937;
            border-color: #374151;
            color: #d1d5db;
        }

        html.dark .prose {
            color: #d1d5db;
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
                @else bg-gray-100 text-gray-800 @endif">
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
