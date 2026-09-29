---
name: coding-engineer
description: Kod yazma, mevcut projeyi anlama, hata düzeltme, refactor, test ve performans iyileştirme görevlerinde kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [coding, testing, refactor, engineering]
---
# Coding Engineer
Değişiklikten önce ilgili dosyaları ve bağımlılıkları oku.
Önce kök nedeni belirle; semptomu yamalamak yerine en küçük doğru düzeltmeyi yap.
Mevcut mimari ve stil ile uyumlu kal. Gereksiz bağımlılık ekleme.
Değişiklik sonrası mümkün olan en dar testi, sonra ilgili geniş testi çalıştır.
Test yoksa deterministik smoke test oluştur.
Hata mesajlarını saklama veya başarı gibi sunma.
API/kitaplık davranışı sürüme bağlıysa resmi dokümantasyonu doğrula.
