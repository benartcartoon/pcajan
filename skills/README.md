# Hermes Power Skills

Bu klasör Hermes Agent için taşınabilir bir skill tap'idir. Hermes, Agent Skills SKILL.md formatını destekler.

## Kurulum
En kolay yol:
```bash
hermes skills tap add benartcartoon/pcajan
```
Tap yolu sorulursa `skills/` kullan.

Tek tek skill kurulumu destekleniyorsa bu depodaki ilgili `skills/<skill>/SKILL.md` dosyasını kullan.

## Paket
- pc-master: Windows/PowerShell ve yerel PC operasyonları
- coding-engineer: kod yazma, refactor, test ve doğrulama
- github-workflow: branch/commit/PR ve güvenli GitHub akışı
- browser-research: web araştırması ve kaynak doğrulama
- browser-automation: web UI otomasyonu için güvenli çalışma akışı
- debug-doctor: log/hata kök neden analizi
- automation-builder: tekrarlanabilir otomasyonlar ve idempotent scriptler
- security-guard: sırlar, bağımlılıklar ve komut güvenliği
- colab-comfyui: Colab/Drive/ComfyUI operasyonları
- skill-hunter: yeni Hermes skilllerini bulma, inceleme ve güvenli kurma
- self-improve: başarısız görevlerden tekrar kullanılabilir iyileştirme çıkarma

## Güvenlik
Dış skill doğrudan kurulmaz. Önce `hermes skills inspect <kaynak>`, sonra güvenlik kontrolü; şüpheli komut, credential toplama, gizli veri gönderme veya kalıcı sistem değişikliği varsa kullanıcı onayı alınır.
