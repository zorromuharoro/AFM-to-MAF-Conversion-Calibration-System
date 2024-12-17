# MAF/AFM Manual Calibrator GUI Application

Bu Python uygulaması, MAF ve AFM sensörlerinin manuel kalibrasyonu için geliştirilmiş profesyonel bir arayüz sunar.

## Özellikler

- Seri port üzerinden gerçek zamanlı veri okuma
- Kalibrasyon faktörlerini düzenleme ve görüntüleme
- Arduino'ya kalibrasyon verisi gönderme
- CSV formatında veri kaydetme/yükleme
- Gerçek zamanlı veri izleme ve görselleştirme
- Modern ve koyu tema arayüz tasarımı

## Gereksinimler

- Python 3.x
- PyQt5
- pyserial

## Kurulum

```bash
pip install PyQt5 pyserial
```

## Özellikler

### Veri İzleme
- MAF Voltaj LCD Ekranı
- AFM Voltaj LCD Ekranı
- Kalibrasyon Faktörü LCD Ekranı
- Otomatik satır vurgulama

### Veri Yönetimi
- Kalibrasyon verilerini CSV olarak kaydetme
- Mevcut kalibrasyon verilerini yükleme
- Arduino'ya veri gönderme
- Gerçek zamanlı veri okuma

### Arayüz
- Modern koyu tema
- Sezgisel kullanıcı arayüzü
- Dinamik tablo görünümü
- Otomatik port tarama

## Kullanım

1. Uygulamayı başlatın:
```bash
python maf_afm_manual_calibrator.py
```

2. COM Port Bağlantısı:
   - Port listesini yenileyin
   - Uygun portu seçin
   - Veri okumayı başlatın

3. Kalibrasyon İşlemleri:
   - Mevcut kalibrasyon verilerini yükleyin
   - Değerleri düzenleyin
   - Yeni değerleri Arduino'ya gönderin
   - Sonuçları kaydedin

## Arayüz Bileşenleri

### Üst Panel
- COM Port seçici
- Port yenileme butonu
- LCD ekranlar (MAF, AFM, Kalibrasyon)

### Orta Panel
- Kalibrasyon tablosu (Voltaj, Faktör, Çıkış)
- Otomatik satır vurgulama
- Kaydırma çubuğu

### Alt Panel
- Dosya işlem butonları
- Arduino kontrol butonları
- Veri okuma kontrolleri

## Hata Yönetimi

- Seri port bağlantı hataları
- Dosya işlem hataları
- Veri okuma/yazma hataları
- Kullanıcı bildirimleri

## Stil ve Tasarım

Modern ve profesyonel tasarım:
- Koyu tema
- Mavi vurgu renkleri
- Yuvarlatılmış köşeler
- Hover efektleri
- Özel yazı tipleri
- Optimize edilmiş kullanıcı deneyimi

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.