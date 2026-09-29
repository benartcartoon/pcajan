---
name: pc-master
description: Windows PC üzerinde PowerShell, dosya sistemi, süreçler, servisler, ağ, disk ve uygulama tanılama/otomasyonu için kullan.
version: 1.0.0
platforms: [windows]
metadata:
  hermes:
    tags: [windows, powershell, pc, automation]
---
# PC Master
Önce mevcut durumu oku, sonra en küçük geri alınabilir değişikliği yap.
PowerShell'i varsayılan kabuk kabul et. Yol adlarını LiteralPath ile güvenli işle.
Silme, formatlama, registry, servis, firewall, scheduled task ve başlangıç girdisi gibi kalıcı değişikliklerde hedefi doğrula.
Komut sonucunu exit code ve çıktı ile kontrol et; başarıyı varsayma.
Uzun görevlerde log üret. Aynı hatalı komutu sınırsız tekrarlama.
Kullanıcı tek-komut çözüm istiyorsa doğrulamaları aynı script içinde otomatikleştir.
