---
name: colab-comfyui
description: Google Colab, Drive, CUDA GPU, ComfyUI ve büyük AI model workflow kurulum/çalıştırma/hata ayıklama görevlerinde kullan.
version: 1.0.0
metadata:
  hermes:
    tags: [colab, comfyui, cuda, drive, ai]
---
# Colab + ComfyUI
Önce GPU, VRAM, CUDA, PyTorch ve disk/Drive mount durumunu doğrula.
Büyük modeli yeniden indirmeden önce Drive'daki mevcut dosyayı boyut/hash ile kontrol et.
CPU ile yapılabilen indirme/hazırlığı GPU zamanından ayır.
ComfyUI API çağrısından önce portun dinlediğini ve /queue erişimini doğrula.
Workflow node/model yollarını mevcut kurulumdan keşfet; tahmin etme.
OOM'da önce çözünürlük, frame/batch ve precision ayarlarını kontrollü düşür.
Çıktıyı Drive'a atomik şekilde kaydet ve gerçekten oluştuğunu doğrula.
