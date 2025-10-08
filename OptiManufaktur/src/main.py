import numpy as np
from simplex_solver import SimplexSolver

def main():
    """
    Fungsi utama untuk menjalankan program.
    """
    print("--- OptiManufaktur Solver ---")

    # Definisikan masalah dari Fase 1
    # Kolom: [x1, x2, s1, s2, Z, Solusi]
    tableau_phase1 = np.array([
        [4,   2,  1,  0,  0,  60],
        [2,   4,  0,  1,  0,  48],
        [-80, -60, 0,  0,  1,  0]
    ])

    # Inisialisasi solver dengan masalah kita
    solver = SimplexSolver(tableau_phase1)

    # Cetak tabel awal untuk verifikasi
    print("Tabel Simpleks Awal (Fase 1):")
    print(solver)

    # Panggil method solve (saat ini belum melakukan apa-apa)
    solver.solve()


if __name__ == "__main__":
    main()