import numpy as np
from simplex_solver import SimplexSolver

def main():
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # Definisikan M sebagai angka yang sangat besar
    M = 100000.0

    # --- PERSIAPAN TABLEAU BIG-M ---
    
    # Tujuan Asli: Min Z = 2x1 + x2  =>  Max P = -2x1 - x2
    # Tujuan Big-M: Max P = -2x1 - x2 - Ma1 - Ma2  =>  P + 2x1 + x2 + Ma1 + Ma2 = 0
    
    # Kolom: [x1, x2, s1, s2, a1, a2, P, Solusi]
    # s1 -> surplus, s2 -> slack
    
    # Baris batasan
    r1 = [3., 1.,  0., 0., 1., 0., 0., 3.]
    r2 = [4., 3., -1., 0., 0., 1., 0., 6.]
    r3 = [1., 2.,  0., 1., 0., 0., 0., 4.]
    
    # Baris P "mentah"
    p_row = [2., 1., 0., 0., M, M, 1., 0.]
    
    tableau = np.array([r1, r2, r3, p_row])
    
    # Buat kanonik: R_P_baru = R_P_lama - M*R_a1 - M*R_a2
    # a1 adalah basis di baris 0, a2 adalah basis di baris 1
    print("Tableau Awal (Sebelum Koreksi Basis):")
    print(tableau)
    
    tableau[3, :] -= M * tableau[0, :]
    tableau[3, :] -= M * tableau[1, :]
    
    # --- MENJALANKAN SOLVER ---
    print("\nTableau Awal (Setelah Koreksi Basis):")
    solver = SimplexSolver(tableau)
    print(solver)
    
    solver.solve()
    
    # --- HASIL AKHIR ---
    print("\n\n" + "="*30)
    print("       HASIL AKHIR OPTIMASI (BIG-M)")
    print("="*30)
    
    final_tableau = solver.tableau
    
    optimal_P = final_tableau[-1, -1]
    optimal_Z = -optimal_P

    print(f"\nJenis Masalah: Minimisasi")
    print(f"Nilai Optimal Z Minimal = {optimal_Z:.3f}")
    
    # Ambil nilai variabel keputusan dari tabel akhir
    print("\nSolusi Variabel Keputusan:")
    num_decision_vars = 2 # x1 dan x2
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
    
    # Cek apakah masih ada var artifisial di basis
    num_total_vars = final_tableau.shape[1] - 2
    for col in range(num_decision_vars, num_total_vars):
         column_data = final_tableau[:-1, col]
         is_basis = np.sum(np.abs(column_data)) == 1 and np.count_nonzero(column_data) == 1
         if is_basis and col >= 4: # Indeks var artifisial mulai dari 4
             print("\n⚠️ Peringatan: Variabel artifisial masih ada di basis akhir.")
             print("   Ini bisa menandakan masalah infeasible atau degenerasi.")

    print("="*30)


if __name__ == "__main__":
    main()