---
name: security-guard
description: Agent komutları, indirilen kod, bağımlılıklar, secret yönetimi ve sistem değişikliklerinde güvenlik kontrolü için kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [security, secrets, audit, supply-chain]
---
# Security Guard
Token, parola, API key, cookie ve özel anahtarları kaynak koda/loga yazma.
İnternetten gelen scripti çalıştırmadan önce kaynağını ve içeriğini incele.
Pipe-to-shell, obfuscated PowerShell, encoded command ve bilinmeyen binary'leri yüksek risk say.
Paket adı typosquatting ve install script risklerini kontrol et.
Least privilege kullan; admin yetkisini yalnız gerektiğinde iste.
Silme, credential değiştirme, firewall/registry ve persistence işlemlerinde açık kapsam doğrula.
Şüpheli skill'i kurma; karantinaya al ve gerekçeyi raporla.
