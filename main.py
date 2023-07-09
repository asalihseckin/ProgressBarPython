import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class DosyaSayaciThread(QThread):
    dosya_sayisi_degisti = pyqtSignal(int)

    def __init__(self, dizin):
        super().__init__()
        self.dizin = dizin

    def run(self):
        while True:
            sayi = self.dosya_sayisi_bul(self.dizin)
            self.dosya_sayisi_degisti.emit(sayi)
            self.sleep(1)

    def dosya_sayisi_bul(self, dizin):
        dosya_sayisi = 0
        for dosya in os.listdir(dizin):
            if os.path.isfile(os.path.join(dizin, dosya)):
                dosya_sayisi += 1
        return dosya_sayisi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('dosyalar.ui', self)
        self.startButton.clicked.connect(self.start_count)

    def start_count(self):
        dizin_yolu = "C:\src"
        self.dosyaSayisiEdit.setText("0")

        self.dosya_sayaci_thread = DosyaSayaciThread(dizin_yolu)
        self.dosya_sayaci_thread.dosya_sayisi_degisti.connect(self.update_dosya_sayisi)
        self.dosya_sayaci_thread.start()

    def update_dosya_sayisi(self, sayi):
        self.dosyaSayisiEdit.setText(str(sayi))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
