import numpy as np
from simplex_solver import SimplexSolver

def main():
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # --- FASE 1: Mencari Solusi Fisibel ---
    print("--- ✳️ MEMULAI FASE 1 ---")
    
    # Tujuan Fase 1: Maksimalkan R = -a1
    # Kolom: [x1, x2, s1, s2, s3, a1, R, Solusi]
    tableau_p1 = np.array([
        [2.,  1., -1.,  0.,  0.,  1., 0., 2.],
        [1.,  3.,  0.,  1.,  0.,  0., 0., 2.],
        [0.,  1.,  0.,  0.,  1.,  0., 0., 4.],
        [0.,  0.,  0.,  0.,  0.,  1., 1., 0.]  # Baris R = -a1  -> R+a1=0
    ])

    # Buat kanonik: R_baru = R_lama - R_dimana_a1_basis (yaitu baris 0)
    tableau_p1[-1, :] -= tableau_p1[0, :]
    
    solver_p1 = SimplexSolver(tableau_p1)
    print("Tableau Awal Fase 1 (Setelah Koreksi Basis):")
    print(solver_p1)
    solver_p1.solve()
    
    hasil_p1 = solver_p1.tableau
    if not np.isclose(hasil_p1[-1, -1], 0):
        print("\n--- ❌ Masalah tidak punya solusi fisibel. ---")
        return

    # --- FASE 2: Optimasi Fungsi Asli ---
    print("\n\n--- ✅ MEMULAI FASE 2 ---")
    
    # Ambil baris batasan dari hasil Fase 1, buang kolom a1 (indeks 5) dan R (indeks 6)
    cols_to_keep = [0, 1, 2, 3, 4, 7]
    tableau_p2 = hasil_p1[:-1, cols_to_keep]

    # Ganti baris tujuan dengan Z asli: -3x1 + x2 + Z = 0
    # Kolom Fase 2: [x1, x2, s1, s2, s3, Z, Solusi]
    baris_z = np.zeros(tableau_p2.shape[1] + 1) # Tambah 1 untuk kolom Z
    baris_z[0] = -3  # Koefisien x1
    baris_z[1] = 1   # Koefisien x2
    baris_z[-2] = 1  # Kolom Z
    
    # Gabungkan kolom Z ke tabel batasan
    col_z = np.zeros((tableau_p2.shape[0], 1))
    tableau_p2 = np.hstack([tableau_p2[:, :-1], col_z, tableau_p2[:, -1:]])
    tableau_p2 = np.vstack([tableau_p2, baris_z])
    
    # --- Koreksi Basis di Baris Z Baru (VERSI PERBAIKAN) ---
    num_vars = tableau_p2.shape[1] - 2
    for col_idx in range(num_vars):
        column = tableau_p2[:-1, col_idx]
        is_basis = np.sum(np.abs(column)) == 1 and np.count_nonzero(column) == 1
        
        if is_basis:
            # Jika kolom ini basis, koefisiennya di baris Z harus nol
            if not np.isclose(tableau_p2[-1, col_idx], 0):
                row_idx = np.where(np.isclose(column, 1))[0][0]
                koefisien = tableau_p2[-1, col_idx]
                tableau_p2[-1, :] -= koefisien * tableau_p2[row_idx, :]

    solver_p2 = SimplexSolver(tableau_p2)
    print("\nTableau Awal Fase 2 (Setelah Koreksi Basis):")
    print(solver_p2)
    solver_p2.solve()


if __name__ == "__main__":
    main()