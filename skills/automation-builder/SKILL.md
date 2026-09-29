---
name: automation-builder
description: Tek komutlu kurulumlar, watcher, scheduler, pipeline ve güvenilir tekrar çalıştırılabilir otomasyonlar oluşturmak için kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [automation, pipeline, scripts, reliability]
---
# Automation Builder
Kullanıcı için mümkün olan en az manuel adımı hedefle.
Scriptleri idempotent yap: ikinci çalıştırma sistemi bozmamalı.
Ön koşulları otomatik kontrol et; eksikleri anlaşılır hata ile bildir.
Uzun görevlerde checkpoint/resume ve log kullan.
Network/indirme işlemlerinde timeout ve sınırlı retry uygula.
Başarılı çıktı oluşmadan sonraki aşamaya geçme.
Maliyetli GPU/bulut kaynağını yalnız gerektiğinde başlat ve iş bitince kapatma seçeneği sun.
