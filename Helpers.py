from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent,QScreen
from qtpy.QtWidgets import QFrame,QApplication,QMainWindow
def snapToLeft(self:QMainWindow,screen:QScreen):
    if screen is not None:
        geo = screen.availableGeometry()
        self.oldGeomtry = self.geometry()
        self.setGeometry(geo.x(), geo.y(), geo.width() // 2, geo.height())
        self.setGeometry(geo.x(), geo.y(), geo.width() // 2, geo.height())
        self.snapped = True
def snapToRight(self,screen:QScreen):
    if screen is not None:
        self.oldGeomtry = self.geometry()
        geo = screen.availableGeometry()
        self.setGeometry(geo.x() + geo.width() // 2, geo.y(), geo.width() // 2, geo.height())
        self.setGeometry(geo.x() + geo.width() // 2, geo.y(), geo.width() // 2, geo.height())
        self.snapped = True
def modifyQFrameDragBehave(self:QMainWindow, frame: QFrame):
    def drag_window(event:QMouseEvent):
        try:
            if event.buttons() == Qt.LeftButton and self.isMaximizedNative:
                self.isMaximizedNative = False
                self.setGeometry(self.oldGeomtry)
            elif event.buttons() == Qt.LeftButton and self.snapped:
                self.setGeometry(self.oldGeomtry)
                self.snapped = False
                self.move(event.globalX() - 150 ,event.globalY() - 20)
                event.accept()
            elif event.buttons() == Qt.LeftButton and not self.isMaximized():
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
            elif event.buttons() == Qt.LeftButton and self.isMaximized():
                self.showNormal()
                self.move(event.globalX() - 150 ,event.globalY() - 20)
                event.accept()
        except:
            pass

    def mousePressEvent(event):
        try:
            if event.button() == Qt.LeftButton:
                self.dragPos = event.globalPos()
                event.accept()
        except:
            pass

    frame.mouseMoveEvent = drag_window
    frame.mousePressEvent = mousePressEvent

    def snap_window(event):
        if event.type() == event.MouseButtonRelease and event.button() == Qt.LeftButton:
            screen = QApplication.screenAt(event.globalPos())
            geo = screen.geometry()
            if abs(event.globalPos().x() - geo.left()) < 10:
                snapToLeft(self,screen)
            if abs(event.globalPos().y() - geo.top()) < 10:
                if not self.isMaximized():
                    self.showMaximized()
                else:
                    self.showNormal()
            if abs(event.globalPos().x() - geo.right()) < 10:
                snapToRight(self,screen)
    frame.mouseReleaseEvent = snap_window
def modifyQFrameDoubleClickBehave(self, frame:QFrame) -> None:
    def mouseDoubleClickEvent(a0):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        return self.mouseDoubleClickEvent(a0)
    frame.mouseDoubleClickEvent = mouseDoubleClickEvent