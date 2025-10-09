import numpy as np

class SimplexSolver:
    """
    Sebuah class untuk menyelesaikan masalah program linier
    menggunakan algoritma simpleks.
    """
    def __init__(self, tableau, num_decision_vars = 2):
        """
        Inisialisasi solver dengan tabel simpleks awal.

        Args:
            tableau (np.array): Matriks tabel simpleks awal (baris terakhir fungsi tujuan)
            num_decision_vars (int): Jumlah variabel keputusan (x)
        """
        self.tableau = np.array(tableau, dtype=float)
        self.num_decision_vars = num_decision_vars 

    def solve(self):
        max_iterations = 100
        iteration = 0

        while not self.is_optimal() and iteration < max_iterations:
            print(f"\n--- Iterasi ke-{iteration + 1} ---")
            
            pivot_col = self.find_pivot_column()
            print(f"Kolom Pivot: {pivot_col}")

            pivot_row = self.find_pivot_row(pivot_col)
            if pivot_row == -1:
                print("Solusi tidak terbatas (unbounded).")
                return None
            
            print(f"Baris Pivot: {pivot_row}")
            
            self.do_pivot(pivot_row, pivot_col)
            print("Tabel setelah pivot:")
            print(self.tableau)
            
            iteration += 1

        if self.is_optimal():
            print("\n✅ Kondisi optimal tercapai.")
            self.display_solution()
        else:
            print("\n⚠️ Gagal menemukan solusi optimal dalam batas iterasi.")

    def is_optimal(self):
        objective_row = self.tableau[-1, :-1]
        return np.all(objective_row >= 0)

    def find_pivot_column(self):
        objective_row = self.tableau[-1, :-1]
        return np.argmin(objective_row)

    def find_pivot_row(self, pivot_col):
        ratios = []
        for i, row in enumerate(self.tableau[:-1, :]):
            element = row[pivot_col]
            if element > 0:
                ratio = row[-1] / element
                ratios.append(ratio)
            else:
                ratios.append(float('inf'))
        if all(r == float('inf') for r in ratios):
            return -1
        return np.argmin(ratios)

    def do_pivot(self, pivot_row, pivot_col):
        pivot_element = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row, :] /= pivot_element
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                multiplier = self.tableau[i, pivot_col]
                self.tableau[i, :] -= multiplier * self.tableau[pivot_row, :]

    def display_solution(self):
        """
        Menampilkan hanya nilai variabel keputusan (x1..xn) dan nilai optimal Z.
        """
        optimal_value = self.tableau[-1, -1]
        print(f"\nNilai Optimal Z = {optimal_value:.2f}")

        # Hanya ambil kolom x1..xn
        solution = {}
        for i in range(self.num_decision_vars):
            column_data = self.tableau[:, i]
            if np.sum(column_data == 1) == 1 and np.sum(column_data) == 1:
                row_index = np.where(column_data == 1)[0][0]
                solution[f'x{i+1}'] = self.tableau[row_index, -1]
            else:
                solution[f'x{i+1}'] = 0.0

        print("Solusi Variabel Keputusan:")
        for i in range(self.num_decision_vars):
            print(f"  x{i+1} = {solution[f'x{i+1}']:.2f}")

    def __repr__(self):
        return f"Current Tableau:\n{self.tableau}"
