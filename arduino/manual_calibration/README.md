# MAF/AFM Manual EEPROM Calibration System

Bu proje, MAF sensörü çıkışını AFM sinyaline dönüştüren ve kalibrasyon değerlerini EEPROM'da saklayan bir Arduino sistemidir.

## Özellikler

- MAF sensör voltaj okuma
- Gerçek zamanlı sinyal dönüşümü
- Manuel kalibrasyon sistemi
- EEPROM'da kalibrasyon değerlerini saklama
- MCP4725 DAC modülü ile analog çıkış
- 65ms örnekleme hızı
- Seri port üzerinden kalibrasyon değeri güncelleme

## Donanım Gereksinimleri

- Arduino (herhangi bir model)
- MCP4725 DAC modülü
- MAF sensörü
- Bağlantı kabloları

## Kurulum

1. Arduino IDE'yi açın
2. Gerekli kütüphaneleri yükleyin:
   - Wire.h (Arduino ile birlikte gelir)
   - Adafruit_MCP4725.h
   - EEPROM.h (Arduino ile birlikte gelir)
3. Kodu Arduino'ya yükleyin
4. Bağlantıları yapın:
   - MAF sensörü -> A0 pin
   - MCP4725 -> I2C pinleri (SDA, SCL)

## Kalibrasyon Prosedürü

1. Seri monitörü açın (9600 baud)
2. Her voltaj değeri için kalibrasyon faktörlerini seri port üzerinden gönderin
3. Kalibrasyon faktörleri otomatik olarak EEPROM'a kaydedilecektir
4. Arduino yeniden başlatıldığında kalibrasyon değerleri EEPROM'dan okunacaktır

## Teknik Detaylar

- Örnekleme hızı: 65ms
- ADC çözünürlüğü: 10-bit (0-1023)
- DAC çözünürlüğü: 12-bit (0-4095)
- Voltaj aralığı: 0-5V
- EEPROM kullanımı: ~200 byte

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.