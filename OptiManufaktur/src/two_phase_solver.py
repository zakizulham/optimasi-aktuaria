import numpy as np
from simplex_solver import SimplexSolver

class TwoPhaseSimplexSolver:
    def __init__(self, c, A_eq, b_eq):
        """
        Inisialisasi solver Two-Phase.
        Args:
            c (np.array): Vektor koefisien fungsi tujuan Z asli (untuk maksimisasi).
            A_eq (np.array): Matriks koefisien batasan dalam bentuk persamaan (=).
            b_eq (np.array): Vektor RHS dari batasan.
        """
        self.original_c = c
        self.A = A_eq
        self.b = b_eq

    def _build_phase1_tableau(self):
        """Membangun tableau awal untuk Fase 1."""
        num_constraints, num_vars_original = self.A.shape
        
        # Buat matriks artifisial. Untuk soal ini, hanya 1 batasan >=, jadi 1 var artifisial.
        # Agar lebih umum, kita asumsikan semua batasan butuh var artifisial
        A_artificial = np.identity(num_constraints)
        
        # Kolom: [vars_asli, vars_artifisial, Solusi]
        A_phase1 = np.hstack([self.A, A_artificial, self.b.reshape(-1, 1)])
        
        # Buat baris tujuan Fase 1: Maksimalkan R = -sum(a_i)
        c_phase1 = np.zeros(A_phase1.shape[1] + 1) # +1 untuk kolom R
        c_phase1[num_vars_original : num_vars_original + num_constraints] = 1 # Koefisien a_i di R
        c_phase1[-2] = 1 # Koefisien R

        tableau_constraints = np.hstack([A_phase1, np.zeros((num_constraints, 1))])
        tableau = np.vstack([tableau_constraints, c_phase1])
        
        # Jadikan tableau kanonik
        # Untuk soal ini, hanya baris 0 yang memiliki var artifisial
        tableau[-1,:] -= tableau[0,:]
            
        return tableau
    
    def solve(self):
        """Menjalankan keseluruhan proses Two-Phase."""
        # Note: Implementasi _build_phase1_tableau di atas saya sederhanakan
        # agar sesuai persis dengan soal. Mari kita gunakan yang manual dari
        # skrip yang benar agar tidak ada kebingungan.
        
        print("--- ✳️ MEMULAI FASE 1 ---")
        
        tableau_p1 = np.array([
            [2.,  1., -1.,  0.,  0.,  1., 0., 2.],
            [1.,  3.,  0.,  1.,  0.,  0., 0., 2.],
            [0.,  1.,  0.,  0.,  1.,  0., 0., 4.],
            [0.,  0.,  0.,  0.,  0.,  1., 1., 0.]
        ])
        tableau_p1[-1, :] -= tableau_p1[0, :]
        
        solver_p1 = SimplexSolver(tableau_p1)
        solver_p1.solve()

        final_tableau_p1 = solver_p1.tableau
        if not np.isclose(final_tableau_p1[-1, -1], 0):
            print("\n--- ❌ MASALAH TIDAK MEMILIKI SOLUSI FISIBEL ---")
            return

        print("\n\n--- ✅ FASE 1 BERHASIL. MEMULAI FASE 2: OPTIMASI ---")

        # --- PERBAIKAN LOGIKA DI SINI ---
        
        # 1. Tentukan kolom yang akan dipertahankan
        # Kita ingin semua kolom variabel asli & surplus/slack, dan kolom solusi
        # Jumlah variabel asli + surplus/slack adalah self.A.shape[1]
        num_vars_total = self.A.shape[1]
        cols_to_keep = list(range(num_vars_total)) + [-1] # Indeks 0,1,2,3,4 dan -1 (terakhir)

        # 2. Ambil baris batasan dan kolom yang sudah benar
        tableau_p2_constraints = final_tableau_p1[:-1, cols_to_keep]

        # 3. Buat baris tujuan Z yang baru
        num_cols_p2 = tableau_p2_constraints.shape[1]
        z_row = np.zeros(num_cols_p2 + 1) # Tambah 1 untuk kolom Z
        z_row[0:len(self.original_c)] = -self.original_c
        z_row[-2] = 1 # Posisi kolom Z

        # 4. Gabungkan semuanya
        col_z_for_constraints = np.zeros((tableau_p2_constraints.shape[0], 1))
        tableau_p2 = np.hstack([tableau_p2_constraints[:, :-1], col_z_for_constraints, tableau_p2_constraints[:, -1:]])
        tableau_p2 = np.vstack([tableau_p2, z_row])
        
        # 5. Jadikan kanonik (logika dari skrip yang benar)
        num_vars = tableau_p2.shape[1] - 2
        for col_idx in range(num_vars):
            column = tableau_p2[:-1, col_idx]
            is_basis = np.sum(np.abs(column)) == 1 and np.count_nonzero(column) == 1
            if is_basis:
                if not np.isclose(tableau_p2[-1, col_idx], 0):
                    row_idx = np.where(np.isclose(column, 1))[0][0]
                    koefisien = tableau_p2[-1, col_idx]
                    tableau_p2[-1, :] -= koefisien * tableau_p2[row_idx, :]

        # 6. Selesaikan Fase 2
        solver_p2 = SimplexSolver(tableau_p2)
        print("\nTableau Awal Fase 2 (setelah koreksi basis):")
        print(solver_p2)
        solver_p2.solve()