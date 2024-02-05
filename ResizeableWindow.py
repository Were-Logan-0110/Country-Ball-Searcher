from qtpy import QtCore, QtWidgets
from platform import system

if system() == "Windows":
    import ctypes.wintypes
    from ctypes.wintypes import POINT
    import win32con
    import win32gui
    from qtpy.QtCore import Qt, QRect
    from qtpy.QtGui import QCursor
    from qtpy.QtWidgets import QApplication
    from qtpy.QtWinExtras import QtWin
    from traceback import format_exc

    class MINMAXINFO(ctypes.Structure):
        _fields_ = [
            ("ptReserved", POINT),
            ("ptMaxSize", POINT),
            ("ptMaxPosition", POINT),
            ("ptMinTrackSize", POINT),
            ("ptMaxTrackSize", POINT),
        ]


class SideGrip(QtWidgets.QWidget):
    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)
        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class ResizeableWindow(QtWidgets.QMainWindow):
    _gripSize = 8
    BorderWidth = 6

    def __init__(self, *args, **kwargs):
        if system() != "Windows":
            QtWidgets.QMainWindow.__init__(self)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.sideGrips = [
                SideGrip(self, QtCore.Qt.LeftEdge),
                SideGrip(self, QtCore.Qt.TopEdge),
                SideGrip(self, QtCore.Qt.RightEdge),
                SideGrip(self, QtCore.Qt.BottomEdge),
            ]
            self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]
            [
                cornerGrip.setStyleSheet("background:transparent;")
                for cornerGrip in self.cornerGrips
            ]
            self.setStyleSheet("background-color:black;")
        else:
            super(ResizeableWindow, self).__init__(*args, **kwargs)
            self._rect = QApplication.instance().desktop().availableGeometry(self)
            self.resize(800, 600)
            self.setWindowFlags(
                Qt.Window
                | Qt.FramelessWindowHint
                | Qt.WindowSystemMenuHint
                | Qt.WindowMinimizeButtonHint
                | Qt.WindowMaximizeButtonHint
                | Qt.WindowCloseButtonHint
            )
            style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
            win32gui.SetWindowLong(
                int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME
            )

            if QtWin.isCompositionEnabled():
                QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
            else:
                QtWin.resetExtendedFrame(self)

    def nativeEvent(self, eventType, message):
        retval, result = super(ResizeableWindow, self).nativeEvent(eventType, message)
        if getattr(self, "titleBar", False):
            try:
                if eventType == "windows_generic_MSG":
                    msg = ctypes.wintypes.MSG.from_address(message.__int__())
                    pos = QCursor.pos()
                    x = pos.x() - self.frameGeometry().x()
                    y = pos.y() - self.frameGeometry().y()

                    widg = self.childAt(x, y)
                    if (
                        isinstance(widg, QtWidgets.QPushButton)
                        and widg.objectName() != "pushButton_4"
                    ):
                        return retval, result
                    if msg.message == win32con.WM_NCCALCSIZE:
                        return True, 0
                    if msg.message == win32con.WM_GETMINMAXINFO:
                        info = ctypes.cast(
                            msg.lParam, ctypes.POINTER(MINMAXINFO)
                        ).contents
                        info.ptMaxSize.x = self._rect.width()
                        info.ptMaxSize.y = self._rect.height()
                        info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0
                    if msg.message == win32con.WM_NCHITTEST:
                        w, h = self.width(), self.height()
                        lx = x < self.BorderWidth
                        rx = x > w - self.BorderWidth
                        ty = y < self.BorderWidth
                        by = y > h - self.BorderWidth
                        if lx and ty:
                            return True, win32con.HTTOPLEFT
                        elif rx and by:
                            return True, win32con.HTBOTTOMRIGHT
                        elif rx and ty:
                            return True, win32con.HTTOPRIGHT
                        elif lx and by:
                            return True, win32con.HTBOTTOMLEFT
                        elif ty:
                            return True, win32con.HTTOP
                        elif by:
                            return True, win32con.HTBOTTOM
                        elif lx:
                            return True, win32con.HTLEFT
                        elif rx:
                            return True, win32con.HTRIGHT
                        CRPos = QCursor.pos()
                        titleBarRect = self.titleBar.rect()
                        if titleBarRect.contains(self.mapFromGlobal(CRPos)):
                            return True, win32con.HTCAPTION
                    if msg.message == win32con.WM_MOVE:
                        if self.isMaximizedNative and (not self.isMinimized()):
                            QCURSORPOS = QCursor.pos()
                            scaleX = self.oldGeomtry.width() / self.geometry().width()
                            scaleY = self.oldGeomtry.height() / self.geometry().height()

                            offsetX = (
                                QCURSORPOS.x() - self.frameGeometry().x()
                            ) * scaleX
                            offsetY = (
                                QCURSORPOS.y() - self.frameGeometry().y()
                            ) * scaleY

                            newPosX = QCURSORPOS.x() - offsetX
                            newPosY = QCURSORPOS.y() - offsetY
                            GeometryRect = QtCore.QRect(
                                int(newPosX),
                                int(newPosY),
                                self.oldGeomtry.width(),
                                self.oldGeomtry.height(),
                            )
                            self.setGeometry(GeometryRect)
                            self.isMaximizedNative = False
                            self.isMaximizedNativeBefore = False
                            self.isWaitingForMouseSlip = True
                return retval, result
            except Exception as e:
                print(format_exc())
                pass
        else:
            return retval, result

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(3, 3, 3, 3)
        outRect = self.rect()
        inRect = outRect.adjusted(
            self.gripSize, self.gripSize, -self.gripSize, -self.gripSize
        )
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft())
        )
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized()
        )
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight())
        )
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized()
        )
        self.sideGrips[0].setGeometry(0, inRect.top(), self.gripSize, inRect.height())
        self.sideGrips[1].setGeometry(inRect.left(), 0, inRect.width(), self.gripSize)
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), inRect.top(), self.gripSize, inRect.height()
        )
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), inRect.width(), self.gripSize
        )

    def resizeEvent(self, event):
        if system() != "Windows":
            QtWidgets.QMainWindow.resizeEvent(self, event)
            self.updateGrips()
            return super().resizeEvent(event)
        else:
            return super().resizeEvent(event)
