import threading
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
import pyttsx3
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, QVariant
from ava_desktop_ui.Models.TaskRunner import RunTask


class CallHandler(QObject):
    transcript = str

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

    @pyqtSlot(QVariant, result=QVariant)
    def Avaconnected(self):

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 130)
        engine.setProperty('voice', voices[1].id)  # change index to change voices
        engine.say("Ava is online")

        engine.runAndWait()
        return "true"

    @pyqtSlot(QVariant, result=QVariant)
    def transcriptRecieved(self, args):
        print('Recieved: ', args)
        self.transcript = args
        try:
            t1 = threading.Thread(target=self._executeThread)
            t1.start()
            t1.join()
        except Exception as e:
            print(e)

        return "ok"

    def _executeThread(self):
        runTaskObject = RunTask(self.transcript.lower())
        print("Running Task")
        runTaskObject.enumerateData()


class WebView(QWebEngineView):
    mainWindow = None

    def __init__(self, mainWindow,url:str):
        super(WebView, self).__init__()
        self.mainWindow = mainWindow
        self.url = url
        self.channel = QWebChannel()
        self.handler = CallHandler(self.mainWindow)
        # self.handler.mainWindow = self.mainWindow
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)
        self.page().featurePermissionRequested.connect(self.onFeaturePermissionRequested)

        # file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Icons/index.html"))
        # self.local_url = QUrl.fromLocalFile(file_path)
        self.local_url = QUrl(url)
        print(self.local_url)
        self.load(self.local_url)

    def onFeaturePermissionRequested(self, url, feature):
        if feature in (QWebEnginePage.MediaAudioCapture,
                       QWebEnginePage.MediaVideoCapture,
                       QWebEnginePage.MediaAudioVideoCapture):
            self.page().setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.page().setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)

#
# if __name__ == "__main__":
#     app = QApplication([])
#     view = WebView()
#     view.show()
#     app.exec_()
