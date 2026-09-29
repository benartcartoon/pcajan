---
name: browser-automation
description: Web sitelerinde gezinme, form doldurma, tıklama, veri çıkarma, ekran görüntüsü ve web uygulaması test otomasyonunda kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [browser, automation, testing, scraping]
---
# Browser Automation
Tercih edilen motor mevcutsa agent-browser/Playwright benzeri erişilebilirlik snapshot tabanlı araç kullan.
Her etkileşimden sonra sayfa durumunu yeniden gözlemle; eski selector/ref'e kör güvenme.
Login, ödeme, yayınlama, silme ve gönderme gibi dış etki oluşturan son adımlarda kullanıcı kapsamını doğrula.
CAPTCHA veya güvenlik kontrolünü aşmaya çalışma.
Credential'ları loglama veya dosyaya gömme.
Veri çıkarırken rate limit, robots/ToS ve kişisel veri sınırlarına uy.
