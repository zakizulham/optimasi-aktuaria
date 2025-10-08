import numpy as np

class SimplexSolver:
    """
    Sebuah class untuk menyelesaikan masalah program linier
    menggunakan algoritma simpleks.
    """
    def __init__(self, tableau):
        """
        Inisialisasi solver dengan tabel simpleks awal.

        Args:
            tableau (np.array): Matriks yang merepresentasikan masalah LP.
                                  Baris terakhir adalah fungsi tujuan.
        """
        self.tableau = np.array(tableau, dtype=float)

    def solve(self):
        """
        Fungsi utama untuk menjalankan iterasi algoritma simpleks.
        """
        # Batasi jumlah iterasi untuk mencegah infinite loop
        max_iterations = 100
        iteration = 0

        while not self.is_optimal() and iteration < max_iterations:
            print(f"\n--- Iterasi ke-{iteration + 1} ---")
            
            pivot_col = self.find_pivot_column()
            print(f"Kolom Pivot: {pivot_col}")

            pivot_row = self.find_pivot_row(pivot_col)
            # Jika tidak ada baris pivot yang valid, solusi tidak terbatas (unbounded)
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
        """
        Mengecek apakah kondisi optimal sudah tercapai.
        Kondisi optimal tercapai jika semua koefisien di baris fungsi tujuan
        (baris terakhir) bernilai non-negatif (>= 0).
        """
        objective_row = self.tableau[-1, :-1] # Semua kolom kecuali kolom solusi
        return np.all(objective_row >= 0)

    def find_pivot_column(self):
        """
        Mencari kolom pivot, yaitu kolom dengan nilai paling negatif
        di baris fungsi tujuan.
        """
        objective_row = self.tableau[-1, :-1]
        return np.argmin(objective_row)

    def find_pivot_row(self, pivot_col):
        """
        Mencari baris pivot dengan menghitung rasio terkecil.
        Rasio = Solusi / Elemen di kolom pivot
        Hanya baris dengan elemen pivot > 0 yang dipertimbangkan.
        """
        ratios = []
        # Iterasi semua baris kecuali baris fungsi tujuan
        for i, row in enumerate(self.tableau[:-1, :]):
            element = row[pivot_col]
            if element > 0:
                ratio = row[-1] / element
                ratios.append(ratio)
            else:
                # Rasio tidak valid untuk elemen non-positif
                ratios.append(float('inf'))
        
        # Jika semua rasio tidak valid, solusi unbounded
        if all(r == float('inf') for r in ratios):
            return -1

        return np.argmin(ratios)

    def do_pivot(self, pivot_row, pivot_col):
        """
        Melakukan operasi baris elementer (pivot) untuk memperbarui tabel.
        """
        # 1. Jadikan elemen pivot menjadi 1
        pivot_element = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row, :] /= pivot_element
        
        # 2. Jadikan elemen lain di kolom pivot menjadi 0
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                multiplier = self.tableau[i, pivot_col]
                self.tableau[i, :] -= multiplier * self.tableau[pivot_row, :]
                
    def display_solution(self):
        """
        Menampilkan solusi akhir dari tabel.
        """
        # Nilai Z optimal ada di pojok kanan bawah
        optimal_value = self.tableau[-1, -1]
        print(f"\nNilai Optimal Z = {optimal_value:.2f}")

        # Variabel basis dan nilainya
        num_vars = self.tableau.shape[1] - self.tableau.shape[0] 
        solution = {}
        for col in range(num_vars):
            column_data = self.tableau[:, col]
            # Variabel basis adalah kolom yg punya satu angka 1 dan sisanya 0
            if np.sum(column_data) == 1 and len(column_data[column_data == 1]) == 1:
                row_index = np.where(column_data == 1)[0][0]
                solution[f'x{col+1}'] = self.tableau[row_index, -1]

        print("Solusi Variabel Keputusan:")
        for i in range(num_vars):
             # Jika variabel tidak ada di basis, nilainya 0
            value = solution.get(f'x{i+1}', 0)
            print(f"  x{i+1} = {value:.2f}")