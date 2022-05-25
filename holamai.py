import sys
from turtle import width
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi

class WelcomeScreen(QMainWindow):
    def __init__(self):     #constructor
        super(WelcomeScreen, self).__init__()
        loadUi('disenho.ui', self) #importar el disenho de la interfaz

        self.bt_menu1.clicked.connect(self.mover_menu)      #permitir mostrar el menu de la parte izquierda
        self.bt_menu2.clicked.connect(self.mover_menu)      

        #ocultar botones
        self.bt_restaurar.hide()
        self.bt_menu2.hide()

        #sombra de los widgets
        self.sombra_frame(self.stackedWidget)
        self.sombra_frame(self.frame_superior)
        self.sombra_frame(self.toolBox)
        self.sombra_frame(self.bt_1)
        self.sombra_frame(self.bt_2)
        self.sombra_frame(self.bt_3)
        self.sombra_frame(self.bt_4)

        #control de barra de titulos
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_cerrar.clicked.connect(lambda: self.close()) #ejecutamos aca mismo el metodo close

        #eliminar barra y titulo - opacidad
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #size grip para redimencionar interfaz grafica
        self.gripSize = 10      #tam del frip
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)


        #mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        #acceder a las paginas
        self.bt_1.clicked.connect(self.pagina_uno)
        self.bt_2.clicked.connect(self.pagina_dos)
        self.bt_3.clicked.connect(self.pagina_tres)
        self.bt_4.clicked.connect(self.pagina_cuatro)

    def control_bt_minimizar(self):
        self.shorMinimized()

    def control_bt_maximizar(self): 
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()
    
    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()


    #metodo sombra
    def sombra_frame(self, frame): #frame a la cual asignarle la sombra
        sombra = QGraphicsDropShadowEffect(self) 
        sombra.setBlurRadius(30) #radio para especificar el anchoo de la sobra
        sombra.setXOffset(8)
        sombra.setYOffset(8)
        sombra.setColor(QColor(20,200,220,255)) # el color
        frame.setGraphicsEffect(sombra)

    #sizegrip redimencionar
    def resizeEvent(self, event):
        rect = self.rect() #coordenadas de donde se encuentra algo
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize) #
    
    #mover ventana
    def mousePressEvent(self, event): #presionamos 
        self.clickPosition =  event.globalPos() #obtenemos la posicion de la ventana
    
    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + (event.globalPos() - self.clickPosition))
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10: #si la posicion del mouse es menor a 10, al acercar a y=10 se pone en pantalla completa
            self.showMaximized()
            self.bt_maximizar.hide()
            self.bt_restaurar.show()
        else:
            self.showNormal()
            self.bt_restaurar.hide()
            self.bt_maximizar.show()

    # netidi oara niver el menu lateral izquierdo
    def mover_menu(self):
        if True:
            width = self.menu_lateral.width() #ancho del menu lateral
            normal = 0
            if width == 0:                      #si el ancho es 0
                extender = 300
                self.bt_menu2.hide()    #ocultar boton
                self.bt_menu1.show()    #mostrar boton y su menu
            else:
                self.bt_menu2.show()
                self.bt_menu1.hide()
                extender = normal
            self.animacion = QPropertyAnimation(self.menu_lateral, b"maximumWidth")
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setDuration(500)
            self.animacion.setEasingCurve(QEasingCurve.OutInBack)   #InQuad, InOutQuad, InCubic, InOutExpo, que efecto va a hacer ver documentacion
            self.animacion.start()

    #animacion de paginas
    def pagina_uno(self):
        self.stackedWidget.setCurrentWidget(self.pagina1)
        self.animacion_paginas()
    def pagina_dos(self):
        self.stackedWidget.setCurrentWidget(self.pagina2)
        self.animacion_paginas()
    def pagina_tres(self):
        self.stackedWidget.setCurrentWidget(self.pagina3)
        self.animacion_paginas()
    def pagina_cuatro(self):
        self.stackedWidget.setCurrentWidget(self.pagina4)
        self.animacion_paginas()
    
    def animacion_paginas(self): #obtenemos el tam de frame que contiene el frame 
        if True:
            width = self.stackedWidget.width()
            x1 = self.frame_paginas.rect().right()
            normal = 100
            if width == 100:
                extender = x1
            else:
                extender = normal
            
            self.animacion1 = QPropertyAnimation(self.stackedWidget, b"maximumWidth") #b es para que no se confunda con el metodo setMaximumWidth. b"geometry" Qrect(x,y,x1,y1)
            self.animacion1.setStartValue(width)
            self.animacion1.setEndValue(extender)
            self.animacion1.setDuration(500)
            self.animacion1.setEasingCurve(QEasingCurve.InOutBack)   #InQuad, InOutQuad, InCubic, InOutExpo
            self.animacion1.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = WelcomeScreen()
    mi_app.show()
    sys.exit(app.exec_())