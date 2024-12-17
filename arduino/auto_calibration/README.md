# MAF/AFM Auto Calibration System

Bu proje, araç MAF (Mass Air Flow) sensörünün çıkış sinyalini AFM (Air Flow Meter) sinyaline dönüştüren ve otomatik kalibrasyon yapan bir Arduino sistemidir.

## Özellikler

- MAF sensör voltaj okuma
- Gerçek zamanlı sinyal dönüşümü
- Otomatik kalibrasyon sistemi
- MCP4725 DAC modülü ile analog çıkış
- 65ms örnekleme hızı
- Seri port üzerinden veri izleme

## Donanım Gereksinimleri

- Arduino (herhangi bir model)
- MCP4725 DAC modülü
- MAF sensörü
- Bağlantı kabloları

## Kurulum

1. Arduino IDE'yi açın
2. Gerekli kütüphaneleri yükleyin:
   - Wire.h (Arduino ile birlikte gelir)
   - Adafruit_MCP4725.h (Arduino Library Manager'dan yükleyebilirsiniz)
3. Kodu Arduino'ya yükleyin
4. Bağlantıları yapın:
   - MAF sensörü -> A0 pin
   - MCP4725 -> I2C pinleri (SDA, SCL)

## Kalibrasyon Tablosu

Kod içerisinde önceden tanımlanmış kalibrasyon tablosu bulunmaktadır. Bu tablo, farklı MAF voltaj değerleri için uygun kalibrasyon faktörlerini içerir.

## Kullanım

1. Sistemi çalıştırın
2. Serial Monitor'ü açın (9600 baud)
3. MAF voltajı, kalibre edilmiş voltaj ve kalibrasyon faktörü değerlerini izleyin

## Teknik Detaylar

- Örnekleme hızı: 65ms
- ADC çözünürlüğü: 10-bit (0-1023)
- DAC çözünürlüğü: 12-bit (0-4095)
- Voltaj aralığı: 0-5V

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
