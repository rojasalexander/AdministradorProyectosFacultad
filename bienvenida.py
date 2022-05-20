import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow
#from messagebox import msg_error
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#sys.path.append('database')
from database.proyectodata import *
from packages.proyecto import *

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('ingrese2.ui', self)
        self.ingre.clicked.connect(self.window_access)
    
    def gui_login(self):
        self.window_access()
    
    def window_access(self):
        self.name1 = self.lineEdit.text()
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
        self.proyectos = []
        self.currentProyecto = {}
        self.crp.hide()
        self.crp_2.hide()
        self.eliminar.hide()
        widget.move(100, 50) 
        widget.setFixedHeight(800)    #se le asigna un tamaño fijo al widget
        widget.setFixedWidth(1230)    #se le asigna un tamaño fijo al widget
        self.name.setText(nombre)
        
        botonPrueba = QPushButton(self)
        botonPrueba.setGeometry(1100,700,51,51)
        
        addIcon = QPixmap('add-icon.png')
        botonPrueba.setIcon(QIcon(addIcon))
        botonPrueba.setIconSize(QSize(50,50))
        botonPrueba.setStyleSheet(
            "*{border-radius: 50%;}")
        botonPrueba.clicked.connect(self.aggPopUp)

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.crearbtn.clicked.connect(self.crear)
        self.cancelarbtn.clicked.connect(self.cancelar)
        self.eliminarbtn.clicked.connect(self.delete)
        self.cancelarbtn_2.clicked.connect(self.cancelar)
        self.editarbtn.clicked.connect(self.editar)
        self.cancelarbtn_3.clicked.connect(self.cancelar)

        self.loadData()
        
    
    def loadData(self):
        self.proyectos = get_proyectos()
        self.tableWidget.setRowCount(len(self.proyectos))
        for i in range(len(self.proyectos)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.proyectos[i][1]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.proyectos[i][3]))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.proyectos[i][2]))
            
            btn = QPushButton(self.tableWidget)
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(25,25))
            btn.setStyleSheet("*{border-radius: 50%;}")
            btn.clicked.connect(lambda state, x=i: self.editarPopUp(x))
            self.tableWidget.setCellWidget(i, 3, btn)

            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(25,25))
            btn2.setStyleSheet("*{border-radius: 50%;}")
            btn2.clicked.connect(lambda state, x=i: self.deletePopUp(x))
            self.tableWidget.setCellWidget(i, 4, btn2)

    def regresar_login(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.move(400, 80)
        widget.setFixedHeight(500)    #se le asigna un tamaño fijo al widget
        widget.setFixedWidth(500)    #se le asigna un tamaño fijo al widget
    
    def aggPopUp(self):
        self.crp.show()
        self.nom.setText('')
        self.des.setText('')
        self.fech.setText('')
        
    def crear(self):
        newProyecto = Proyecto(self.nom.text(), self.des.text(), self.fech.text())
        create_proyecto(newProyecto)
        self.loadData()
        self.crp.hide()
    
    def editarPopUp(self, indice):
        self.currentProyecto = self.proyectos[indice]
        self.crp_2.show()
        self.nom_2.setText(self.currentProyecto[1])
        self.des_2.setText(self.currentProyecto[3])
        self.fech_2.setText(self.currentProyecto[2])

    def editar(self):
        newProyecto = Proyecto(self.nom_2.text(), self.des_2.text(), self.fech_2.text())
        modify_proyecto(self.currentProyecto[0], newProyecto)
        self.loadData()
        self.crp_2.hide()

    def cancelar(self):
        self.crp.hide()
        self.crp_2.hide()
        self.eliminar.hide()

    def deletePopUp(self, indice):
        self.eliminar.show()
        self.currentProyecto = self.proyectos[indice]
        self.nom_proy.setText(self.currentProyecto[1])

    def delete(self):
        id = self.currentProyecto[0]
        delete_proyecto(id)
        self.eliminar.hide()
        self.loadData()



def printear(indice):
    print("Hola mundo", indice)

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

editIcon = QPixmap('edit-icon.png')
deleteIcon = QPixmap('delete-icon.png')
try:
    sys.exit(app.exec_())
except:
    print("Error")
