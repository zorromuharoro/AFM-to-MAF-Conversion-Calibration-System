import sys
import re
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTableWidgetItem, 
    QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, 
    QLCDNumber, QTableWidget, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

class VoltageCalibrationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voltaj ve Kalibrasyon Faktörü Düzenleyici")
        self.setGeometry(100, 100, 800, 600)
        
        # Serial port ve timer değişkenleri
        self.serial_port = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
        
        try:
            with open("oto_calibrator.css", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("CSS dosyası bulunamadı!")

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # COM port seçimi
        port_layout = QHBoxLayout()
        port_label = QLabel("COM Port:")
        self.port_combo = QComboBox()
        self.port_combo.addItem("COM Portu Seçin")
        self.refresh_ports()
        
        refresh_button = QPushButton("Portları Yenile")
        refresh_button.clicked.connect(self.refresh_ports)
        
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(refresh_button)
        layout.addLayout(port_layout)

        # LCD ekranlar ve etiketleri
        lcd_layout = QHBoxLayout()
        
        maf_layout = QVBoxLayout()
        maf_label = QLabel("MAF Voltaj:")
        self.mafVoltageLCD = QLCDNumber()
        self.mafVoltageLCD.setSegmentStyle(QLCDNumber.Flat)
        self.mafVoltageLCD.setDigitCount(6)
        maf_layout.addWidget(maf_label)
        maf_layout.addWidget(self.mafVoltageLCD)
        
        afm_layout = QVBoxLayout()
        afm_label = QLabel("AFM Voltaj:")
        self.afmVoltageLCD = QLCDNumber()
        self.afmVoltageLCD.setSegmentStyle(QLCDNumber.Flat)
        self.afmVoltageLCD.setDigitCount(6)
        afm_layout.addWidget(afm_label)
        afm_layout.addWidget(self.afmVoltageLCD)
        
        cal_layout = QVBoxLayout()
        cal_label = QLabel("Kalibrasyon Faktörü:")
        self.calibrationFactorLCD = QLCDNumber()
        self.calibrationFactorLCD.setSegmentStyle(QLCDNumber.Flat)
        self.calibrationFactorLCD.setDigitCount(6)
        cal_layout.addWidget(cal_label)
        cal_layout.addWidget(self.calibrationFactorLCD)

        lcd_layout.addLayout(maf_layout)
        lcd_layout.addLayout(afm_layout)
        lcd_layout.addLayout(cal_layout)
        layout.addLayout(lcd_layout)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Voltaj", "Kalibrasyon Faktörü", "Çıktı Voltajı"])
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Düğmeler
        self.create_buttons(layout)
        
        self.highlighted_row = -1
        self.stop_reading = False

    def create_buttons(self, layout):
        button_layout = QHBoxLayout()
        
        buttons = [
            ("Dosya Aç", self.open_file),
            ("Kalibrasyon Faktörlerini Arduino'ya Gönder", self.write_calibration_to_arduino),
            ("Kalibrasyon Faktörlerini Kaydet", self.save_calibration_file),
            ("Arduino'dan Veri Oku", self.start_reading_data),
            ("Veri Okumayı Durdur", self.stop_reading_data)
        ]
        
        for text, callback in buttons:
            button = QPushButton(text)
            button.clicked.connect(callback)
            button_layout.addWidget(button)
            
        layout.addLayout(button_layout)

    def refresh_ports(self):
        self.port_combo.clear()
        self.port_combo.addItem("COM Portu Seçin")
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo.addItems(ports)

    def extract_values(self, content, variable_name):
        try:
            pattern = fr"{variable_name}\[\] = \{{(.*?)\}};"
            match = re.search(pattern, content)
            if match:
                values_str = match.group(1)
                values = [float(value) for value in values_str.split(", ")]
                return values
            return []
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Değer çıkarma hatası: {str(e)}")
            return []

    def update_table(self, voltages, factors):
        try:
            self.table.setRowCount(len(voltages))
            for i in range(len(voltages)):
                voltage_item = QTableWidgetItem(f"{voltages[i]:.3f}")
                factor_item = QTableWidgetItem(f"{factors[i]:.3f}")
                output_voltage = voltages[i] * factors[i]
                output_item = QTableWidgetItem(f"{output_voltage:.3f}")

                # Sadece sayısal değerleri sağa hizala
                voltage_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                factor_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                output_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                self.table.setItem(i, 0, voltage_item)
                self.table.setItem(i, 1, factor_item)
                self.table.setItem(i, 2, output_item)

            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Tablo güncelleme hatası: {str(e)}")

    def open_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "CSV Files (*.csv)")
            if file_path:
                with open(file_path, 'r') as file:
                    content = file.read()
                    refVoltages = self.extract_values(content, "refVoltages")
                    calibrationFactors = self.extract_values(content, "calibrationFactors")
                    if refVoltages and calibrationFactors:
                        if len(refVoltages) == len(calibrationFactors):
                            self.update_table(refVoltages, calibrationFactors)
                        else:
                            QMessageBox.warning(self, "Hata", "Voltaj ve kalibrasyon faktörü sayıları eşleşmiyor!")
                    else:
                        QMessageBox.warning(self, "Hata", "Dosya formatı uygun değil!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya açma hatası: {str(e)}")

    def write_calibration_to_arduino(self):
        com_port = self.port_combo.currentText()
        if com_port == "COM Portu Seçin":
            QMessageBox.warning(self, "Uyarı", "Lütfen bir COM portu seçin!")
            return

        try:
            if self.table.rowCount() == 0:
                QMessageBox.warning(self, "Uyarı", "Gönderilecek kalibrasyon faktörü bulunamadı!")
                return

            ser = serial.Serial(com_port, 9600, timeout=1)
            
            # Arduino'ya veri gönderme başlangıç sinyali
            ser.write(b'START\n')
            
            # Kalibrasyon faktörlerini gönder
            for row in range(self.table.rowCount()):
                factor_item = self.table.item(row, 1)
                factor = factor_item.text() + '\n'
                ser.write(factor.encode('utf-8'))
                
            # Arduino'ya veri gönderme bitiş sinyali
            ser.write(b'END\n')
            
            ser.close()
            QMessageBox.information(self, "Başarılı", "Kalibrasyon faktörleri Arduino'ya gönderildi!")
        except serial.SerialException as e:
            QMessageBox.critical(self, "Hata", f"Seri port hatası: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri gönderme hatası: {str(e)}")

    def save_calibration_file(self):
        try:
            if self.table.rowCount() == 0:
                QMessageBox.warning(self, "Uyarı", "Kaydedilecek kalibrasyon faktörü bulunamadı!")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Kalibrasyon Faktörlerini Kaydet",
                "",
                "CSV Files (*.csv)"
            )
            
            if file_path:
                with open(file_path, 'w') as file:
                    # Voltaj değerlerini yaz
                    file.write("refVoltages[] = {")
                    voltages = []
                    for i in range(self.table.rowCount()):
                        voltage_item = self.table.item(i, 0)
                        voltages.append(voltage_item.text())
                    file.write(", ".join(voltages))
                    file.write("};\n\n")

                    # Kalibrasyon faktörlerini yaz
                    file.write("calibrationFactors[] = {")
                    factors = []
                    for i in range(self.table.rowCount()):
                        factor_item = self.table.item(i, 1)
                        factors.append(factor_item.text())
                    file.write(", ".join(factors))
                    file.write("};")

                QMessageBox.information(self, "Başarılı", "Kalibrasyon faktörleri kaydedildi!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kaydetme hatası: {str(e)}")

    def find_nearest_voltage(self, maf_voltage):
        try:
            voltages = []
            for row in range(self.table.rowCount()):
                voltage_item = self.table.item(row, 0)
                if voltage_item:
                    voltages.append(float(voltage_item.text()))
            
            if not voltages:
                return -1

            return min(range(len(voltages)), key=lambda i: abs(voltages[i] - maf_voltage))
        except Exception as e:
            print(f"En yakın voltaj bulma hatası: {str(e)}")
            return -1

    def highlight_row(self, row):
        if 0 <= row < self.table.rowCount():
            highlight_color = QColor(255, 255, 0, 100)  # Yarı saydam sarı
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(highlight_color)

    def reset_row_color(self, row):
        if 0 <= row < self.table.rowCount():
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor(0, 0, 0, 0))  # Şeffaf arka plan

    def start_reading_data(self):
        com_port = self.port_combo.currentText()
        if com_port == "COM Portu Seçin":
            QMessageBox.warning(self, "Uyarı", "Lütfen bir COM portu seçin!")
            return
            
        try:
            self.serial_port = serial.Serial(com_port, 9600, timeout=1)
            self.stop_reading = False
            self.timer.start(100)  # 100ms aralıklarla veri oku
            QMessageBox.information(self, "Bilgi", "Veri okuma başlatıldı")
        except serial.SerialException as e:
            QMessageBox.critical(self, "Hata", f"Seri port hatası: {str(e)}")

    def read_serial_data(self):
        if self.serial_port and self.serial_port.is_open and not self.stop_reading:
            if self.serial_port.in_waiting > 0:
                try:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if line.startswith("MAF Voltage:"):
                        self.process_serial_data(line)
                except Exception as e:
                    print(f"Veri okuma hatası: {str(e)}")

    def process_serial_data(self, line):
        data = line.split(", ")
        try:
            maf_voltage = float(data[0].split(": ")[1])
            calibrated_voltage = float(data[1].split(": ")[1])
            calibration_factor = float(data[2].split(": ")[1])
            
            self.mafVoltageLCD.display(f"{maf_voltage:.3f}")
            self.afmVoltageLCD.display(f"{calibrated_voltage:.3f}")
            self.calibrationFactorLCD.display(f"{calibration_factor:.3f}")

            self.update_highlighted_row(maf_voltage)
        except (ValueError, IndexError) as e:
            print(f"Veri işleme hatası: {str(e)}")

    def update_highlighted_row(self, maf_voltage):
        nearest_index = self.find_nearest_voltage(maf_voltage)
        if nearest_index != self.highlighted_row and nearest_index != -1:
            if self.highlighted_row != -1:
                self.reset_row_color(self.highlighted_row)
            self.highlight_row(nearest_index)
            self.highlighted_row = nearest_index
            self.table.scrollToItem(self.table.item(nearest_index, 0))

    def stop_reading_data(self):
        self.stop_reading = True
        self.timer.stop()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.serial_port = None
            QMessageBox.information(self, "Bilgi", "Veri okuma durduruldu")

    def closeEvent(self, event):
        """Uygulama kapatılırken çağrılır"""
        try:
            self.stop_reading_data()
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
        except Exception as e:
            print(f"Kapatma hatası: {str(e)}")
        finally:
            event.accept()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = VoltageCalibrationApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Uygulama başlatma hatası: {str(e)}")