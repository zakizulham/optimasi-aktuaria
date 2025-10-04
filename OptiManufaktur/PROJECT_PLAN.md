# Proyek: OptiManufaktur

## Deskripsi
Proyek ini bertujuan untuk membangun sebuah program solver metode simpleks dari nol untuk membantu pengambilan keputusan produksi di sebuah pabrik furnitur fiktif "KayuJaya". Proyek ini berfokus pada pembelajaran *project-based* untuk memahami algoritma simpleks, kasus maksimisasi, minimisasi, Metode Big M, dan Metode Dua Fase.

---

## Fase Proyek

### Fase 1: Kasus Dasar - Maksimisasi Profit (Standard Simplex)
**Skenario**: Memaksimalkan profit mingguan dari produksi Meja ($x_1$) dan Kursi ($x_2$).

**Model Matematis**:
- **Fungsi Tujuan (Maksimisasi)**: $Z = 80x_1 + 60x_2$
- **Batasan**:
  1. $4x_1 + 2x_2 \le 60$  (Departemen Perakitan)
  2. $2x_1 + 4x_2 \le 48$  (Departemen Pemolesan)
  3. $x_1, x_2 \ge 0$

**Tujuan Fase 1**:
1. Mendesain struktur data untuk tabel simpleks.
2. Mengimplementasikan algoritma simpleks standar (pemilihan pivot, OBE, deteksi optimal).
3. Menghasilkan output solusi optimal (nilai $x_1$, $x_2$, dan $Z$).

### Fase 2: Kasus Lanjutan - Minimisasi Biaya (Big M Method)
**Skenario**: Meminimalkan biaya pembelian bahan baku P ($x_1$) dan Q ($x_2$) untuk memenuhi kontrak suplai nutrisi.

**Model Matematis**:
- **Fungsi Tujuan (Minimisasi)**: $C = 10x_1 + 12x_2$
- **Batasan**:
  1. $2x_1 + 4x_2 \ge 20$  (Kebutuhan Nutrisi A)
  2. $5x_1 + 3x_2 \ge 30$  (Kebutuhan Nutrisi B)
  3. $x_1, x_2 \ge 0$

**Tujuan Fase 2**:
1. Memahami kebutuhan variabel surplus dan artifisial untuk batasan '≥'.
2. Mengimplementasikan Metode Big M dengan memberi penalti (M) pada variabel artifisial di fungsi tujuan.

### Fase 3: Kasus Kompleks - Batasan Campuran (Two-Phase Method)
**Skenario**: Memenuhi pesanan kompleks yang melibatkan Meja ($x_1$), Kursi ($x_2$), dan Lemari ($x_3$) dengan berbagai jenis batasan.

**Model Matematis (Contoh)**:
- **Fungsi Tujuan (Maksimisasi)**: $Z = 5x_1 + 8x_2 + 4x_3$
- **Batasan**:
  1. $x_1 + x_2 \le 100$      (Batasan Kayu, tipe '≤')
  2. $x_2 + 2x_3 \ge 60$       (Permintaan Minimal, tipe '≥')
  3. $x_1 + x_3 = 40$         (Kontrak Pasti, tipe '=')
  4. $x_1, x_2, x_3 \ge 0$

**Tujuan Fase 3**:
1. Mengimplementasikan Metode Dua Fase:
   - **Fase 1**: Mencari solusi fisibel dengan meminimalkan jumlah variabel artifisial.
   - **Fase 2**: Menggunakan solusi fisibel dari Fase 1 untuk menyelesaikan masalah optimasi asli.
2. Mampu menangani ketiga jenis batasan (`<=`, `>=`, `=`) dalam satu solver.

### Fase 4: Pengembangan & Analisis (The Practitioner Part)
**Skenario**: Mengubah solver dari alat hitung menjadi alat bantu keputusan.

**Tujuan Fase 4**:
1. **Input Fleksibel**: Membaca model masalah dari file eksternal (misalnya, JSON/CSV).
2. **Analisis Sensitivitas**: Menghitung dan menampilkan "Shadow Price" dan "Reduced Cost".
3. **Interpretasi Hasil**: Menerjemahkan output numerik menjadi laporan bisnis yang mudah dipahami.

---

## Struktur Repositori (Proposal)

```
/OptiManufaktur
|-- .gitignore
|-- README.md
|-- PROJECT_PLAN.md
|-- /src
|   |-- simplex_solver.py
|   |-- main.py
|   |-- utils.py
|-- /data
|   |-- phase1_problem.json
|   |-- phase2_problem.json
|   |-- phase3_problem.json
|-- /notebooks
|   |-- 01_Phase1_Maximization.ipynb
|   |-- 02_Phase2_BigM.ipynb
|   |-- 03_Phase3_TwoPhase.ipynb
|-- /tests
    |-- test_solver.py
```