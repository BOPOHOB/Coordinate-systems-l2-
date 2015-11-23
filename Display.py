from CGLWidget import CGLWidget
from CParallelepiped import CParallelepiped
from OpenGL.GL import *
from PySide import QtGui
from math import *


class Display(CGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.box = CParallelepiped(QtGui.QVector3D(40,40,40))
        self.box.include(QtGui.QVector3D(40,40,40))
        self.box.include(-QtGui.QVector3D(40,40,40))
        self.setMinimumWidth(200)
        self.t = 0.0

    def setData(self, data, enable_opengl_transformation):
        self.data = data
        self.gl_t = enable_opengl_transformation
        self.repaint()

    def initializeGL(self):
        super().initializeGL()
        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glEnable(GL_NORMALIZE)
        glEnable (GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        light1_diffuse = (GLfloat * 4)(14/255, 88/255, 228/255)
        light1_position = (GLfloat * 4)(0.0, 0.0, 1.0, 1.0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light1_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light1_position)

    def set_t(self, val):
        self.t = val
        self.repaint()

    def paintGL(self):
        super().paintGL()


        material_diffuse = (GLfloat * 4)(1.0, 0.5, 1.0, 1.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)

        def rrange(a,b,s):
            while(a <= b):
                yield a
                a += s

        glColor3ub(0xFF,0x00,0x00)
        if self.gl_t:
            for t in rrange(0,1,0.005):
                for i in self.data:
                    glPushMatrix()
                    i.apply_transformation(t)
                    glTranslatef(0.0,0.0,10.0)
                glBegin(GL_POINTS)
                glVertex3f(0.0,0.0,0.0)
                glEnd()
                for i in self.data:
                    glPopMatrix()
        else:
            glBegin(GL_LINE_STRIP)
            for t in rrange(0,1,0.005):
                m = QtGui.QMatrix4x4()
                for i in self.data:
                    m *= i.get_transform_matrix(t)
                    m.translate(0.0,0.0,10.0)
                v = m * QtGui.QVector3D(0,0,0)
                glVertex3f(v.x(),v.y(),v.z())
            glEnd()

        glColor3ub(0xFF,0x80,0x80)

        for i in self.data:
            glPushMatrix()
            i.apply_transformation(self.t)
            i.draw()
            glTranslatef(0.0,0.0,i.p2.z())
        for i in self.data:
            glPopMatrix()