# Soal Fase 1: Maksimisasi Profit Produksi

## 1. Deskripsi Masalah

Sebuah pabrik furnitur "KayuJaya" memproduksi dua produk: **Meja** dan **Kursi**. Proses produksi dibatasi oleh ketersediaan jam kerja di dua departemen: Perakitan dan Pemolesan. Data terkait produksi adalah sebagai berikut:

-   **Profit**:
    -   Setiap Meja ($x_1$) memberikan profit **$80**.
    -   Setiap Kursi ($x_2$) memberikan profit **$60**.
-   **Kebutuhan Jam Kerja & Ketersediaan**:
    -   **Departemen Perakitan**: 1 Meja butuh 4 jam, 1 Kursi butuh 2 jam. Total jam tersedia adalah **60 jam/minggu**.
    -   **Departemen Pemolesan**: 1 Meja butuh 2 jam, 1 Kursi butuh 4 jam. Total jam tersedia adalah **48 jam/minggu**.

**Pertanyaan**: Berapa jumlah Meja dan Kursi yang harus diproduksi setiap minggu untuk memaksimalkan total profit?

---

## 2. Bedah Soal & Informasi Kunci

Dari deskripsi di atas, kita dapat mengekstrak informasi berikut untuk membangun model program linier:

-   **Tujuan (Objective)**: **Maksimisasi** total profit ($Z$). Ini adalah masalah optimasi.
-   **Variabel Keputusan (Decision Variables)**:
    -   $x_1$: Jumlah Meja yang akan diproduksi.
    -   $x_2$: Jumlah Kursi yang akan diproduksi.
-   **Fungsi Tujuan (Objective Function)**: Persamaan matematis dari tujuan kita.
    -   $Z = 80x_1 + 60x_2$
-   **Batasan (Constraints)**: Sumber daya yang terbatas yang membatasi produksi.
    -   Batasan Perakitan: $4x_1 + 2x_2 \le 60$
    -   Batasan Pemolesan: $2x_1 + 4x_2 \le 48$
-   **Batasan Non-Negatif (Non-negativity)**: Jumlah produk tidak mungkin negatif.
    -   $x_1 \ge 0$, $x_2 \ge 0$

---

## 3. Rencana Algoritma Penyelesaian

Masalah ini adalah kasus klasik program linier dan akan diselesaikan menggunakan **Algoritma Simpleks**. Langkah-langkahnya adalah sebagai berikut:

1.  **Mengubah ke Bentuk Standar**: Mengubah semua batasan pertidaksamaan (`≤`) menjadi persamaan (`=`) dengan menambahkan **variabel slack** ($s_1, s_2$).
2.  **Membuat Tabel Simpleks Awal**: Merepresentasikan seluruh sistem persamaan (termasuk fungsi tujuan) ke dalam sebuah matriks (tableau).
3.  **Melakukan Iterasi Simpleks**:
    a. **Cek Kondisi Optimal**: Jika semua koefisien pada baris fungsi tujuan (baris Z) non-negatif (≥ 0), solusi optimal telah ditemukan. Jika tidak, lanjut.
    b. **Tentukan Kolom Pivot**: Pilih kolom dengan nilai negatif terbesar di baris Z. Variabel pada kolom ini akan menjadi *entering variable*.
    c. **Tentukan Baris Pivot**: Hitung rasio antara kolom solusi (RHS) dengan kolom pivot. Pilih baris dengan rasio positif terkecil. Variabel pada baris ini akan menjadi *leaving variable*.
    d. **Lakukan Operasi Baris Elementer (OBE)**: Perbarui tabel dengan menjadikan elemen pivot bernilai 1 dan elemen lain di kolom pivot bernilai 0.
    e. Ulangi dari langkah 3a.
4.  **Interpretasi Solusi**: Setelah kondisi optimal tercapai, baca nilai variabel keputusan dan nilai fungsi tujuan dari tabel akhir.

**Implementasi Teknis**:
Algoritma ini akan diimplementasikan menggunakan Python. Logika inti dari algoritma simpleks akan berada dalam sebuah *class* `SimplexSolver` di file `src/simplex_solver.py`. Proses inisialisasi masalah dan pemanggilan *solver* akan dieksekusi dari file `src/main.py`.