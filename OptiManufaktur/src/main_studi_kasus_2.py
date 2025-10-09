import numpy as np
from simplex_solver import SimplexSolver

def main():
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # --- FASE 1: Mencari Solusi Fisibel ---
    print("--- ✳️ MEMULAI FASE 1 ---")
    
    # Tujuan Fase 1: Maksimalkan R = -a1
    # Batasan setelah ditambah surplus (s1), slack (s2, s3), dan artifisial (a1)
    # 2x1 + x2 - s1 + a1 = 2
    #  x1 + 3x2 + s2      = 2
    #       x2 + s3      = 4

    # Kolom: [x1, x2, s1, s2, s3, a1, R, Solusi]
    tableau_p1 = np.array([
        [2.,  1., -1.,  0.,  0.,  1., 0., 2.],
        [1.,  3.,  0.,  1.,  0.,  0., 0., 2.],
        [0.,  1.,  0.,  0.,  1.,  0., 0., 4.],
        [0.,  0.,  0.,  0.,  0.,  1., 1., 0.]  # Baris R = -a1  -> R+a1=0
    ])

    # Buat kanonik: R_baru = R_lama - R_dimana_a1_basis
    tableau_p1[-1, :] -= tableau_p1[0, :]
    
    solver_p1 = SimplexSolver(tableau_p1)
    solver_p1.solve()
    
    # Cek hasil
    hasil_p1 = solver_p1.tableau
    if not np.isclose(hasil_p1[-1, -1], 0):
        print("\n--- ❌ Masalah tidak punya solusi fisibel. ---")
        return

    # --- FASE 2: Optimasi Fungsi Asli ---
    print("\n\n--- ✅ MEMULAI FASE 2 ---")
    
    # Persiapan Tableau Fase 2
    # Ambil baris batasan dari hasil Fase 1, buang kolom a1 dan R
    tableau_p2 = hasil_p1[:-1, :-2]

    # Ganti baris tujuan dengan Z asli: -3x1 + x2 + Z = 0
    baris_z = np.zeros(tableau_p2.shape[1])
    baris_z[0] = -3  # Koefisien x1
    baris_z[1] = 1   # Koefisien x2
    baris_z[-2] = 1  # Kolom Z
    
    tableau_p2 = np.vstack([tableau_p2, baris_z])
    
    # Koreksi basis di baris Z baru
    # Dari hasil Fase 1, kita akan lihat x1 dan x2 menjadi basis.
    # Misalnya, x1 basis di baris 0, dan s2 di baris 1.
    for col_idx in range(2): # Cek untuk x1 dan x2
        if not np.isclose(tableau_p2[-1, col_idx], 0):
            # Cari baris mana var ini menjadi basis
            for r in range(len(tableau_p2)-1):
                if np.isclose(tableau_p2[r, col_idx], 1.0):
                    koefisien = tableau_p2[-1, col_idx]
                    tableau_p2[-1, :] -= koefisien * tableau_p2[r, :]

    solver_p2 = SimplexSolver(tableau_p2)
    solver_p2.solve()


if __name__ == "__main__":
    main()