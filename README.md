# 🎛️ El Hareketiyle Ses Kontrolü

Bu Python projesi, bilgisayarınızın ses seviyesini el hareketleriyle kontrol etmenizi sağlar. Kamera aracılığıyla elinizi algılar ve parmak sayınıza ve hareketlerinize göre ses seviyesini ayarlar.

---

## 📌 Özellikler

- ✋ **El Algılama**: Mediapipe ile gerçek zamanlı el takibi.
- 🖐️ **Parmak Sayısı Algılama**: Açık parmak sayısına göre işlem yapılır.
- 🔊 **Ses Kontrolü**:
  - Üç parmak gösterildiğinde ses kontrolü aktifleşir.
  - Başparmak ve işaret parmağı arasındaki mesafe ses seviyesini belirler.
- 👁️ **Görsel Geri Bildirim**:
  - Algılanan el ve parmaklar ekranda işaretlenir.
  - Anlık FPS bilgisi gösterilir.
  - Ses kontrolü durumu ve mevcut ses düzeyi ekrana yazdırılır.
  - Başparmak ve işaret parmağı arasına çizgi ve daire çizilir.
---
## 🚀 Nasıl Çalıştırılır?

- Üç parmağınızı göstererek ses kontrolünü aktif hale getirin.
-	Başparmak ve işaret parmağı arasındaki mesafeyi değiştirerek sesi ayarlayın.
- q tuşuna basarak programdan çıkabilirsiniz.
---
## ⚠️ Notlar

-	Bu proje macOS işletim sistemi için tasarlanmıştır (osascript komutu kullanılır).
-	Windows veya Linux kullanıcıları, sistem sesini değiştirmek için farklı komutlar veya kütüphaneler kullanmalıdır.
-	pyaudio sadece import edilmiştir, aktif olarak kullanılmaz.
---
## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|----------|----------|
| Python   | Ana programlama dili |
| OpenCV (`cv2`) | Görüntü işleme ve kamera erişimi |
| Mediapipe | El takibi için Google ML çözümü |
| PyAudio (opsiyonel) | Ses işleme kütüphanesi (bu projede doğrudan kullanılmaz) |
| OS & Time | Sistem komutları ve zaman hesaplamaları için |

---

## 🔧 Kurulum

Aşağıdaki komutlarla gerekli kütüphaneleri kurabilirsiniz:

```bash
pip install opencv-python mediapipe pyaudio
