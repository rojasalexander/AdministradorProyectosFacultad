from re import I
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
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
        self.showMaximized()
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
    def __init__(self, nombreUser):
        super(Gui_access, self).__init__()
        loadUi('vistaproyectos.ui', self)
        widget.showMaximized() #fullscreen al entrar a la vista proyectos

        self.nombreUser = nombreUser
        self.proyectos = []
        self.currentProyecto = {}
        self.crp.hide()
        self.editarp.hide()
        self.eliminar.hide()
        # widget.move(100, 50) 
        # widget.setFixedHeight(700)    #se le asigna un tamaño fijo al widget
        # widget.setFixedWidth(1280)    #se le asigna un tamaño fijo al widget
        self.name.setText(nombreUser)
        
        self.botoMAS.clicked.connect(self.aggPopUp)

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

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
            
            btnActi = QPushButton(self.tableWidget)
            btnActi.setIcon(QIcon(actividadIcon))
            btnActi.setIconSize(QSize(25,25))
            btnActi.setStyleSheet("*{border-radius: 50%;}")
            btnActi.clicked.connect(lambda state, x=i: self.ventanaActi(x))
            self.tableWidget.setCellWidget(i, 4, btnActi)

            btn = QPushButton(self.tableWidget)
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(25,25))
            btn.setStyleSheet("*{border-radius: 50%;}")
            btn.clicked.connect(lambda state, x=i: self.editarPopup(x))
            self.tableWidget.setCellWidget(i, 5, btn)

            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(25,25))
            btn2.setStyleSheet("*{border-radius: 50%;}")
            btn2.clicked.connect(lambda state, x=i: self.deletePopup(x))
            self.tableWidget.setCellWidget(i, 6, btn2)

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
    
    def editarPopup(self, indice):
        self.currentProyecto = self.proyectos[indice]
        self.editarp.show()
        self.nom_2.setText(self.currentProyecto[1])
        self.des_2.setText(self.currentProyecto[3])
        self.fech_2.setText(self.currentProyecto[2])

    def ventanaActi(self, indice):
        self.currentProyecto = self.proyectos[indice]
        ventana3 = ventanaActividades(self.nombreUser, self.currentProyecto[0], self.currentProyecto[1])
        widget.addWidget(ventana3)  #para el cambio de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def editar(self):
        newProyecto = Proyecto(self.nom_2.text(), self.des_2.text(), self.fech_2.text())
        modify_proyecto(self.currentProyecto[0], newProyecto)
        self.loadData()
        self.editarp.hide()

    def cancelar(self):
        self.crp.hide()
        self.editarp.hide()
        self.eliminar.hide()

    def deletePopup(self, indice):
        self.eliminar.show()
        self.currentProyecto = self.proyectos[indice]
        self.nom_proy.setText(self.currentProyecto[1])

    def delete(self):
        id = self.currentProyecto[0]
        delete_proyecto(id)
        self.eliminar.hide()
        self.loadData()


class ventanaActividades(QDialog):
    def __init__(self, nombreUser, id_proyecto, nom_proyecto):
        super(ventanaActividades, self).__init__()
        loadUi('abrir.ui', self)
        self.nombreUser = nombreUser
        self.proy_name.setText(nom_proyecto)
        self.id_proyecto = id_proyecto
        self.actividades = []
        self.currentActividad = {}
        self.crear_act.hide()
        self.editar_act.hide()
        self.eliminar.hide()
        self.relacionar_w.hide()
        
        
        widget.move(100, 50)
        widget.setFixedHeight(700)    #se le asigna un tamaño fijo al widget
        widget.setFixedWidth(1280)    #se le asigna un tamaño fijo al widget

        self.botonMAS.clicked.connect(self.crearPopup)
        self.crear_actbtn.clicked.connect(self.crear)
        self.cancelarbtn_2.clicked.connect(self.cancelar)
        self.cancelarbtn_3.clicked.connect(self.cancelar)
        self.cancelarbtn_4.clicked.connect(self.cancelar)
        self.cancelarbtn_5.clicked.connect(self.cancelar)
        self.editar_btn.clicked.connect(self.editar)
        self.eliminarbtn.clicked.connect(self.delete)
        self.relacionarbtn.clicked.connect(self.relacionarPopup)
        self.relacionar_btn.clicked.connect(self.relacionar)
        self.volverbtn.clicked.connect(self.volver)

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i in range(1,7):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.loadData()

    def loadData(self):
        self.actividades = get_actividades(self.id_proyecto)
        self.tableWidget.setRowCount(len(self.actividades))
        for i in range(len(self.actividades)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.actividades[i][1]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.actividades[i][2])))

            btn = QPushButton(self.tableWidget)
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(25,25))
            btn.setStyleSheet("*{border-radius: 50%;}")
            btn.clicked.connect(lambda state, x=i: self.editarPopup(x))
            self.tableWidget.setCellWidget(i, 5, btn)

            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(25,25))
            btn2.setStyleSheet("*{border-radius: 50%;}")
            btn2.clicked.connect(lambda state, x=i: self.deletePopup(x))
            self.tableWidget.setCellWidget(i, 6, btn2)
    
    def crearPopup(self):
        self.crear_act.show()
        self.nom_2.setText('')
        self.dur_2.setText('')
        
    def crear(self):
        newActividad = Actividad(self.nom_2.text(), self.dur_2.text())
        create_actividad(newActividad, self.id_proyecto)
        self.loadData()
        self.crear_act.hide()

    def cancelar(self):
        self.crear_act.hide()
        self.editar_act.hide()
        self.eliminar.hide()
        self.relacionar_w.hide()

    def editarPopup(self, indice):
        self.currentActividad = self.actividades[indice]
        self.editar_act.show()
        self.nom_1.setText(self.currentActividad[1])
        self.dur.setText(str(self.currentActividad[2]))

    def editar(self):
        newActividad = Actividad(self.nom_1.text(), self.dur.text())
        modify_actividad(self.currentActividad[0], newActividad, self.id_proyecto)
        self.loadData()
        self.editar_act.hide()

    def deletePopup(self, indice):
        self.currentActividad = self.actividades[indice]
        self.nom_acti.setText(self.currentActividad[1])
        self.eliminar.show()

    def delete(self):
        id = self.currentActividad[0]
        delete_actividad(id, self.id_proyecto)
        self.eliminar.hide()
        self.loadData()

    def relacionarPopup(self):
        self.relacionar_w.show()
        for actividad in self.actividades:
            self.anterior_box.addItem(actividad[1])
            self.siguiente_box.addItem(actividad[1])


    def relacionar(self):
        self.relacionar_w.hide()
    
    def volver(self):
        ventana = Gui_access(self.nombreUser)
        widget.addWidget(ventana)  #para el cambio de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1)

def printear(indice):
    print("Hola mundo", indice)

app = QApplication(sys.argv) #inicializar la aplicacion
welcome = WelcomeScreen() #crear un objeto de la clase que creamos
widget = QtWidgets.QStackedWidget() #se crea un widget que va a contener todos los widgets, nos permite mover entre ellos
widget.addWidget(welcome) #agregar un widget al widget, se agrega la ventana
#widget.move(400, 80) #ponemos en la parte central de la pantalla
#widget.setFixedHeight(420)    #se le asigna un tamaño fijo al widget
#widget.setFixedWidth(380)    #se le asigna un tamaño fijo al widget
widget.show()

actividadIcon = QPixmap('acti-icon.png')
editIcon = QPixmap('edit-icon.png')
deleteIcon = QPixmap('delete-icon.png')

try:
    sys.exit(app.exec_())
except:
    print("Error")
