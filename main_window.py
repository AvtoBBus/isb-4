import hashlib
import sys
import time
import json
import multiprocessing as mp
import special_func as sf

from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QMainWindow,
                             QProgressBar, QPushButton, QSlider, QVBoxLayout,
                             QWidget)


class MainWindow(QMainWindow):
    options_path = ""

    def __init__(self, options_path: str):
        super().__init__()
        self.options_path = options_path
        self.initUI()
        

    def read_options(self) -> dict:
        with open(self.options_path) as json_file:
            options = json.load(json_file)
        return options

    def initUI(self):
        X_SIZE = 1067
        Y_SIZE = 600
        self.setWindowTitle('Hash function collision search')
        self.setFixedSize(X_SIZE, Y_SIZE)
        original_image = QImage('XP_4k.jpg')
        scaled_image = original_image.scaled(X_SIZE, Y_SIZE)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        self.setPalette(palette)
        options = self.read_options()
        self.card_info = QLabel(self)
        self.card_info.setText(f"Available card information: {options['bin']}******{options['last_digit']}")
        self.card_info.setFont(QFont('Arial font', 16))
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.timer = QBasicTimer()
        self.timer.stop()
        title_slider = QLabel('Select number of pools:', self)
        title_slider.setFont(QFont('Arial font', 14))
        self.result_label = QLabel('Result:')
        form_layout = QFormLayout()
        self.setLayout(form_layout)
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(1, 64)
        slider.setSingleStep(1)
        slider.setValue(36)
        slider.valueChanged.connect(self.updateLabel)
        self.value_label = QLabel('', self)
        self.value = slider.value()
        form_layout.addRow(self.card_info)
        form_layout.addRow(title_slider)
        form_layout.addRow(slider)
        form_layout.addRow(self.value_label)
        form_layout.addRow(self.result_label)
        form_layout.addRow(self.progress_bar)
        self.start_button = QPushButton('To start searching')
        self.start_button.clicked.connect(self.find_solution)
        form_layout.addWidget(self.start_button)
        central_widget = QWidget()
        central_widget.setLayout(form_layout)
        self.setCentralWidget(central_widget)

    def search_card_number(self, start: float):
        """
        функция поиска номера карты

        Args:
            start (float): время начала поиска
        """
        with mp.Pool(self.value) as p:
            for i, result in enumerate(p.map(sf.check_hash, range(99999, 10000000))):
                if result:
                    self.update_pb_on_success(start, result)
                    p.terminate()
                    break
                self.update_pb_on_progress(i)
            else:
                self.result_label.setText('Solution not found')
                self.progress_bar.setValue(100)

    def find_solution(self):
        """
           Подготовка прогрессбара, задание времени начала и вызов функции поиска номера карты
        """
        self.prepare_pb()
        start = time.time()
        self.search_card_number(start)

    def prepare_pb(self):
        """
            Подготавка прогрессбара и вывод информации
        """
        self.result_label.setText('Search in progress...')
        self.progress_bar.show()
        if not self.timer.isActive():
            self.timer.start(100, self)
        QApplication.processEvents()

    def update_pb_on_success(self, start: float, result: float):
        """
            Обновление прогрессбара и вывод информации о карте и времени поиска

        Args:
            start (float): время начала
            result (float): время окончания поиска
        """
        opitons = self.read_options()
        self.progress_bar.setValue(100)
        end = time.time() - start
        result_text = f'Found: {result}\n'
        result_text += f'Checking the Luhn Algorithm: {sf.luna_algorithm(result)}\n'
        result_text += f'Lead time: {end:.2f} seconds'
        self.card_info.setText(
            f'Available card information: {opitons["bin"]}{result}{opitons["last_digit"]}')
        self.result_label.setText(result_text)

    def update_pb_on_progress(self, i: int):
        """
            обновление ползунка в прогрессбаре

        Args:
            i (int): значение итерации
        """
        self.progress_bar.setValue(
            int((i + 1) / len(range(99999, 10000000)) * 100))

    def updateLabel(self, value: int):
        """
            Функция, которая обновляет значение числа в слайдере

        Args:
            value (int): число ядер
        """
        self.value_label.setText(str(value))

if __name__ == "__main__":
    options = {
        'hash': "7dbbccf1e06c2ea6c7f7711cb90b08eee16d1476fa0e75067d84a642494589149eba75ba396ad3ccbb9ca9d2fc5340cf",
        'bin' : '220015',
        'last_digit': '6302'    
    }
    options_path = 'options.json'
    with open(options_path, 'w') as file:
        json.dump(options, file)
    app = QApplication(sys.argv)
    mw = MainWindow(options_path)
    mw.show()
    sys.exit(app.exec_())