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