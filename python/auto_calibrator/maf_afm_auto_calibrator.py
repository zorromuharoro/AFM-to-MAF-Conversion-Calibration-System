import numpy as np
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QAction, QSpinBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QLCDNumber, QLabel, QFileDialog, QMessageBox, QButtonGroup, QRadioButton)
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtSerialPort import QSerialPortInfo
import serial
import pyqtgraph as pg
import time
import logging
import matplotlib.pyplot as plt

logging.basicConfig(filename="hata.log", level=logging.ERROR)

class SerialReader(QThread):
    maf_value_signal = pyqtSignal(float)
    afm_value_signal = pyqtSignal(float)

    def __init__(self, port, delay=100):
        super().__init__()
        self.port = port
        try:
            self.serial = serial.Serial(port, 9600)
        except serial.SerialException as e:
            logging.error(f"Seri port hatası: {str(e)}")
            raise e
        self.running = False
        self.set_delay(delay)

    def set_delay(self, delay):
        self.delay = delay / 1000.0

    def run(self):
        self.running = True
        if not self.serial.is_open:
            try:
                self.serial.open()
            except serial.SerialException as e:
                logging.error(f"Seri port hatası: {str(e)}")
                self.running = False
                return
        while self.running:
            if self.serial.in_waiting > 0:
                try:
                    data = self.serial.readline().decode().strip()
                    values = np.array(data.split(","), dtype=float)
                    self.maf_value_signal.emit(values[0])
                    self.afm_value_signal.emit(values[1])
                except (ValueError, IndexError) as e:
                    logging.error(f"Veri okuma hatası: {str(e)}")
            time.sleep(self.delay)

    def stop(self):
        self.running = False
        if self.serial.is_open:
            self.serial.close()

