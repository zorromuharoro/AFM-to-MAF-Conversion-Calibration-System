# MAF/AFM Auto Calibrator GUI Application

Bu Python uygulaması, MAF ve AFM sensörlerinin kalibrasyonu için geliştirilmiş kullanıcı dostu bir arayüz sunar.

## Özellikler

- Gerçek zamanlı veri okuma ve görselleştirme
- Otomatik kalibrasyon faktörü hesaplama
- Ayarlanabilir örnekleme hızı (0ms, 10ms, 50ms, 100ms)
- Kalibrasyon tablosu boyutu seçenekleri (25, 50, 75, 100 nokta)
- Matplotlib ve PyQtGraph ile gelişmiş grafik görselleştirme
- CSV formatında kalibrasyon verisi kaydetme/yükleme
- Modern ve kullanıcı dostu arayüz tasarımı
- Hata loglama sistemi

## Gereksinimler

- Python 3.x
- PyQt5
- pyserial
- numpy
- pyqtgraph
- matplotlib

## Kurulum

```bash
pip install PyQt5 pyserial numpy pyqtgraph matplotlib
```

## Kullanım

1. Uygulamayı başlatın:
```bash
python maf_afm_auto_calibrator.py
```

2. Seri port bağlantısı:
   - COM portunu seçin
   - Örnekleme hızını ayarlayın
   - "Başlat" butonuna tıklayın

3. Kalibrasyon:
   - Tablo boyutunu seçin (25-100 arası)
   - MAF ve AFM değerlerini gerçek zamanlı izleyin
   - Kalibrasyon faktörleri otomatik hesaplanır
   - Grafikleri analiz edin

4. Veri Yönetimi:
   - Kalibrasyon tablosunu CSV olarak kaydedin
   - Önceki kalibrasyon verilerini yükleyin

## Arayüz Bileşenleri

- Port Seçici: Mevcut COM portlarını listeler
- Gecikme Seçici: Örnekleme hızını ayarlar
- Kalibrasyon Tablosu: Voltaj/faktör değerlerini gösterir
- LCD Ekranlar: Anlık MAF/AFM değerlerini gösterir
- Grafik Panelleri: Veri trendlerini görselleştirir

## Hata Yönetimi

- Seri port hataları
- Veri okuma/yazma hataları
- Uygulama başlatma hataları
- Tüm hatalar "hata.log" dosyasına kaydedilir

## Stil ve Tasarım

Uygulama, özel CSS stil dosyası ile modern bir görünüm sunar:
- Koyu gri tema
- Yuvarlatılmış köşeler
- Hover efektleri
- Tutarlı renk paleti
- Profesyonel font seçimi

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.