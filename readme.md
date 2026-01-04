# Quiz Sederhana (Python + Kivy)

Aplikasi quiz pilihan ganda sederhana dibuat dengan Python 3 dan Kivy.

Fitur:
- Tampilan awal berisi judul dan tombol Mulai
- Menampilkan pertanyaan pilihan ganda (A, B, C, D)
- Pengguna pilih satu jawaban (ToggleButton)
- Tombol Next untuk pindah soal
- Skor otomatis (+1 untuk jawaban benar)
- Halaman hasil menampilkan skor total

Teknis:
- Bahasa: Python 3
- GUI: Kivy
- Navigasi layar: ScreenManager
- Pertanyaan disimpan dalam list (`QUESTIONS`) di `apt.py`
- Kode diberi komentar agar mudah dipahami

Cara menjalankan (untuk pemula):
1. Pastikan Python 3 sudah terpasang (cek dengan `python3 --version`).
2. Pasang Kivy dengan pip:

   pip install kivy

   Catatan: pada beberapa sistem (terutama macOS) pemasangan Kivy mungkin memerlukan dependensi tambahan.
   Jika ada masalah, lihat dokumentasi Kivy: https://kivy.org
3. Buka terminal dan pindah ke folder project:

   cd /Users/popy/Desktop/python/quiz1

4. Jalankan aplikasi:

   python3 apt.py

5. Aplikasi akan terbuka dalam jendela. Tekan tombol "Mulai", pilih jawaban, lalu tekan "Next" sampai selesai.

Catatan singkat:
- Jika ingin menambah soal, edit daftar `QUESTIONS` di `apt.py`.
- Untuk menjalankan di virtual environment, buat venv lalu instal Kivy di dalamnya.

Semoga membantu — aplikasi ini disusun agar mudah dibaca dan dimodifikasi oleh pemula.