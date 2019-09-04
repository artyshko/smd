from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimediaWidgets import QVideoWidget

import os
import sys
import time
import requests

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.url = QUrl('https://accounts.spotify.com/en/login') 
        self.browser.page().profile().setCachePath(f'{os.getcwd()}/cache')
        self.browser.page().profile().setPersistentCookiesPolicy( self.browser.page().profile().NoPersistentCookies)
        self.browser.page().profile().clearHttpCache()
        #self.browser.setUrl(QUrl("file:///home/eve/Data/PycharmProjects/SpotifyMusicDownloader/GUI/templates/login.html"))
        self.browser.setUrl(QUrl("http://127.0.0.1:5000/login"))
        self.browser.page().profile().setPersistentCookiesPolicy( self.browser.page().profile().NoPersistentCookies)
        #self.browser.setUrl(QUrl("https://open.spotify.com/artist/3iOvXCl6edW5Um0fXEBRXy"))


        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)
        self.setGeometry(10, 10, 1200, 600)
        self.show()
        #self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("SMD")

    def navigate_mozarella(self):
        self.browser.setUrl(QUrl(""))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.browser.setUrl(QUrl(""))

    def navigate_to_url(self):  # Does not receive the Url

        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):

        if q.toString() == 'http://localhost:5000/shutdown':

            sys.exit(0)

        try:
            if q.scheme() == 'https':
                # Secure padlock icon
                self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

            else:
                # Insecure padlock icon
                self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        except:
            
            pass

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


def serverShutDown():
    requests.get('http://127.0.0.1:5000/shutdown')

if __name__ ==  "__main__":
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(serverShutDown)
    app.setApplicationName("SMD")
    app.setOrganizationName("GoART Lab.")
    app.setOrganizationDomain("")

    time.sleep(3)

    window = MainWindow()
    app.exec_()
