# MAF/AFM Kalibrasyon Sistemi

Bu proje, araçlardaki MAF (Mass Air Flow) sensörlerinin çıkış sinyallerini AFM (Air Flow Meter) sinyallerine dönüştüren kapsamlı bir kalibrasyon sistemidir.

## Attribution Requirements
This project requires mandatory attribution. Any use, modification, or distribution 
of this software must include clear credit to the original author:
Muharrem Şişli (@zorromuharoro on GitHub - https://github.com/zorromuharoro)

## Proje Yapısı

```
├── arduino/
│   ├── auto_calibration/     # Otomatik kalibrasyon Arduino kodu
│   ├── data_collection/      # Veri toplama Arduino kodu
│   └── manual_calibration/   # Manuel kalibrasyon Arduino kodu
│
└── python/
    ├── auto_calibrator/      # Otomatik kalibrasyon GUI uygulaması
    └── manual_calibrator/    # Manuel kalibrasyon GUI uygulaması
```

## Arduino Projeleri

### Auto Calibration
- Önceden tanımlanmış kalibrasyon tablosu kullanır
- MCP4725 DAC modülü ile analog çıkış sağlar
- 65ms örnekleme hızı ile gerçek zamanlı çalışır

### Data Collection
- MAF ve AFM sensörlerinden eşzamanlı veri toplar
- CSV formatında veri çıkışı sağlar
- Kalibrasyon analizi için veri seti oluşturur

### Manual Calibration
- EEPROM'da kalibrasyon verilerini saklar
- Seri port üzerinden kalibrasyon güncelleme
- MCP4725 DAC modülü ile analog çıkış

## Python Uygulamaları

### Auto Calibrator
- Gerçek zamanlı veri görselleştirme
- Otomatik kalibrasyon faktörü hesaplama
- Matplotlib ve PyQtGraph grafikleri
- Modern GUI arayüzü

### Manual Calibrator
- Manuel kalibrasyon değeri düzenleme
- Arduino'ya kalibrasyon verisi gönderme
- Gerçek zamanlı veri izleme
- Koyu tema modern arayüz

## Gereksinimler

### Arduino
- Arduino IDE
- Wire.h kütüphanesi
- Adafruit_MCP4725 kütüphanesi
- EEPROM kütüphanesi

### Python
- Python 3.x
- PyQt5
- pyserial
- numpy
- matplotlib
- pyqtgraph

## Kurulum

1. Arduino kurulumu:
```bash
# Arduino IDE'den kütüphaneleri yükleyin
- Adafruit MCP4725
```

2. Python kurulumu:
```bash
pip install PyQt5 pyserial numpy matplotlib pyqtgraph
```

## Başlarken

1. Donanım bağlantılarını yapın:
   - MAF sensörü -> Arduino A0 pin
   - MCP4725 -> Arduino I2C pinleri
   - AFM bağlantısı -> MCP4725 çıkışı

2. Arduino kodunu yükleyin:
   - Otomatik kalibrasyon için auto_calibration
   - Manuel kalibrasyon için manual_calibration
   - Veri toplamak için data_collection

3. Python uygulamasını başlatın:
   - Otomatik kalibrasyon için auto_calibrator
   - Manuel kalibrasyon için manual_calibrator
   
## Note:

This project is still a work in progress. Some documentation and schematics may be missing. However, the core functionality is operational and usable.

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Özellik branchı oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'ı push edin (`git push origin feature/AmazingFeature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje GNU General Public License v3 (GPL-3.0) lisansı altında lisanslanmıştır ve zorunlu atıf gerektirmektedir. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
