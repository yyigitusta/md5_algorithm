A = 0x01234567
B = 0x89abcdef
C = 0xfedcba98
D = 0x76543210
sonuc = []
T = [
    i for i in range(1, 65)  # T1'den T64'e kadar liste oluşturuluyor
]

def slice512to32(parca):
    return [parca[i:i+32] for i in range(0, len(parca), 32)]

def f_func(B, C, D):
    return (B & C) | (~B & D)

def g_func(B, C, D):
    return (B & D) | (C & ~D)

def h_func(B, C, D):
    return B ^ C ^ D

def i_func(B, C, D):
    return C ^ (B | ~D)

def eldesiz_toplama(a, b):
    while b != 0:
        toplam = a ^ b
        tasma = (a & b) << 1
        a = toplam
        b = tasma
    return a

def left_rotate(n, d):
    bit_size = 32
    d %= bit_size
    left_shifted = (n << d) & ((1 << bit_size) - 1)
    right_shifted = n >> (bit_size - d)
    return left_shifted | right_shifted

def algoritma(A, B, C, D, parcalar):
    parca_sayisi = len(parcalar)
    for i in range(parca_sayisi):
        boxtobox = slice512to32(parcalar[i])
        for j in range(64):  # 64 işlem
            if 0 <= j < 16:
                result = f_func(B, C, D)
                s = [7, 12, 17, 22][j % 4]
            elif 16 <= j < 32:
                result = g_func(B, C, D)
                s = [5, 9, 14, 20][j % 4]
            elif 32 <= j < 48:
                result = h_func(B, C, D)
                s = [4, 11, 16, 23][j % 4]
            else:
                result = i_func(B, C, D)
                s = [6, 10, 15, 21][j % 4]

            temp = eldesiz_toplama(A, result)
            temp = eldesiz_toplama(temp, int(boxtobox[j % 16], 2))  # Boxtobox elemanı 32 bitlik olmalı
            temp = eldesiz_toplama(temp, T[j])
            temp = left_rotate(temp, s)
            temp = eldesiz_toplama(temp, B)

            A, D, C, B = D, C, B, temp  # Dönüşüm

        sonuc.extend([A, B, C, D])

def string_to_bits(string):
    return ''.join(format(ord(c), '08b') for c in string)

def ayir_512_bit_dize(string):
    bit_dizisi = string_to_bits(string)
    parcalar = [bit_dizisi[i:i+512] for i in range(0, len(bit_dizisi), 512)]
    if len(parcalar[-1]) < 512:
        kalan = 512 - len(parcalar[-1])
        parcalar[-1] += '0' * kalan
    return parcalar

def main():
    sifrelenecakMesaj = (
        "Sabahin erken saatlerinde ormansdan derinliklerinde huzur dolu bir sessizlik vardads. "
        "Gün doğumunun altin sarisi işiklarsad, ağaçlardasn arassadndan süzülerek yeryüzüne iniyor "
        "ve çiğ tanelerinin üzerinde parlayan minik mücevherler yaratadsyordu."
    )
    parcalar = ayir_512_bit_dize(sifrelenecakMesaj)
    algoritma(A, B, C, D, parcalar)
    print("Sonuç:", sonuc)

if __name__ == "__main__":
    main()

