from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QSizePolicy,
    QGridLayout,
)
from qtpy.QtGui import QIcon, QPainter, QColor, QPixmap
from qtpy.QtCore import QSize, Qt
from qtpy.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from qtpy.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from qtpy.QtWidgets import *
import sys
from os import path
from pathlib import Path

appMainDir = Path(getattr(sys, "_MEIPASS", path.dirname(path.abspath(__file__))))


class QModernTitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("frameContent")
        self.frame = QFrame(self)
        self.frame.setMaximumHeight(70)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color: rgb(14, 13, 13);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.titleBarIcon = QPushButton(self.frame_3)
        self.titleBarIcon.setObjectName("titleBarIcon")
        self.titleBarIcon.setStyleSheet("border:none;")
        icon = QIcon()
        icon.addFile(
            str(appMainDir / "icons/PyraNodeIcon.png"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.titleBarIcon.setIcon(icon)
        self.titleBarIcon.setIconSize(QSize(52, 52))
        self.horizontalLayout_3.addWidget(self.titleBarIcon)
        self.title = QLabel(self.frame_3)
        self.title.setObjectName("title")
        self.title.setStyleSheet(
            "color: #FFFDFD;\n"
            "text-align: center;\n"
            "font-family: Inter;\n"
            "font-size: 25px;\n"
            "font-style: normal;\n"
            "font-weight: 500;\n"
            "line-height: normal;"
        )
        self.horizontalLayout_3.addWidget(self.title)
        self.horizontalLayout_2.addWidget(self.frame_3, 0, Qt.AlignLeft)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName("frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSpacing(35)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.minimizeButton = QPushButton(self.frame_2)
        self.minimizeButton.setObjectName("minimizeButton")
        self.minimizeButton.setStyleSheet(
            "QPushButton {border: none; background: transparent; padding: 0; margin: 0; icon-size: 24px; }"
            "QPushButton:hover { padding:1px;border-radius:8px;background: rgba(191, 191, 191, 20); }"
            "QPushButton:pressed { padding:1px;border-radius:8px;background: rgba(141, 161, 171, 20); }border:none"
        )
        icon1 = QIcon()
        icon1.addFile(
            str(appMainDir / "icons/minus-sm.svg"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.minimizeButton.setIcon(icon1)
        self.minimizeButton.setIconSize(QSize(29, 29))
        self.horizontalLayout.addWidget(self.minimizeButton, 0, Qt.AlignRight)
        self.maximizeButton = QPushButton(self.frame_2)
        self.maximizeButton.setObjectName("pushButton")
        self.maximizeButton.setStyleSheet(
            "QPushButton {border: none; background: transparent; padding: 0; margin: 0; icon-size: 24px; }"
            "QPushButton:hover { padding:1px;border-radius:8px;background: rgba(191, 191, 191, 20); }"
            "QPushButton:pressed { padding:1px;border-radius:8px;background: rgba(141, 161, 171, 20); }"
        )
        icon2 = QIcon()
        icon2.addFile(
            str(appMainDir / "icons/maximize-02.svg"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.maximizeButton.setIcon(icon2)
        self.maximizeButton.setIconSize(QSize(30, 30))
        self.horizontalLayout.addWidget(self.maximizeButton, 0, Qt.AlignRight)
        self.closeButton = QPushButton(self.frame_2)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setStyleSheet(
            "QPushButton {border: none; background: transparent; padding: 0; margin: 0; icon-size: 24px; }"
            "QPushButton:hover { padding:1px;border-radius:8px;background: rgba(191, 191, 191, 20); }"
            "QPushButton:pressed { padding:1px;border-radius:8px;background: rgba(191, 191, 191, 20); }"
        )
        icon3 = QIcon()
        icon3.addFile(str(appMainDir / "icons/x.svg"), QSize(), QIcon.Normal, QIcon.Off)
        self.closeButton.setIcon(icon3)
        self.closeButton.setIconSize(QSize(30, 30))
        self.horizontalLayout.addWidget(self.closeButton, 0, Qt.AlignRight)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(0)
        self.gridLayout.addWidget(self.frame, 0, 0, 0, 0)
        self.retranslateUi(self)

    def retranslateUi(self, Form):
        self.titleBarIcon.setText("")
        self.title.setText("PyraNode")
        self.minimizeButton.setText("")
        self.maximizeButton.setText("")
        self.closeButton.setText("")

    def QIconFromSvg(svgPath, color="black"):
        img = QPixmap(svgPath)
        qp = QPainter(img)
        qp.setCompositionMode(QPainter.CompositionMode_SourceIn)
        qp.fillRect(img.rect(), QColor(color))
        qp.end()
        return QIcon(img)

    def setTitleBarBgColor(self, color):
        self.frame.setStyleSheet(f"background-color: {color}")

    def setWindowTitle(self, a0: str) -> None:
        self.title.setText(a0)

    def setWindowIcon(self, icon: QIcon) -> None:
        self.titleBarIcon.setIcon(icon)

    def setWindowIconFromPath(self, path: (str | Path), size=(None | QSize)):
        icon = QIcon()
        icon.addFile(
            str(path), QSize(size) if size else QSize(), QIcon.Normal, QIcon.Off
        )
        self.titleBarIcon.setIcon(icon)

    def hideIcon(self):
        self.titleBarIcon.hide()


class QModernDarkWindowsTitleBar(QFrame):
    def __init__(self):
        super().__init__()
        Layout = QHBoxLayout()
        Layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(Layout)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.setStyleSheet("")
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        self.frame.setGeometry(QRect(0, 0, 621, 35))
        self.frame.setStyleSheet("background-color:black;\n" "border:none;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.horizontalLayout = QHBoxLayout(self.frame)
        self.frame.horizontalLayout.setSpacing(0)
        self.frame.horizontalLayout.setObjectName("horizontalLayout")
        self.frame.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame.frame_5 = QFrame(self.frame)
        self.frame.frame_5.setObjectName("frame_5")
        self.frame.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame.frame_5.setFrameShadow(QFrame.Raised)
        self.frame.horizontalLayout_4 = QHBoxLayout(self.frame.frame_5)
        self.frame.horizontalLayout_4.setSpacing(0)
        self.frame.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame.horizontalLayout_4.setContentsMargins(12, 0, 0, 0)
        self.frame.titleBarIcon = QPushButton(self.frame.frame_5)
        self.frame.titleBarIcon.setObjectName("titleBarIcon")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame.titleBarIcon.sizePolicy().hasHeightForWidth()
        )
        self.frame.titleBarIcon.setStyleSheet("border:none;")
        icon2 = QIcon()
        icon2.addFile(
            str(appMainDir / "icons/PyraNodeIcon.png"),
            QSize(30, 30),
            QIcon.Normal,
            QIcon.Off,
        )
        self.frame.titleBarIcon.setIcon(icon2)
        self.frame.titleBarIcon.setIconSize(QSize(35, 35))
        self.frame.horizontalLayout_4.addWidget(
            self.frame.titleBarIcon, 0, Qt.AlignLeft
        )

        self.frame.title = QLabel(self.frame.frame_5)
        self.frame.title.setObjectName("title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.title.sizePolicy().hasHeightForWidth())
        self.frame.title.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamily("Segoe UI")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(10)
        self.frame.title.setFont(font1)
        self.frame.title.setStyleSheet("color:white;")
        self.frame.title.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.frame.horizontalLayout_4.addWidget(self.frame.title, 0, Qt.AlignLeft)

        self.frame.horizontalLayout.addWidget(self.frame.frame_5, 0, Qt.AlignLeft)

        self.frame.frame_4 = QFrame(self.frame)
        self.frame.frame_4.setObjectName("frame_4")
        sizePolicy1.setHeightForWidth(
            self.frame.frame_4.sizePolicy().hasHeightForWidth()
        )
        self.frame.frame_4.setSizePolicy(sizePolicy1)
        self.frame.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame.frame_4.setFrameShadow(QFrame.Raised)
        self.frame.horizontalLayout_3 = QHBoxLayout(self.frame.frame_4)
        self.frame.horizontalLayout_3.setSpacing(0)
        self.frame.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame.minimizeButton = QPushButton(self.frame.frame_4)
        self.frame.minimizeButton.setObjectName("minimizeButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.frame.minimizeButton.sizePolicy().hasHeightForWidth()
        )
        self.frame.minimizeButton.setSizePolicy(sizePolicy2)
        self.frame.minimizeButton.setMinimumSize(QSize(45, 0))
        self.frame.minimizeButton.setStyleSheet(
            "QPushButton::hover {\n"
            "	background-color: rgb(66, 66, 66);border:none;\n"
            "}"
        )
        icon = QIcon()
        icon.addFile(
            str(appMainDir / "icons/minus.svg"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.frame.minimizeButton.setIcon(icon)
        self.frame.minimizeButton.setIconSize(QSize(22, 22))

        self.frame.horizontalLayout_3.addWidget(self.frame.minimizeButton)

        self.frame.maximizeButton = QPushButton(self.frame.frame_4)
        self.frame.maximizeButton.setObjectName("pushButton")
        sizePolicy2.setHeightForWidth(
            self.frame.maximizeButton.sizePolicy().hasHeightForWidth()
        )
        self.frame.maximizeButton.setSizePolicy(sizePolicy2)
        self.frame.maximizeButton.setMinimumSize(QSize(45, 0))
        self.frame.maximizeButton.setStyleSheet(
            "QPushButton::hover {\n"
            "	background-color: rgb(66, 66, 66);border:none;\n"
            "}"
        )
        icon1 = QIcon()
        icon1.addFile(
            str(appMainDir / "icons/squar.svg"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.frame.maximizeButton.setIcon(icon1)
        self.frame.maximizeButton.setIconSize(QSize(16, 16))
        self.frame.horizontalLayout_3.addWidget(self.frame.maximizeButton)

        self.frame.closeButton = QPushButton(self.frame.frame_4)
        self.frame.closeButton.setObjectName("closeButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.frame.closeButton.sizePolicy().hasHeightForWidth()
        )
        self.frame.closeButton.setSizePolicy(sizePolicy3)
        self.frame.closeButton.setMinimumSize(QSize(45, 0))
        self.frame.closeButton.setStyleSheet(
            "QPushButton::hover{\n" "	background:rgb(255, 33, 36);border:none;\n" "}"
        )
        icon2 = QIcon()
        icon2.addFile(
            str(appMainDir / "icons/Xwin.svg"), QSize(), QIcon.Normal, QIcon.Off
        )
        self.frame.closeButton.setIcon(icon2)
        self.frame.closeButton.setIconSize(QSize(20, 20))
        self.frame.horizontalLayout_3.addWidget(self.frame.closeButton)
        self.frame.horizontalLayout.addWidget(self.frame.frame_4, 0, Qt.AlignRight)
        self.retranslateUi(self)

    def retranslateUi(self, Form):
        self.frame.minimizeButton.setText("")
        self.frame.title.setText(QCoreApplication.translate("Form", "Calender", None))
        self.frame.minimizeButton.setText("")
        self.frame.maximizeButton.setText("")
        self.frame.closeButton.setText("")

    def setTitleBarBgColor(self, color):
        self.frame.setStyleSheet(f"background-color: {color}")

    def setWindowTitle(self, a0: str) -> None:
        self.frame.title.setText(a0)

    def setWindowIcon(self, icon: QIcon) -> None:
        self.frame.minimizeButton.setIcon(icon)

    def setWindowIconFromPath(self, path: (str | Path), size=(None | QSize)):
        icon = QIcon()
        icon.addFile(
            str(path), QSize(size) if size else QSize(), QIcon.Normal, QIcon.Off
        )
        self.titleBarIcon.setIcon(icon)

    def hideIcon(self):
        self.frame.titleBarIcon.hide()
