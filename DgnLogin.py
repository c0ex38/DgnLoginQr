import sys
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QIcon  # QIcon sınıfını ekliyorum
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Pencere başlığını ayarlıyorum
        self.setWindowTitle("TalipsanLoginQr")

        # Pencere simgesini ayarlıyorum
        self.setWindowIcon(QIcon("TalipsanLogo.ico"))

        # Pencere boyutlarını ekrana dinamik olarak sığacak şekilde ayarlıyorum
        screen_geometry = QDesktopWidget().screenGeometry()
        window_width = min(screen_geometry.width(), 1920)
        window_height = min(screen_geometry.height(), 1080)
        self.setGeometry(
            (screen_geometry.width() - window_width) // 2,
            (screen_geometry.height() - window_height) // 2,
            window_width,
            window_height,
        )

        # Web görünümünü oluşturuyorum
        self.web_view = QWebEngineView()
        self.web_view.page().profile().setHttpUserAgent("TalipsanLoginQr")

        # Sağ tıklama menüsünü devre dışı bırakmak için contextMenuEvent bağlantısını yapıyorum
        self.web_view.page().loadFinished.connect(self.on_load_finished)

        # Yüklemek için URL'yi tanımlıyorum
        self.url = QUrl.fromUserInput("https://talipsan.onestoreview.com/msa/stores?cmd=qrcode_show")
        self.web_view.load(self.url)

        # Web görünümünü merkezi bileşen olarak ayarlıyorum
        self.setCentralWidget(self.web_view)

        # 15 dakikada bir sayfayı yenilemek için QTimer ayarlıyorum
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reload_page)
        self.timer.start(900000)  # 15 dakika = 900000 milisaniye

    def on_load_finished(self):
        # Sağ tıklama menüsünü devre dışı bırakmak için JavaScript ekliyorum
        self.web_view.page().runJavaScript("""
            document.addEventListener('contextmenu', function(e) {
                e.preventDefault();
            });
        """)

    def reload_page(self):
        # Sayfayı yeniden yüklüyorum ve zamanı konsola yazdırıyorum
        self.web_view.load(self.url)
        print(f"Sayfa yenilendi: {datetime.datetime.now()}")


if __name__ == "__main__":
    # Uygulamayı başlatıyorum
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Pencereyi gösteriyorum
    sys.exit(app.exec_())
