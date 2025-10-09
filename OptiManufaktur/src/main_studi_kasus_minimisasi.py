import numpy as np
from simplex_solver import SimplexSolver

def main():
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # --- FASE 1: MENCARI SOLUSI FISIBEL ---
    print("--- ✳️ MEMULAI FASE 1 ---")
    
    # ... (Bagian Fase 1 tetap sama persis)
    tableau_p1 = np.array([
        [3.,  2., -1.,  0.,  0.,  1.,  0., 0., 3.],
        [1.,  4.,  0., -1.,  0.,  0.,  1., 0., 4.],
        [1.,  1.,  0.,  0.,  1.,  0.,  0., 0., 5.],
        [0.,  0.,  0.,  0.,  0.,  1.,  1., 1., 0.]
    ])
    tableau_p1[-1, :] -= tableau_p1[0, :]
    tableau_p1[-1, :] -= tableau_p1[1, :]
    
    solver_p1 = SimplexSolver(tableau_p1)
    solver_p1.solve()
    
    hasil_p1 = solver_p1.tableau
    if not np.isclose(hasil_p1[-1, -1], 0):
        print("\n--- ❌ Masalah tidak punya solusi fisibel. ---")
        return

    # --- FASE 2: OPTIMASI FUNGSI ASLI ---
    print("\n\n--- ✅ MEMULAI FASE 2 ---")
    
    # ... (Bagian persiapan dan penyelesaian Fase 2 tetap sama persis)
    num_vars_original_slack = 5
    cols_to_keep = list(range(num_vars_original_slack)) + [-1]
    tableau_p2_constraints = hasil_p1[:-1, cols_to_keep]

    p_row = np.zeros(tableau_p2_constraints.shape[1] + 1)
    p_row[0] = 5
    p_row[1] = 8
    p_row[-2] = 1
    
    col_p_for_constraints = np.zeros((tableau_p2_constraints.shape[0], 1))
    tableau_p2 = np.hstack([tableau_p2_constraints[:, :-1], col_p_for_constraints, tableau_p2_constraints[:, -1:]])
    tableau_p2 = np.vstack([tableau_p2, p_row])
    
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
    solver_p2.solve()

    # --- HASIL AKHIR YANG SUDAH DIPERBAIKI ---
    print("\n\n" + "="*30)
    print("       HASIL AKHIR OPTIMASI")
    print("="*30)
    
    final_tableau = solver_p2.tableau
    
    # Ambil nilai P_maks dari solver
    optimal_P = final_tableau[-1, -1]
    # Konversi ke Z_min
    optimal_Z = -optimal_P

    print(f"\nJenis Masalah: Minimisasi")
    print(f"Nilai Optimal Z Minimal = {optimal_Z:.3f}")
    
    # Ambil nilai variabel keputusan dari tabel akhir
    print("\nSolusi Variabel Keputusan:")
    num_decision_vars = 2 # Kita tahu ada x1 dan x2
    solution = {}
    for col in range(num_decision_vars):
        column_data = final_tableau[:, col]
        is_basis = np.sum(np.abs(column_data)) == 1 and np.count_nonzero(column_data) == 1
        if is_basis:
            row_index = np.where(np.isclose(column_data, 1))[0][0]
            solution[f'x{col+1}'] = final_tableau[row_index, -1]

    for i in range(num_decision_vars):
        value = solution.get(f'x{i+1}', 0)
        print(f"  x{i+1} = {value:.3f}")
    
    print("="*30)


if __name__ == "__main__":
    main()