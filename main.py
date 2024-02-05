from QModernResizeableWindow import *
from GUI import Ui_MainWindow as GUI
from urllib.parse import urlparse
from matchImage import matchImage
from PyQt5.QtGui import QPixmap
from tempfile import gettempdir
from PyQt5.QtWidgets import *
from fileHandlers import *
from re import compile
from io import BytesIO
from PIL import Image
import requests
import os
def convertGifToSinglePng(gifContent, outputFileName="output.png"):
    try:
        gifImage = Image.open(BytesIO(gifContent))
        pngFrame = gifImage.convert("RGBA")
        pngFrame.save(outputFileName)
    except Exception as e:
        pass


findFormatPattern = compile(r"format=(\w+)&")


def getImageExt(imageUrl):
    result = findFormatPattern.search(imageUrl)
    if result:
        return result.group(1)
    path = urlparse(imageUrl).path
    _, fileExtenstion = os.path.splitext(path)
    fileExtenstion = fileExtenstion[1:]
    return fileExtenstion.lower()


class MainWindow(ResizeableWindow, QModernFramelessWindow):
    def __init__(
        self,
        useWidnowsDarkTitleBar: bool = False,
        titleBarBgColor="default",
        windowName: str = "default",
        windowIconPath="default",
        windowTitleFont="default",
        windowBorderRadius: int = 0,
    ):
        super(ResizeableWindow, self).__init__()
        ResizeableWindow.__init__(self)
        self.titleBar: (QModernDarkWindowsTitleBar | QModernTitleBar)
        self.ui = GUI()
        self.ui.setupUi(self)
        QModernFramelessWindow.start(
            self,
            useWidnowsDarkTitleBar,
            titleBarBgColor,
            windowName,
            windowIconPath,
            windowTitleFont,
            windowBorderRadius,
        )
        self.titleBar.title.setText("Country Ball Searcher")
        self.titleBar.setStyleSheet(
            self.titleBar.styleSheet()
            + "#"
            + self.titleBar.objectName()
            + "{border:1px solid red;border-bottom:none;}"
            + "QPushButton{border:none;}"
        )
        self.setWindowIconFromPath(
            str(GetMainAppDir() / "icons" / "windowIcon.png"), QSize(50, 50)
        )
        self.allBalls = [
            file.split(".")[0] for file in os.listdir(GetMainAppDir() / "balls")
        ]
        self.addBalls(self.allBalls)
        self.ui.pushButton_2.clicked.connect(self.searchBalls)
        self.setAcceptDrops(True)
        self.ui.label_2.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            del widget

    def searchBalls(self):
        searchTerm = self.ui.lineEdit.text().lower().replace(" ", "")
        searchedBalls = [
            ball
            for ball in self.allBalls
            if ball.lower().replace(" ", "").startswith(searchTerm)
        ]
        if searchedBalls == []:
            return
        self.addBalls(searchedBalls)

    def addBalls(self, countryNames: list):
        ui = self.ui
        scrollWidget = ui.scrollArea
        containerWidget = QWidget()
        containerLayout = QVBoxLayout(containerWidget)
        for countryName in countryNames:
            countryLayout = QHBoxLayout()
            countryLabel = QLabel(countryName)
            countryLayout.addWidget(countryLabel)
            imagePath = GetMainAppDir() / "balls" / f"{countryName}.png"
            imageLabel = QLabel()
            pixmap = QPixmap(str(imagePath))
            imageLabel.setPixmap(pixmap)
            imageLabel.setAlignment(Qt.AlignCenter)
            imageLabel.setScaledContents(True)
            imageLabel.setFixedSize(100, 100)
            countryLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
            countryLayout.addWidget(imageLabel)
            containerLayout.addLayout(countryLayout)
        scrollWidget.setWidget(containerWidget)


QABSTRACT_SCROLLABLE_STYLE = """
QScrollBar:vertical {
    border: 1px solid #999999;
    background: white;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(28, 167, 231), stop: 0.5 rgb(28, 167, 231), stop: 1 rgb(28, 167, 231));
    min-height: 0px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(28, 167, 231), stop: 0.5 rgb(28, 167, 231), stop: 1 rgb(28, 167, 231));
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(28, 167, 231), stop: 0.5 rgb(28, 167, 231), stop: 1 rgb(28, 167, 231));
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
"""
if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setStyleSheet(QABSTRACT_SCROLLABLE_STYLE)
    m = MainWindow(True, windowBorderRadius=8)

    def dragEnterEvent(event):
        mimeType = event.mimeData()
        try:
            if mimeType.hasUrls() and (mimeType.urls()[0]):
                m.ui.tabWidget.setCurrentIndex(1)
                event.acceptProposedAction()
        except IndexError:
            if path.exists(mimeType.text()):
                event.acceptProposedAction()

    def dropEvent(event):
        mimeType = event.mimeData()
        try:
            if mimeType.hasUrls() and mimeType.urls()[0].isLocalFile():
                filePath = str(Path(mimeType.urls()[0].toLocalFile()))
                with open(filePath, "rb") as f:
                    content = f.read()
                filePath = (
                    Path(gettempdir())
                    / "tempCountryBalls"
                    / f"country.{filePath.split('.')[-1]}"
                )
                createFile(filePath)
                with open(filePath, "wb") as f:
                    f.write(content)
                filePath = str(filePath)
                pixmap = QPixmap(filePath)
                m.ui.label_3.setPixmap(pixmap)
                name = matchImage(
                    str(
                        GetMainAppDir()
                        / ("countries" if m.ui.checkBox.isChecked() else "balls")
                    ),
                    filePath,
                    m.ui.spinBox.value(),
                )
                m.ui.label_2.setText(str(name))
                os.remove(filePath)
            elif mimeType.hasUrls() and (mimeType.urls()[0].isValid()):
                url = mimeType.urls()[0].toString()
                ext = getImageExt(url)
                if ext == "gif":
                    isGif = True
                    ext = "png"
                else:
                    isGif = False
                filePath = Path(gettempdir()) / "tempCountryBalls" / f"country.{ext}"
                createFile(filePath)
                print(filePath)
                content = requests.get(url).content
                if not isGif:
                    with open(filePath, "wb") as f:
                        f.write(content)
                else:
                    convertGifToSinglePng(content,filePath)
                filePath = str(filePath)
                pixmap = QPixmap(filePath)
                m.ui.label_3.setPixmap(pixmap)
                name = matchImage(
                    str(
                        GetMainAppDir()
                        / ("countries" if m.ui.checkBox.isChecked() else "balls")
                    ),
                    filePath,
                    m.ui.spinBox.value()
                )
                m.ui.label_2.setText(str(name))
                os.remove(filePath)
        except Exception as e:
            import traceback
            traceback.print_exc()

    m.dragEnterEvent = dragEnterEvent
    m.dropEvent = dropEvent
    m.show()
    app.exec_()
