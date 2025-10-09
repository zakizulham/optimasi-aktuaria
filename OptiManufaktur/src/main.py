import numpy as np
from simplex_solver import SimplexSolver

def main():
    """
    Fungsi utama untuk menjalankan program.
    """
    print("--- OptiManufaktur Solver ---")

    np.set_printoptions(linewidth=np.inf, suppress=True, precision=3) # type: ignore

    # Definisikan masalah baru
    # Kolom: [x1, x2, s1, s2, Z, Solusi]
    tableau_phase1 = np.array([
        [2,   1,  1,  0,  0,  50 ],
        [2,   5,  0,  1,  0,  100],
        [2,   3,  1,  0,  0,  90 ],
        [-4, -10, 0,  0,  1,  0  ]
    ])

    # Inisialisasi solver dengan masalah kita
    solver = SimplexSolver(tableau_phase1)

    # Cetak tabel awal untuk verifikasi
    print("Tabel Simpleks Awal (Fase 1):")
    print("Ingat Kolom: [x1, x2, s1, s2, Z, Solusi]")
    print(solver)

    # Panggil method solve (saat ini belum melakukan apa-apa)
    solver.solve()


if __name__ == "__main__":
    main()