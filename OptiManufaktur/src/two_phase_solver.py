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