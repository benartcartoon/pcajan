# pcajan

## Proje Amacı

pcajan, kullanıcı tarafından verilen görevleri otomatik olarak yerine getiren bir yazılım ajanıdır. Görevler önce kullanıcının bilgisayarından, ardından Telegram üzerinden iletilir. Her görev için ayrı bir `hermes/<kisa-gorev-adi>` dalı açılır ve değişiklikler PR (Pull Request) üzerinden ana dala birleştirilir — doğrudan push yapılmaz, birleştirme kullanıcı onayına bırakılır.

Ajanın temel prensipleri:
- Mevcut dosyaları okumadan değiştirme
- Kod değişikliklerini depoda yap, kontrolleri çalıştır
- Başarısızliği başarılı olarak raporlama
- Değişiklikleri kendi dalına commit/push, PR açıp bağlantıyı bildir
- Ana dala doğrudan push etme; PR birleştirmeyi kullanıcı onayına bırak