from PySide.QtGui import QVector3D

class CParallelepiped:
    def __init__(self):
        self.p1 = QVector3D()
        self.p2 = QVector3D()

    def __init__(self, p):
        self.p1 = QVector3D(p)
        self.p2 = QVector3D(p)

    def include_x(self, v):
        self.p1.setX(min(self.p1.x(), v))
        self.p2.setX(max(self.p2.x(), v))

    def include_y(self, v):
        self.p1.setY(min(self.p1.y(), v))
        self.p2.setY(max(self.p2.y(), v))

    def include_z(self, v):
        self.p1.setZ(min(self.p1.z(), v))
        self.p2.setZ(max(self.p2.z(), v))

    def include(self, v):
        self.include_x(v.x())
        self.include_y(v.y())
        self.include_z(v.z())

    def size(self):
        return (self.p2 - self.p1).length()

    def center(self):
        return (self.p1 + self.p2) / 2