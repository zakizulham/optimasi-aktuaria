import numpy as np
from simplex_solver import SimplexSolver

def main():
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # --- FASE 1: MENCARI SOLUSI FISIBEL ---
    print("--- ✳️ MEMULAI FASE 1 ---")
    
    # Tujuan Fase 1: Maksimalkan R = -a1 - a2
    # Kolom: [x1, x2, s1, s2, s3, a1, a2, R, Solusi]
    tableau_p1 = np.array([
        [3.,  2., -1.,  0.,  0.,  1.,  0., 0., 3.],
        [1.,  4.,  0., -1.,  0.,  0.,  1., 0., 4.],
        [1.,  1.,  0.,  0.,  1.,  0.,  0., 0., 5.],
        [0.,  0.,  0.,  0.,  0.,  1.,  1., 1., 0.]  # Baris R + a1 + a2 = 0
    ])

    # Buat kanonik: R_baru = R_lama - R_a1 - R_a2
    tableau_p1[-1, :] -= tableau_p1[0, :]
    tableau_p1[-1, :] -= tableau_p1[1, :]
    
    solver_p1 = SimplexSolver(tableau_p1)
    print("Tableau Awal Fase 1 (Setelah Koreksi Basis):")
    print(solver_p1)
    solver_p1.solve()
    
    hasil_p1 = solver_p1.tableau
    if not np.isclose(hasil_p1[-1, -1], 0):
        print("\n--- ❌ Masalah tidak punya solusi fisibel. ---")
        return

    # --- FASE 2: OPTIMASI FUNGSI ASLI ---
    print("\n\n--- ✅ MEMULAI FASE 2 ---")
    
    # Buang kolom artifisial (a1, a2) dan kolom R
    num_vars_original_slack = 5 # x1, x2, s1, s2, s3
    cols_to_keep = list(range(num_vars_original_slack)) + [-1] # Indeks 0,1,2,3,4 dan -1 (terakhir)
    tableau_p2_constraints = hasil_p1[:-1, cols_to_keep]

    # Buat baris tujuan P (Z) baru: 5x1 + 8x2 + P = 0
    num_cols_p2 = tableau_p2_constraints.shape[1]
    p_row = np.zeros(num_cols_p2 + 1) # Tambah 1 untuk kolom P
    p_row[0] = 5  # Koefisien x1
    p_row[1] = 8  # Koefisien x2
    p_row[-2] = 1 # Kolom P (Z)
    
    # Gabungkan semuanya
    col_p_for_constraints = np.zeros((tableau_p2_constraints.shape[0], 1))
    tableau_p2 = np.hstack([tableau_p2_constraints[:, :-1], col_p_for_constraints, tableau_p2_constraints[:, -1:]])
    tableau_p2 = np.vstack([tableau_p2, p_row])
    
    # Koreksi Basis di Baris P Baru
    num_vars = tableau_p2.shape[1] - 2
    for col_idx in range(num_vars):
        column = tableau_p2[:-1, col_idx]
        is_basis = np.sum(np.abs(column)) == 1 and np.count_nonzero(column) == 1
        
        if is_basis:
            if not np.isclose(tableau_p2[-1, col_idx], 0):
                row_idx = np.where(np.isclose(column, 1))[0][0]
                koefisien = tableau_p2[-1, col_idx]
                tableau_p2[-1, :] -= koefisien * tableau_p2[row_idx, :]

    solver_p2 = SimplexSolver(tableau_p2)
    print("\nTableau Awal Fase 2 (Setelah Koreksi Basis):")
    print(solver_p2)
    solver_p2.solve()

    # Tampilkan hasil akhir
    print("\n--- HASIL AKHIR ---")
    optimal_P = solver_p2.tableau[-1, -1]
    optimal_Z = -optimal_P
    print(f"Nilai P Maksimal = {optimal_P:.3f}")
    print(f"Nilai Z Minimal = {optimal_Z:.3f}")
    solver_p2.display_solution()


if __name__ == "__main__":
    main()