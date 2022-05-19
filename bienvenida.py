import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow
#from messagebox import msg_error
from PyQt5.QtWidgets import QStackedWidget, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *

sys.path.append('database')
from proyectodata import *

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('ingrese.ui', self)
        self.ingre.clicked.connect(self.window_access)
    
    def gui_login(self):
        
        self.window_access()
    
    def window_access(self):
        self.name1 = self.lineEdit.text()
        print(self.lineEdit.text())
        ventana2 = Gui_access(self.name1)
        #widget = QStackedWidget()
        
        widget.addWidget(ventana2)  #para el cambio de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1)
        #widget.setFixedHeight(400)    #se le asigna un tamaño fijo al widget
        #widget.setFixedWidth(420)    #se le asigna un tamaño fijo al widget
        

class Gui_access(QDialog):
    def __init__(self, nombre):
        super(Gui_access, self).__init__()
        loadUi('chicos.ui', self)
        self.crp.hide()
        widget.move(100, 50) 
        widget.setFixedHeight(800)    #se le asigna un tamaño fijo al widget
        widget.setFixedWidth(1230)    #se le asigna un tamaño fijo al widget
        self.name.setText(nombre)
        #self.volver.clicked.connect(self.regresar_login)
        botonPrueba = QPushButton(self)
        botonPrueba.setGeometry(1100,700,51,51)

        proyectos = get_proyectos()
        self.tableWidget.setRowCount(len(proyectos))
        for i in range(len(proyectos)):
            self.tableWidget.setItem(i+1, 0, QtWidgets.QTableWidgetItem(proyectos[i][1]))
            self.tableWidget.setItem(i+1, 1, QtWidgets.QTableWidgetItem(proyectos[i][3]))
            # self.tableWidget.setItem(i+1, 0, proyectos[i][1])
            # self.tableWidget.setItem(i+1, 1, proyectos[i][3])
            
            btn = QPushButton(self.tableWidget)

            btn.setText('Eliminar')
            self.tableWidget.setCellWidget(i+1, 4, btn)

            btn2 = QPushButton(self.tableWidget)
            btn2.setText('Editar')
            self.tableWidget.setCellWidget(i+1, 5, btn2)

        

        addIcon = QPixmap('add-icon.png')
        botonPrueba.setIcon(QIcon(addIcon))
        botonPrueba.setIconSize(QSize(50,50))
        botonPrueba.setStyleSheet(
            "*{border-radius: 50%;}")
        botonPrueba.clicked.connect(self.agg)
    
    def regresar_login(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.move(400, 80)
        widget.setFixedHeight(500)    #se le asigna un tamaño fijo al widget
        widget.setFixedWidth(500)    #se le asigna un tamaño fijo al widget
    
    def agg(self):
        self.crp.show()
        self.nom.setText('')
        self.des.setText('')
        self.fech.setText('')
        self.crearbtn.clicked.connect(self.crear)
        self.cancelarbtn.clicked.connect(self.cancelar)
        
    def crear(self):
        print(self.nom.text(), self.des.text(), self.fech.text())
        self.crp.hide()

    def cancelar(self):
        self.crp.hide()


app = QApplication(sys.argv) #inicializar la aplicacion
welcome = WelcomeScreen() #crear un objeto de la clase que creamos
widget = QtWidgets.QStackedWidget() #se crea un widget que va a contener todos los widgets, nos permite mover entre ellos
widget.addWidget(welcome) #agregar un widget al widget, se agrega la ventana
widget.move(400, 80) #ponemos en la parte central de la pantalla
widget.setFixedHeight(420)    #se le asigna un tamaño fijo al widget
widget.setFixedWidth(380)    #se le asigna un tamaño fijo al widget
#widget.setWindowFlags(QtCore.Qt.FramelessWindowHint) #quitar bordes
#widget.setAttribute(QtCore.Qt.WA_TranslucentBackground) #translucido
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Error")
