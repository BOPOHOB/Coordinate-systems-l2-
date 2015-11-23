from OpenGL.GL import *
from PySide import QtGui
from PySide import QtOpenGL
from PySide import QtCore
from CParallelepiped import CParallelepiped


class CGLWidget(QtOpenGL.QGLWidget):
    rotateMatrix = QtGui.QMatrix4x4()
    rotate = QtGui.QVector2D()
    zoom = float()
    translate = QtGui.QVector2D()
    mPPosition = QtCore.QPoint()
    edge = float()
    box = CParallelepiped(QtGui.QVector3D(0,0,0))

    def __init__(self,parent = None):
        super().__init__(parent)
        self.box.include(QtGui.QVector3D(1,1,1))
        self.box.include(QtGui.QVector3D(0,0,0))

    def transformIdentity(self):
        self.rotateMatrix.setToIdentity()

        self.rotate = self.translate = QtGui.QVector2D(0.0, 0.0)

        self.zoom = 0.5

        self.repaint()

    def resizeGL(self, width, height) :
        self.edge = width if width < height else height
        glPointSize(self.edge / 300 + 1)

    def loadRotate(self):
        glMatrixMode(GL_MODELVIEW)
        glRotatef(self.rotate.x(),1.,0.,0.)
        glRotatef(self.rotate.y(),0.,1.,0.)
        if QtCore.__version_info__[0] >= 5:
            glMultMatrixf(self.rotateMatrix.data())
        else:
            glMultMatrixd(self.rotateMatrix.data())

    def modelviewMatrix(self):
        result = QtGui.QMatrix4x4()
        self.makeCurrent()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.loadRotate()
        buf = (GLfloat * 16)()
        glGetFloatv(GL_MODELVIEW_MATRIX, buf)
        for i in range(0,4):
            result.setRow(i, QtGui.QVector4D(buf[0 + i], buf[4 + i], buf[8 + i], buf[12 + i]))
        return result

    def bufRotate(self):
        if self.rotate.lengthSquared() :
            self.rotateMatrix = self.modelviewMatrix()
            self.rotate = QtGui.QVector2D(0.0, 0.0)
            self.repaint()

    def initializeGL(self) :
        glEnable(GL_DEPTH_TEST)
        glPointSize(12)
        glLineWidth(2)

        self.transformIdentity()

        self.rotate =  QtGui.QVector2D(45.0, 45.0)
        self.bufRotate()

    def paintGL(self):
        glClearColor(1,1,1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0,0,self.width(), self.height())

        r = self.zoom * self.box.size()

        glMatrixMode(GL_MODELVIEW)
        glTranslatef(self.translate.x() * 2 * r, self.translate.y() * 2 * r,0)

        glMatrixMode(GL_PROJECTION);
        if self.width() > self.height() :
            k = self.width() / self.height()
            glOrtho(-r * k, r * k, -r, r, r * 50.0, -r * 50.0)
        else :
            k = self.height() / self.width()
            glOrtho(-r, r, -r * k, r * k, r * 50.0, -r * 50.0)

        self.loadRotate();
        center = -self.box.center()
        glTranslatef(center.x(), center.y(),center.z())


    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            if not e.modifiers() & QtCore.Qt.ALT :
                self.rotate -= QtGui.QVector2D(180.0 * (e.y() - self.mPPosition.y()) / self.edge, 0.0)
            if not e.modifiers() & QtCore.Qt.CTRL :
                self.rotate -= QtGui.QVector2D(0.0, 180.0 * (e.x() - self.mPPosition.x()) / self.edge)

            self.repaint()

            self.mPPosition = e.pos()
        elif e.buttons() & QtCore.Qt.MidButton:
            if not e.modifiers() & QtCore.Qt.ALT :
                self.translate -= QtGui.QVector2D(0.0, (e.y() - self.mPPosition.y()) / self.edge)
            if not e.modifiers() & QtCore.Qt.CTRL:
                self.translate += QtGui.QVector2D((e.x() - self.mPPosition.x()) / self.edge, 0.0)

            self.repaint()

            self.mPPosition = e.pos()

    def mouseReleaseEvent(self, *args, **kwargs):
        self.bufRotate()

    def mousePressEvent(self, e):
        if e.buttons() & (QtCore.Qt.LeftButton | QtCore.Qt.MidButton) :
            self.mPPosition = e.pos()

    def wheelEvent(self, e):
        if e.delta() > 0:
            self.zoom *= 0.9
        else:
            self.zoom /= 0.9
        self.repaint()