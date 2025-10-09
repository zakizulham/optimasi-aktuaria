import numpy as np
from two_phase_solver import TwoPhaseSimplexSolver

def main():
    """
    Menjalankan solver Two-Phase untuk soal yang diberikan.
    """
    np.set_printoptions(linewidth=99999, suppress=True, precision=3)

    # --- Definisi Masalah Asli ---
    # Maksimisasi Z = 3x1 - x2
    # Kendala:
    # 2x1 + x2 >= 2  ->  2x1 + x2 - s1 = 2
    #  x1 + 3x2 <= 2  ->   x1 + 3x2 + s2 = 2
    #       x2 <= 4  ->        x2 + s3 = 4

    # Vektor Z asli
    c = np.array([3, -1])

    # Matriks A dan vektor b dalam bentuk persamaan
    # Kolom: [x1, x2, s1, s2, s3]
    A_eq = np.array([
        [2,  1, -1,  0,  0],
        [1,  3,  0,  1,  0],
        [0,  1,  0,  0,  1]
    ])

    b_eq = np.array([2, 2, 4])

    # Buat dan jalankan solver
    solver = TwoPhaseSimplexSolver(c, A_eq, b_eq)
    solver.solve()


if __name__ == "__main__":
    main()