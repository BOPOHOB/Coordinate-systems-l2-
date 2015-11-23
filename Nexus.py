from CParallelepiped import CParallelepiped
from OpenGL.GL import *
from PySide import QtGui
from numpy import pi

class Nexus(CParallelepiped):
    def __init__(self, mobility):
        super().__init__(QtGui.QVector3D(-1, -1, 0))
        self.p2 = QtGui.QVector3D(1, 1, 10)
        self.mobility = mobility
        self.function = lambda x: x;
        if (type(mobility.value) == QtGui.QVector3D):
            self.view_transformation = lambda x: glTranslate((x * mobility.value).x(), (x * mobility.value).y(), (x * mobility.value).z())
        else:
            self.view_transformation = lambda x: glRotate(x, mobility.value.x(), mobility.value.y(), mobility.value.z())

    def setFunction(self, str):
        try:
            t = 0
            eval(str)
            self.apply_transformation = lambda t: self.view_transformation(eval(str))
            self.get_x = lambda t: eval(str)
        except:
            pass

    def get_transform_matrix(self, t : float):
        x = self.get_x(t)
        m = QtGui.QMatrix4x4()
        if (type(self.mobility.value) == QtGui.QVector3D):
            m.translate(x * self.mobility.value)
        else:
            m.rotate(x, self.mobility.value.vector())
        return m

    def draw(self):
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, -1.0);
        """bottom"""
        glVertex3f(self.p1.x(),self.p1.y(),self.p1.z())
        glVertex3f(self.p2.x(),self.p1.y(),self.p1.z())
        glVertex3f(self.p2.x(),self.p2.y(),self.p1.z())
        glVertex3f(self.p1.x(),self.p2.y(),self.p1.z())
        """top"""
        glVertex3f(self.p1.x(),self.p1.y(),self.p2.z())
        glVertex3f(self.p2.x(),self.p1.y(),self.p2.z())
        glVertex3f(self.p2.x(),self.p2.y(),self.p2.z())
        glVertex3f(self.p1.x(),self.p2.y(),self.p2.z())
        """sides"""
        glVertex3f(self.p1.x(),self.p1.y(),self.p1.z())
        glVertex3f(self.p2.x(),self.p1.y(),self.p1.z())
        glVertex3f(self.p2.x(),self.p1.y(),self.p2.z())
        glVertex3f(self.p1.x(),self.p1.y(),self.p2.z())

        glVertex3f(self.p2.x(),self.p2.y(),self.p1.z())
        glVertex3f(self.p2.x(),self.p1.y(),self.p1.z())
        glVertex3f(self.p2.x(),self.p1.y(),self.p2.z())
        glVertex3f(self.p2.x(),self.p2.y(),self.p2.z())

        glVertex3f(self.p2.x(),self.p2.y(),self.p1.z())
        glVertex3f(self.p1.x(),self.p2.y(),self.p1.z())
        glVertex3f(self.p1.x(),self.p2.y(),self.p2.z())
        glVertex3f(self.p2.x(),self.p2.y(),self.p2.z())

        glVertex3f(self.p1.x(),self.p1.y(),self.p1.z())
        glVertex3f(self.p1.x(),self.p2.y(),self.p1.z())
        glVertex3f(self.p1.x(),self.p2.y(),self.p2.z())
        glVertex3f(self.p1.x(),self.p1.y(),self.p2.z())

        glEnd()