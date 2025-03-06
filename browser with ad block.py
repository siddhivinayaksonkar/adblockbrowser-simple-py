import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineUrlRequestInterceptor

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self):
        super().__init__()
        self.blocked_domains = [
            "ads.example.com",
            "doubleclick.net",
            "adservice.google.com",
            "trackersite.com",
            "ads.yahoo.com",
            "analytics.example.com"
        ]

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if any(blocked in url for blocked in self.blocked_domains):
            print(f"Blocked: {url}")
            info.block(True)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser with AdBlock")
        self.setGeometry(100, 100, 1024, 768)

        
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        
        profile = QWebEngineProfile.defaultProfile()
        self.ad_blocker = AdBlocker()
        profile.setUrlRequestInterceptor(self.ad_blocker)  

        
        toolbar = QToolBar()
        self.addToolBar(toolbar)

       
        back_btn = toolbar.addAction("←")
        back_btn.triggered.connect(self.web_view.back)

       
        forward_btn = toolbar.addAction("→")
        forward_btn.triggered.connect(self.web_view.forward)

       
        refresh_btn = toolbar.addAction("↻")
        refresh_btn.triggered.connect(self.web_view.reload)

        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        toolbar.addWidget(self.url_bar)

        
        self.load_url("https://www.google.com/")

    def load_url(self, url=None):
        if not url:
            url = self.url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.web_view.load(QUrl(url))
        self.url_bar.setText(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
