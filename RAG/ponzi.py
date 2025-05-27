import numpy as np
import pandas as pd

# Parametreler
max_kademe = 20
max_kisi_kademede = 5
giris_uretimi = [10_000, 20_000, 40_000, 80_000]  # Her 5 kademede artış
komisyon_yuzdeleri = [0.4, 0.2, 0.1, 0.05, 0.02, 0.01, 0.01]  # 7 kademe için
kazanc_limiti_kat = 3  # Maks 3 kat kazanç

# Kademeye göre giriş ücreti
def giris_ucreti(kademe):
    index = (kademe - 1) // 5
    return giris_uretimi[min(index, len(giris_uretimi)-1)]

# Kişi sayısı (her kademe 2 kat kişi ama max 5 kişi sınırı)
def kisi_sayisi(kademe):
    return min(2**(kademe-1), max_kisi_kademede)

# Kazanç hesaplama
def kademe_komisyon(kademe_uzaklik):
    if kademe_uzaklik < len(komisyon_yuzdeleri):
        return komisyon_yuzdeleri[kademe_uzaklik]
    else:
        return 0

# Simülasyon
kademe_list = []
kisi_list = []
giris_list = []
kazanc_list = []

# Her kademe için kişinin kazancı ve toplam kazanç
kazanc_kisi = np.zeros(max_kademe)
giren_kisi = np.zeros(max_kademe)

for kademe in range(1, max_kademe+1):
    kisi = kisi_sayisi(kademe)
    giren_kisi[kademe-1] = kisi
    giris = kisi * giris_ucreti(kademe)
    
    # Kazanç kişi başı hesapla
    kazanc_toplam = 0
    for kd_uzaklik in range(1, len(komisyon_yuzdeleri)+1):
        k_uzak = kademe + kd_uzaklik
        if k_uzak > max_kademe:
            break
        kisi_alt = kisi_sayisi(k_uzak)
        komisyon_oran = kademe_komisyon(k_uzak-1)
        ucret_alt = giris_ucreti(k_uzak)
        kazanc_toplam += kisi * kisi_alt * komisyon_oran * ucret_alt
    
    # Kazanç limiti uygula (max 3 kat giriş ücreti)
    max_kazanc = giris_ucreti(kademe) * kazanc_limiti_kat
    kazanc_toplam = min(kazanc_toplam, max_kazanc * kisi)
    kazanc_kisi[kademe-1] = kazanc_toplam / kisi
    kademe_list.append(kademe)
    kisi_list.append(kisi)
    giris_list.append(giris)
    kazanc_list.append(kazanc_toplam)

# Sonuç DataFrame
df = pd.DataFrame({
    "Kademe": kademe_list,
    "Kişi Sayısı": kisi_list,
    "Toplam Giriş (₺)": giris_list,
    "Toplam Kazanç (₺)": kazanc_list,
    "Kişi Başı Kazanç (₺)": kazanc_list / np.array(kisi_list)
})

df
