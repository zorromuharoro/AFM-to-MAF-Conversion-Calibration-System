# MAF/AFM Data Collection System

Bu Arduino projesi, MAF (Mass Air Flow) ve AFM (Air Flow Meter) sensörlerinden veri toplayan basit bir veri toplama sistemidir.

## Özellikler

- MAF ve AFM sensörlerinden eşzamanlı veri okuma
- Analog voltaj değerlerini dijital formata dönüştürme
- Seri port üzerinden CSV formatında veri gönderme
- Yüksek örnekleme hızı

## Donanım Gereksinimleri

- Arduino (herhangi bir model)
- MAF sensörü
- AFM sensörü
- Bağlantı kabloları

## Bağlantılar

- MAF sensörü -> A0 pin
- AFM sensörü -> A1 pin

## Kullanım

1. Arduino'ya kodu yükleyin
2. Seri portu 9600 baud hızında açın
3. Verileri CSV formatında alın (MAF_Voltage,AFM_Voltage)
4. Gelen verileri analiz için kaydedin

## Veri Formatı

Seri porttan gelen veriler şu formattadır:
```
MAF_Voltage,AFM_Voltage
```
Örnek:
```
2.5,3.2
2.6,3.3
2.7,3.4
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.