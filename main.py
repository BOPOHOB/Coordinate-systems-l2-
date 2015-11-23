import sys
from PySide import QtGui
from PySide import QtCore
from enum import Enum
from random import randint
from Nexus import Nexus
from Display import Display

class Mobility(Enum):
    tx = QtGui.QVector3D(1,0,0)
    ty = QtGui.QVector3D(0,1,0)
    tz = QtGui.QVector3D(0,0,1)
    rx = QtGui.QQuaternion(0, 1,0,0)
    ry = QtGui.QQuaternion(0, 0,1,0)
    rz = QtGui.QQuaternion(0, 0,0,1)

bench_mark = [
    {
        'mobility' : Mobility.rz,
        'polynom' : 1
    },
    {
        'mobility' : Mobility.ry,
        'polynom' : 2
    },
    {
        'mobility' : Mobility.tx,
        'polynom' : 3
    },
    {
        'mobility' : Mobility.rx,
        'polynom' : 3
    }
]

class Face(QtGui.QWidget):
    def __init__(self, enable_opengl_transformation : bool = False, parent = None):
        super().__init__(parent)
        p = self.palette()
        p.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
        self.setPalette(p)
        self.setLayout(QtGui.QHBoxLayout())
        display = Display(self)
        display.setData([Nexus(i['mobility']) for i in bench_mark], enable_opengl_transformation)
        self.layout().addWidget(display, 5)
        imputsLayout = QtGui.QVBoxLayout()
        self.layout().addLayout(imputsLayout)
        for i in range(0,len(bench_mark)):
            le = QtGui.QLineEdit(self)
            lo = QtGui.QHBoxLayout()
            lo.addWidget(QtGui.QLabel("Закон движения в закреплении звена #{}".format(i + 1), self))
            lo.addWidget(le)
            """
            if (bench_mark[i]['polynom'] == 1):
                le.setText("{}*t + {}".format(randint(1,100),0))
            elif (bench_mark[i]['polynom'] == 2):
                le.setText("{}*t**2+{}*t + {}".format(randint(1,100),randint(1,100),0))
            elif (bench_mark[i]['polynom'] == 3):
                le.setText("{}*t**3+{}*t**2+{}*t + {}".format(randint(1,100),randint(1,100),randint(1,100),0))
            """
            if (i == 0):
                le.setText("720*t")
            elif (i == 1):
                le.setText("540*t*t")
            elif (i == 2):
                le.setText("1-(t*2-1)**2")
            elif (i == 3):
                le.setText("t*900")
            display.data[i].setFunction(le.text())
            le.textEdited.connect(display.data[i].setFunction)
            le.textEdited.connect(display.repaint)
            imputsLayout.addLayout(lo)

        lo = QtGui.QHBoxLayout()
        lo.addWidget(QtGui.QLabel("Время", self))
        dial = QtGui.QSlider(self)
        dial.setMinimum(0.0)
        dial.setOrientation(QtCore.Qt.Horizontal)
        dial.setMaximum(1000.0)
        valDisplay = QtGui.QLabel(self)
        valDisplay.set_value = lambda s: valDisplay.setText("{:0<#5}".format(s / dial.maximum()))
        valDisplay.set_value(0.0)
        dial.valueChanged.connect(valDisplay.set_value)
        dial.valueChanged.connect(lambda s: display.set_t(s / dial.maximum()))
        lo.addWidget(dial)
        lo.addWidget(valDisplay)
        imputsLayout.addLayout(lo)
        imputsLayout.addStretch(10)

a = QtGui.QApplication(sys.argv)

w = Face(enable_opengl_transformation = False)
w.showMaximized()
a.exec_()
