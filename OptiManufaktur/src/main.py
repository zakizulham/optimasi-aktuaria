import numpy as np
from simplex_solver import SimplexSolver

def main():
    """
    Menjalankan solver Simpleks Standar untuk soal maksimisasi.
    """
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # --- Definisi Masalah ---
    # Maksimisasi Z = 3x1 + 2x2 + 3x3
    
    # Kolom: [x1, x2, x3, s1, s2, Z, Solusi]
    tableau = np.array([
        [2.,  1.,  1.,  1.,  0.,  0.,  2.],
        [3.,  4.,  2.,  0.,  1.,  0.,  8.],
        [-3., -2., -3.,  0.,  0.,  1.,  0.]
    ])

    # Buat dan jalankan solver
    solver = SimplexSolver(tableau, num_decision_vars=3)
    print("--- ✳️ MEMULAI SOLVER SIMPLEKS STANDAR ---")
    print("Tableau Awal:")
    print(solver)
    
    solver.solve()
    
    # --- HASIL AKHIR ---
    # Kita bisa langsung menggunakan display_solution karena ini masalah maksimisasi standar
    print("\n\n" + "="*30)
    print("       HASIL AKHIR OPTIMASI")
    print("="*30)
    solver.display_solution()
    print("="*30)


if __name__ == "__main__":
    main()