class CalibrationApp(QMainWindow):
    def __init__(self, serial_reader):
        super().__init__()
        self.serial_reader = serial_reader
        self.initUI()

        # CSS dosyasını yükle
        style_file = QFile("ana_calibrator.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())

    def initUI(self):
        self.setWindowTitle("Sensör Kalibrasyonu")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.delay_combo_box = QComboBox()
        self.delay_combo_box.addItem("0ms", 0)
        self.delay_combo_box.addItem("10ms", 10)
        self.delay_combo_box.addItem("50ms", 50)
        self.delay_combo_box.addItem("100ms", 100)
        self.layout.addWidget(self.delay_combo_box)
        self.delay_combo_box.currentIndexChanged.connect(self.apply_delay)

        self.plot_data = {'MAF': [], 'AFM': []}
        self.calibration_factors = {}
        self.maf_voltage = 0

        self.navbar = self.addToolBar("Navbar")

        self.combo_box = QComboBox()
        self.navbar.addWidget(self.combo_box)
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            self.combo_box.addItem(port.portName())

        start_action = QAction("Başlat", self)
        start_action.triggered.connect(self.start_reading)
        self.navbar.addAction(start_action)

        stop_action = QAction("Durdur", self)
        stop_action.triggered.connect(self.stop_reading)
        self.navbar.addAction(stop_action)

        save_action = QAction("Kaydet", self)
        save_action.triggered.connect(self.save_table)
        self.navbar.addAction(save_action)

        load_action = QAction("Tabloyu Yükle", self)
        load_action.triggered.connect(self.load_table)
        self.navbar.addAction(load_action)

        self.delay_layout = QHBoxLayout()
        self.layout.addLayout(self.delay_layout)

        self.main_layout = QVBoxLayout()
        self.layout.addLayout(self.main_layout)

        self.table_size_group = QButtonGroup(self)
        self.table_size_group.buttonClicked.connect(self.set_table_size)

        self.size_25_button = QRadioButton("25 Adet (0.2V Aralık)")
        self.table_size_group.addButton(self.size_25_button)
        self.layout.addWidget(self.size_25_button)

        self.size_50_button = QRadioButton("50 Adet (0.1V Aralık)")
        self.table_size_group.addButton(self.size_50_button)
        self.layout.addWidget(self.size_50_button)

        self.size_75_button = QRadioButton("75 Adet (0.067V Aralık)")
        self.table_size_group.addButton(self.size_75_button)
        self.layout.addWidget(self.size_75_button)

        self.size_100_button = QRadioButton("100 Adet (0.05V Aralık)")
        self.table_size_group.addButton(self.size_100_button)
        self.layout.addWidget(self.size_100_button)

        self.size_50_button.setChecked(True)

        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(50)
        self.table.setHorizontalHeaderLabels([f"{i * 0.1:.1f} V" for i in range(50)])
        self.table.setVerticalHeaderLabels(["Kalibrasyon Faktörü"])
        self.main_layout.addWidget(self.table)

        self.maf_lcd = QLCDNumber()
        self.afm_lcd = QLCDNumber()
        self.maf_label = QLabel("MAF Voltajı:")
        self.afm_label = QLabel("AFM Voltajı:")

        maf_layout = QHBoxLayout()
        maf_layout.addWidget(self.maf_label)
        maf_layout.addWidget(self.maf_lcd)
        self.main_layout.addLayout(maf_layout)

        afm_layout = QHBoxLayout()
        afm_layout.addWidget(self.afm_label)
        afm_layout.addWidget(self.afm_lcd)
        self.main_layout.addLayout(afm_layout)

        self.maf_plot = pg.PlotWidget(title="MAF Voltajı")
        self.maf_plot.setBackground('w')  
        self.maf_plot.getAxis('left').setPen(pg.mkPen(color='#28a745'))  
        self.maf_plot.getAxis('bottom').setPen(pg.mkPen(color='#28a745'))  
        self.main_layout.addWidget(self.maf_plot)

        self.afm_plot = pg.PlotWidget(title="AFM Voltajı")
        self.afm_plot.setBackground('w')  
        self.afm_plot.getAxis('left').setPen(pg.mkPen(color='#28a745'))  
        self.afm_plot.getAxis('bottom').setPen(pg.mkPen(color='#28a745'))  
        self.main_layout.addWidget(self.afm_plot)

        self.plot_button = QPushButton("Grafikleri Göster")
        self.plot_button.setToolTip("Matplotlib Grafiklerini Göster")
        self.main_layout.addWidget(self.plot_button)
        self.plot_button.clicked.connect(self.show_matplotlib_plots)

    def show_matplotlib_plots(self):
        plt.figure(figsize=(8, 6))
        plt.plot(self.plot_data['MAF'], label='MAF', color='red')
        plt.xlabel('Veri Noktası')
        plt.ylabel('MAF Değeri')
        plt.title('MAF Değerleri')
        plt.legend()
        plt.grid(True)

        plt.figure(figsize=(8, 6))
        plt.plot(self.plot_data['AFM'], label='AFM', color='blue')
        plt.xlabel('Veri Noktası')
        plt.ylabel('AFM Değeri')
        plt.title('AFM Değerleri')
        plt.legend()
        plt.grid(True)

        plt.show()

    def start_reading(self):
        port_name = self.combo_box.currentText()
        delay = self.delay_combo_box.currentData()
        if hasattr(self, 'serial_reader'):
            if self.serial_reader is not None and self.serial_reader.isRunning():
                self.serial_reader.stop()
                self.serial_reader.wait()
        try:
            self.serial_reader = SerialReader(port_name, delay)
        except serial.SerialException as e:
            logging.error(f"Seri port hatası: {str(e)}")
            QMessageBox.critical(self, "Hata", str(e))
            return
        self.serial_reader.maf_value_signal.connect(self.update_maf)
        self.serial_reader.afm_value_signal.connect(self.update_afm)
        self.serial_reader.start()

    def stop_reading(self):
        if self.serial_reader:
            self.serial_reader.stop()
            self.serial_reader.wait()

    def save_table(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Tabloyu Kaydet", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    voltages_str = "const float refVoltages[] = {"
                    factors_str = "const float calibrationFactors[] = {"
                    for col in range(1, self.table.columnCount()):
                        voltage_label = self.table.horizontalHeaderItem(col).text().split()[0]
                        calibration_factor_item = self.table.item(0, col)
                        if calibration_factor_item is not None:
                            calibration_factor = calibration_factor_item.text()
                            voltages_str += voltage_label + ", "
                            factors_str += calibration_factor + ", "
                    voltages_str = voltages_str.rstrip(", ") + "};\n"
                    factors_str = factors_str.rstrip(", ") + "};"
                    f.write(voltages_str + '\n' + factors_str)
            except Exception as e:
                logging.error(f"Dosya kaydetme hatası: {str(e)}")
                QMessageBox.critical(self, "Hata", str(e))

    def load_table(self):
        header = []
        file_path, _ = QFileDialog.getOpenFileName(self, "Tabloyu Yükle", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    header = f.readline().strip().split(',')
                    for line in f:
                        data = line.strip().split(',')
                        voltage = data[0]
                        calibration_factor = data[1]
                        col = int(float(voltage) * 10)
                        calibration_factor_item = QTableWidgetItem(calibration_factor)
                        self.table.setItem(0, col, calibration_factor_item)
            except Exception as e:
                logging.error(f"Dosya yükleme hatası: {str(e)}")
                QMessageBox.critical(self, "Hata", str(e))
                
    def set_table_size(self, button):
        if button == self.size_25_button:
            num_columns = 26  # 25 + 1
            voltage_step = 0.2
        elif button == self.size_50_button:
            num_columns = 51  # 50 + 1
            voltage_step = 0.1
        elif button == self.size_75_button:
            num_columns = 76  # 75 + 1
            voltage_step = 0.067
        elif button == self.size_100_button:
            num_columns = 101  # 100 + 1
            voltage_step = 0.05

        self.table.setRowCount(1)
        self.table.setColumnCount(num_columns)
        self.table.setHorizontalHeaderLabels([f"{i * voltage_step:.3f} V" for i in range(num_columns)])
        self.table.setVerticalHeaderLabels(["Kalibrasyon Faktörü"])

    def update_maf(self, maf_value):
        maf_index = int(maf_value * 10)
        col = maf_index
        self.table.setCurrentCell(0, col)
        self.maf_lcd.display(maf_value)
        self.plot_data['MAF'] = np.append(self.plot_data.get('MAF', np.array([])), maf_value)
        self.maf_voltage = maf_value
        if len(self.plot_data['MAF']) % 100 == 0:  # Update plot every 100 data points
            self.maf_plot.plot(self.plot_data['MAF'], clear=True, pen='r')

    def update_afm(self, afm_value):
        maf_voltage = self.maf_voltage
        maf_value = self.plot_data['MAF'][-1]
        maf_index = int(maf_value * 10)
        col = maf_index
        self.table.setCurrentCell(0, col)
        self.afm_lcd.display(afm_value)
        self.plot_data['AFM'] = np.append(self.plot_data.get('AFM', np.array([])), afm_value)
        if len(self.plot_data['AFM']) % 100 == 0:  # Update plot every 100 data points
            self.afm_plot.plot(self.plot_data['AFM'], clear=True, pen='b')
        if maf_voltage != 0:
            calibration_factor = afm_value / maf_voltage
            if maf_index not in self.calibration_factors:
                self.calibration_factors[maf_index] = []
            self.calibration_factors[maf_index] = np.append(self.calibration_factors.get(maf_index, np.array([])), calibration_factor)
            avg_calibration_factor = np.mean(self.calibration_factors[maf_index])
            calibration_factor_str = '{:.2f}'.format(avg_calibration_factor)
            self.table.setItem(0, col, QTableWidgetItem(calibration_factor_str))

    def apply_delay(self):
        delay = self.delay_combo_box.currentData()
        self.serial_reader.set_delay(delay)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        calibration_app = CalibrationApp(None)
        calibration_app.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Uygulama başlatma hatası: {str(e)}")
        QMessageBox.critical(None, "Hata", str(e))
        sys.exit(1)