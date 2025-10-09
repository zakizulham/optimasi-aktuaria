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
        num_constraints, num_vars = self.A.shape
        
        # Buat matriks artifisial (matriks identitas)
        A_artificial = np.identity(num_constraints)
        
        # Gabungkan matriks A dengan matriks artifisial
        # Kolom: [vars_asli, vars_artifisial, Solusi]
        A_phase1 = np.hstack([self.A, A_artificial, self.b.reshape(-1, 1)])
        
        # Buat baris tujuan Fase 1: Minimalkan W = sum(a_i) -> Maksimalkan R = -sum(a_i)
        # R + a1 + a2 + ... = 0
        c_phase1 = np.zeros(A_phase1.shape[1])
        c_phase1[num_vars : num_vars + num_constraints] = 1 # Koefisien a_i di R
        c_phase1[-2] = 1 # Koefisien R

        tableau = np.vstack([A_phase1, c_phase1])
        
        # Jadikan tableau kanonik: koefisien var basis (a_i) di baris R harus 0
        for i in range(num_constraints):
            tableau[-1,:] -= tableau[i,:]
            
        return tableau
    
    def solve(self):
        """Menjalankan keseluruhan proses Two-Phase."""
        print("--- ✳️ MEMULAI FASE 1: MENCARI SOLUSI FISIBEL ---")
        
        # 1. Bangun dan selesaikan Fase 1
        tableau_p1 = self._build_phase1_tableau()
        solver_p1 = SimplexSolver(tableau_p1)
        solver_p1.solve()

        # 2. Cek hasil Fase 1
        final_tableau_p1 = solver_p1.tableau
        optimal_W = final_tableau_p1[-1, -1]

        # Karena kita memaksimalkan R = -W, nilai optimal R harus 0.
        if not np.isclose(optimal_W, 0):
            print("\n--- ❌ MASALAH TIDAK MEMILIKI SOLUSI FISIBEL ---")
            return

        print("\n\n--- ✅ FASE 1 BERHASIL. MEMULAI FASE 2: OPTIMASI ---")

        # 3. Persiapkan tableau Fase 2
        num_original_vars = len(self.original_c)
        num_constraints = len(self.b)
        
        # Ambil bagian yang relevan dari tabel akhir Fase 1
        # Kolom: [vars_asli, vars_slack/surplus, Solusi]
        tableau_p2 = final_tableau_p1[:-1, np.r_[0:num_original_vars, -1]]
        
        # Buat baris tujuan Z yang baru
        new_z_row = np.zeros(tableau_p2.shape[1])
        new_z_row[0:num_original_vars] = -self.original_c # Koefisien -c
        new_z_row[-2] = 1 # Kolom Z
        
        tableau_p2 = np.vstack([tableau_p2, new_z_row])
        
        # 4. Jadikan kanonik untuk Fase 2
        # Untuk setiap var basis, koefisiennya di baris Z harus 0
        for col in range(num_original_vars):
             # Cek apakah var ini adalah basis
            column_data = tableau_p2[:-1, col]
            if np.sum(column_data) == 1 and np.count_nonzero(column_data) == 1:
                row_idx = np.where(column_data == 1)[0][0]
                z_coeff = tableau_p2[-1, col]
                if not np.isclose(z_coeff, 0):
                    tableau_p2[-1,:] -= z_coeff * tableau_p2[row_idx,:]

        # 5. Selesaikan Fase 2
        solver_p2 = SimplexSolver(tableau_p2)
        print("\nTableau Awal Fase 2 (setelah koreksi basis):")
        print(solver_p2)
        solver_p2.solve()