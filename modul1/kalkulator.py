import penambahan
import pengurangan
import perkalian
import pembagian

print("=== Program Kalkulator Modular ===")
a = int(input("Masukkan angka pertama : "))
b = int(input("Masukkan angka kedua  : "))

print(f"Penambahan dari {a} dan {b} adalah {penambahan.tambah(a, b)}")
print(f"Pengurangan dari {a} dan {b} adalah {pengurangan.kurang(a, b)}")
print(f"Perkalian dari {a} dan {b} adalah {perkalian.kali(a, b)}")
print(f"Pembagian dari {a} dan {b} adalah {pembagian.bagi(a, b)}")
