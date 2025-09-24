# Program Biodata + Hitung Luas Persegi Panjang

nama = input("Masukkan nama kamu: ")
umur = int(input("Masukkan umur kamu: "))

print("\n=== HASIL BIODATA ===")
print(f"Halo {nama}, umur kamu {umur} tahun")

print("\nSekarang kita hitung luas persegi panjang!")
panjang = float(input("Masukkan panjang: "))
lebar = float(input("Masukkan lebar  : "))

luas = panjang * lebar

print("\n=== HASIL PERHITUNGAN ===")
print(f"Luas persegi panjang = {panjang} x {lebar} = {luas}")
