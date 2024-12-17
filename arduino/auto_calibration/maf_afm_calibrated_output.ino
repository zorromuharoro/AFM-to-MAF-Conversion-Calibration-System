#include <Wire.h>
#include <Adafruit_MCP4725.h>

// MAF ve AFM sensörleri için pin tanımlamaları
const int mafPin = A0;

// MCP4725 DAC modülü için I2C adresi
Adafruit_MCP4725 dac;

// Kalibrasyon tablosu
const float refVoltages[] = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.1, 1.2, 1.3, 1.8, 2.1, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.9, 5.0};
const float calibrationFactors[] = {0.00, 0.46, 1.00, 1.11, 0.51, 0.00, 0.00, 1.13, 1.17, 0.29, 0.76, 1.14, 1.16, 0.92, 0.64, 0.99, 0.99, 0.99, 1.06, 1.05, 1.04, 1.04, 1.03, 1.02, 1.01, 1.01, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00};

// Son işlem zamanı
unsigned long previousMillis = 0;
// Gecikme aralığı (milisaniye cinsinden)
const long interval = 65; // 65 ms

void setup() {
    Serial.begin(9600);
    Wire.begin();
    dac.begin(0x62); // MCP4725 başlatma
}

void loop() {
    unsigned long currentMillis = millis(); // Geçerli zamanı al

    // Belirli aralıklarla işlem yap
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis; // Zamanı güncelle

        int mafValue = analogRead(mafPin);
        float mafVoltage = mafValue * (5.0 / 1023.0); // MAF voltajını hesaplama

        float calibrationFactor = getCalibrationFactor(mafVoltage);
        float calibratedVoltage = mafVoltage * calibrationFactor; // Kalibre edilmiş voltajı hesaplama

        // Kalibre edilmiş voltajı DAC'a gönder
        uint16_t dacValue = (uint16_t)(calibratedVoltage * (4095 / 5.0));
        dac.setVoltage(dacValue, false);

        // Seri monitöre orijinal ve kalibre edilmiş voltajları yazdırma
        Serial.print("MAF Voltage: ");
        Serial.print(mafVoltage);
        Serial.print(", Calibrated Voltage: ");
        Serial.print(calibratedVoltage);
        Serial.print(", Calibration Factor: ");
        Serial.println(calibrationFactor); // Kalibrasyon faktörünü yazdır
    }
}

// Kalibrasyon faktörünü bulma fonksiyonu
float getCalibrationFactor(float voltage) {
    int size = sizeof(refVoltages) / sizeof(refVoltages[0]);
    for (int i = size - 1; i >= 0; i--) {
        if (voltage >= refVoltages[i]) {
            return calibrationFactors[i];
        }
    }
    return 1; // Eğer tabloda uygun bir değer bulunamazsa varsayılan olarak 1 döndür
}
