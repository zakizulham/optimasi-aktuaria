# OptiManufaktur: Solver Metode Simpleks

![GitHub language count](https://img.shields.io/github/languages/count/zakizulham/OptiManufaktur)
![GitHub top language](https://img.shields.io/github/languages/top/zakizulham/OptiManufaktur)
![GitHub last commit](https://img.shields.io/github/last-commit/zakizulham/OptiManufaktur)

Selamat datang di repositori **OptiManufaktur**. Proyek ini adalah implementasi *solver* metode simpleks dari nol menggunakan Python, yang dirancang sebagai alat pembelajaran berbasis proyek untuk Riset Operasi dan pemrograman linier.

## 🎯 Tujuan Proyek

Tujuan utama dari proyek ini adalah untuk membangun pemahaman mendalam tentang cara kerja internal algoritma simpleks dengan mengimplementasikannya secara langsung. Proyek ini mencakup:
-   **Maksimisasi & Minimisasi**: Menyelesaikan masalah program linier standar.
-   **Metode Big M**: Menangani batasan `≥` dan `=` dengan menggunakan variabel artifisial dan penalti.
-   **Metode Dua Fase**: Pendekatan alternatif untuk menemukan solusi fisibel awal sebelum optimasi.
-   **Analisis Sensitivitas**: Memberikan wawasan dasar tentang bagaimana perubahan pada batasan dapat memengaruhi solusi optimal.

Untuk rincian lengkap mengenai rencana dan tahapan pengembangan, silakan merujuk ke file [PROJECT_PLAN.md](PROJECT_PLAN.md).

## 🛠️ Teknologi yang Digunakan
Python 3.8+

## 🚀 Cara Menjalankan

*(Bagian ini akan diisi nanti setelah implementasi awal selesai)*

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/zakizulham/optimasi-aktuaria.git
    cd optimasi-aktuaria/OptiManufaktur
    ```
2.  **Buat virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
    ```
3.  **Install dependensi:**
    ```bash
    pip install -r requirements.txt # (File ini akan dibuat nanti)
    ```
4.  **Jalankan solver:**
    ```bash
    python src/main.py
    ```

## 📂 Struktur Repositori

```
/OptiManufaktur
|-- .gitignore
|-- README.md
|-- PROJECT_PLAN.md
|-- /src
|   |-- simplex_solver.py  # Logika inti solver
|   |-- main.py            # Titik masuk program
|-- /data
|   |-- problem.json       # Contoh file input masalah
|-- /notebooks
    |-- exploration.ipynb  # Notebook untuk eksperimen
```
