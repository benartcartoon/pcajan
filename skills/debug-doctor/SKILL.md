---
name: debug-doctor
description: Stack trace, log, servis çökmesi, bağlantı hatası, dependency ve performans problemlerinin kök nedenini bulmak için kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [debug, logs, diagnostics, troubleshooting]
---
# Debug Doctor
Önce hatayı aynen yakala: komut, exit code, stack trace, ortam ve sürümler.
Hipotezleri kanıttan ayır. En olası hipotezi en ucuz testle doğrula.
Port/process sorunlarında servis gerçekten çalışıyor mu kontrol et.
Dependency sorunlarında kurulu sürüm, Python/Node ortamı, CUDA/driver uyumunu doğrula.
Düzeltmeden sonra ilk hatayı üreten komutu yeniden çalıştır.
Geçici workaround ile kalıcı çözümü ayrı raporla.
