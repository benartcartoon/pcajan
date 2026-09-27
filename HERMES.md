# Hermes çalışma kuralları — pcajan

Bu depo otomasyon ajanının kodları içindir. Kullanıcı görevleri önce bilgisayarından, daha sonra Telegram üzerinden verir.

## Görev akışı
1. Görevi, kapsamını ve ilgili dosyaları belirle; mevcut dosyaları okumadan değiştirme.
2. Kod değişikliklerini bu depoda yap. Her görev için ayrı `hermes/<kisa-gorev-adi>` dalı aç.
3. İlgili kontrolleri çalıştır, çıktılarını özetle. Başarısızlığı başarılı diye raporlama.
4. Değişiklikleri kendi dalına commit ve push et; GitHub'da PR açıp bağlantıyı kullanıcıya bildir.
5. Raporunda değişen dosyalar, test sonucu, kalan sorunlar ve PR bağlantısı bulunsun.
6. Ana dala doğrudan push etme; PR birleştirmeyi kullanıcı onayına bırak.

**Kullanıcı belirli bir PR numarası vererek açıkça "PR #... birleştir" demedikçe hiçbir PR'ı birleştirme. "PR oluştur, birleştirme" görevinde PR açıldıktan sonra dur ve GitHub'dan doğruladığın açık durumunu raporla.**

## Sınırlar
- GitHub kimlik bilgilerini, API anahtarlarını, Telegram tokenlarını, Drive erişim bilgilerini ve yerel sırları kodda veya loglarda tutma.
- Büyük modelleri, videoları ve geçici dosyaları GitHub'a yükleme; Drive'da sakla.
- Google Cloud ücretli hizmetlerini, Colab GPU'yu veya dış sistemlerde maliyet doğuran işlemleri yalnızca ilgili görevin açık kapsamıyla kullan.
- Colab oturumunun kapalıyken kendiliğinden başlayacağını varsayma.
- Hata durumunda yapılan adımları ve son hatayı açıkça raporla; aynı başarısız işi sınırsız tekrar etme.

## Proje yolları
- GitHub: benartcartoon/pcajan
- Drive ana klasör: /content/drive/MyDrive/MiniMax-H3
- Colab ComfyUI: /content/drive/MyDrive/MiniMax-H3/ComfyUI
- ComfyUI portu: 8188

Bu yollar Colab oturumu içinde geçerlidir. Windows'ta çalışırken Drive'ın yerel yolu ayrıca belirlenmelidir.
