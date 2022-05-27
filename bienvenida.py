import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
#from messagebox import msg_error
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import *

#sys.path.append('database')
from database.proyectodata import *
from packages.proyecto import *
from gantt2 import *

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        #self.showMaximized()
        loadUi('ui/fabri.ui', self)
        self.ingre.clicked.connect(self.window_access)
    
    def gui_login(self):
        self.window_access()
    
    def window_access(self):
        self.name = self.nameLine.text()
        ventana2 = Gui_access(self.name)
        #widget = QStackedWidget()
        
        widget.addWidget(ventana2)  #para el cambio de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1)

        

class Gui_access(QDialog):
    def __init__(self, nombreUser):
        super(Gui_access, self).__init__()
        loadUi('ui/vistaproyectosmai.ui', self)

        self.nombreUser = nombreUser
        self.proyectos = []
        self.currentProyecto = {}
        self.fechaInicio = ''
        self.crp.hide()
        self.editarp.hide()
        self.eliminar.hide()
        self.calendarioW.hide()
        widget.move(300, 100) 
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
        self.calendarbtn.clicked.connect(self.calendarioPopup)
        self.calendarbtn_2.clicked.connect(self.calendarioPopup)
        self.seleccionarbtn.clicked.connect(self.selectFecha)
        self.cancelarbtn_4.clicked.connect(self.cancelarCalendario)

        self.loadData()
        
    
    def loadData(self):
        self.proyectos = get_proyectos()
        print(self.proyectos)
        self.tableWidget.setRowCount(len(self.proyectos))
        for i in range(len(self.proyectos)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.proyectos[i].nombre))
            self.tableWidget.item(i, 0).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.proyectos[i].descripcion))
            self.tableWidget.item(i, 1).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.proyectos[i].fechaInicio))
            self.tableWidget.item(i, 2).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(self.proyectos[i].fechaFin))
            self.tableWidget.item(i, 3).setForeground(QBrush(QColor(213, 213, 213)))
            
            btnActi = QPushButton(self.tableWidget)
            btnActi.setIcon(QIcon(actividadIcon))
            btnActi.setIconSize(QSize(35,35))
            btnActi.setStyleSheet("*{border-radius: 50%;}")
            btnActi.clicked.connect(lambda state, x=i: self.ventanaActi(x))
            self.tableWidget.setCellWidget(i, 4, btnActi)

            btn = QPushButton(self.tableWidget)
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(35,35))
            btn.setStyleSheet("*{border-radius: 50%;}")
            btn.clicked.connect(lambda state, x=i: self.editarPopup(x))
            self.tableWidget.setCellWidget(i, 5, btn)

            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(35,35))
            btn2.setStyleSheet("*{border-radius: 50%;}")
            btn2.clicked.connect(lambda state, x=i: self.deletePopup(x))
            self.tableWidget.setCellWidget(i, 6, btn2)
    
    def aggPopUp(self):
        self.crp.show()
        self.nom.setText('')
        self.des.setText('')

        self.fechaInicio = str(date.today())
        self.fechaIniLabel.setText(self.fechaInicio)
        self.fechaIniLabel_2.setText('')
        
    def crear(self):
        newProyecto = Proyecto(self.nom.text(), self.des.text(), date.fromisoformat(self.fechaInicio))
        create_proyecto(newProyecto)
        self.loadData()
        self.crp.hide()
    
    def editarPopup(self, indice):
        self.currentProyecto = self.proyectos[indice]
        self.editarp.show()
        self.nom_2.setText(self.currentProyecto.nombre)
        self.des_2.setText(self.currentProyecto.descripcion)
        self.fechaInicio = self.currentProyecto.fechaInicio
        self.fechaIniLabel_2.setText(self.fechaInicio)
        self.fechaIniLabel.setText('')

    def editar(self):
        newProyecto = Proyecto(self.nom_2.text(), self.des_2.text(), date.fromisoformat(self.fechaInicio))
        modify_proyecto(self.currentProyecto.identificador, newProyecto)
        self.loadData()
        self.editarp.hide()

    def ventanaActi(self, indice):
        self.currentProyecto = self.proyectos[indice]
        ventana3 = ventanaActividades(self.nombreUser, self.currentProyecto.identificador, self.currentProyecto.nombre)
        widget.addWidget(ventana3)  #para el cambio de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def cancelar(self):
        self.crp.hide()
        self.editarp.hide()
        self.eliminar.hide()

    def deletePopup(self, indice):
        self.eliminar.show()
        self.currentProyecto = self.proyectos[indice]
        self.nom_proy.setText(self.currentProyecto.nombre)

    def delete(self):
        id = self.currentProyecto.identificador
        delete_proyecto(id)
        self.eliminar.hide()
        self.loadData()

    def calendarioPopup(self):
        self.calendarioW.show()
        fecha = self.fechaInicio.split('-')
        date = QDate(int(fecha[0]), int(fecha[1]), int(fecha[2]))
        self.calendario.setSelectedDate(date)

    def selectFecha(self):
        fecha = self.calendario.selectedDate()
        self.fechaInicio = date.isoformat(fecha.toPyDate())
        
        if(self.fechaIniLabel.text() != ''):
            self.fechaIniLabel.setText(self.fechaInicio)
        else:
            self.fechaIniLabel_2.setText(self.fechaInicio)
        self.calendarioW.hide()

    def cancelarCalendario(self):
        self.calendarioW.hide()
        

class ventanaActividades(QDialog):
    def __init__(self, nombreUser, id_proyecto, nom_proyecto):
        super(ventanaActividades, self).__init__()
        loadUi('ui/abrirMAIA.ui', self)
        self.nombreUser = nombreUser
        self.proy_name.setText(nom_proyecto)
        self.id_proyecto = id_proyecto
        self.actividades = []
        self.currentActividad = {}
        self.crear_act.hide()
        self.editar_act.hide()
        self.eliminar.hide()
        self.relacionar_w.hide()
        self.desrelacionar_w.hide()
        
        widget.move(300, 100)
        #widget.setFixedHeight(700)    #se le asigna un tamaño fijo al widget
        #widget.setFixedWidth(1280)    #se le asigna un tamaño fijo al widget

        self.agregarActiBtn.clicked.connect(self.crearPopup)
        self.crear_actbtn.clicked.connect(self.crear)
        self.cancelarbtn_2.clicked.connect(self.cancelar)
        self.cancelarbtn_3.clicked.connect(self.cancelar)
        self.cancelarbtn_4.clicked.connect(self.cancelar)
        self.cancelarbtn_5.clicked.connect(self.cancelar)
        self.cancelarbtn_6.clicked.connect(self.cancelar)
        self.editar_btn.clicked.connect(self.editar)
        self.eliminarbtn.clicked.connect(self.delete)
        self.relacionarbtn.clicked.connect(self.relacionarPopup)
        self.relacionar_btn.clicked.connect(self.relacionar)
        self.volverbtn.clicked.connect(self.volver)
        self.desrelacionarP.clicked.connect(self.desrelacionarPopup)
        self.desrelacionar_btn.clicked.connect(self.desrelacionar)
        self.grafobtn.clicked.connect(self.verGrafo)
        self.actualizarbtn_2.clicked.connect(self.calcularCamino)
        self.diagramabtn.clicked.connect(self.verDiagrama)
        

        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i in range(1,7):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.loadData()

    def loadData(self):
        self.actividades = get_actividades(self.id_proyecto)
        self.tableWidget.setRowCount(len(self.actividades))
        for i in range(len(self.actividades)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.actividades[i].nombre))
            self.tableWidget.item(i, 0).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.actividades[i].duracion)))
            self.tableWidget.item(i, 1).setForeground(QBrush(QColor(213, 213, 213)))

            btn = QPushButton(self.tableWidget)
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(35,35))
            btn.setStyleSheet("*{border-radius: 50%;}")
            btn.clicked.connect(lambda state, x=i: self.editarPopup(x))
            self.tableWidget.setCellWidget(i, 5, btn)

            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(35,35))
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
        self.desrelacionar_w.hide()

    def editarPopup(self, indice):
        self.currentActividad = self.actividades[indice]
        self.editar_act.show()
        self.nom_1.setText(self.currentActividad.nombre)
        self.dur.setText(str(self.currentActividad.duracion))

    def editar(self):
        newActividad = Actividad(self.nom_1.text(), self.dur.text())
        modify_actividad(self.currentActividad.identificador, newActividad, self.id_proyecto)
        self.loadData()
        self.editar_act.hide()

    def deletePopup(self, indice):
        self.currentActividad = self.actividades[indice]
        self.nom_acti.setText(self.currentActividad.nombre)
        self.eliminar.show()

    def delete(self):
        id = self.currentActividad.identificador
        delete_actividad(id, self.id_proyecto)
        self.eliminar.hide()
        self.loadData()

    def relacionarPopup(self):
        self.relacionar_w.show()
        # self.anterior_box.activated[str].connect(self.onChangeAnterior)
        # self.siguiente_box.activated[str].connect(self.onChangeSiguiente)
        self.anterior_box.clear()
        self.siguiente_box.clear()
        for actividad in self.actividades:
            self.anterior_box.addItem(actividad.nombre)
            self.siguiente_box.addItem(actividad.nombre)
        
        #self.siguiente_box.setCurrentIndex(1)


    def relacionar(self):
        self.relacionar_w.hide()

        anteriorIndex = self.anterior_box.currentIndex()
        siguienteIndex = self.siguiente_box.currentIndex()

        anteriorId = self.actividades[anteriorIndex].identificador
        siguienteId = self.actividades[siguienteIndex].identificador

        newRelacion = Relacion(anteriorId, siguienteId)
        create_relacion(newRelacion, self.id_proyecto)

        self.loadData()

    def desrelacionarPopup(self):
        self.desrelacionar_w.show()
        self.relacion_box.clear()
        relaciones = get_relaciones(self.id_proyecto)

        for relacion in relaciones:
            anterior = get_actividad_by_id(relacion.actividadPrecedente, self.id_proyecto)
            siguiente = get_actividad_by_id(relacion.actividadSiguiente, self.id_proyecto)
            nomAnterior = anterior.nombre
            nomSiguiente = siguiente.nombre
            self.relacion_box.addItem(f"{nomAnterior} -> {nomSiguiente}")
        
    def desrelacionar(self):
        relaciones = get_relaciones(self.id_proyecto)
        index = self.relacion_box.currentIndex()
        id = relaciones[index].identificador
        delete_relacion(id, self.id_proyecto)
        self.loadData()
        self.desrelacionar_w.hide()
    
    def verGrafo(self):
        proy = get_proyecto_by_id(self.id_proyecto)
        print(proy)
        proy.actualizar_bd()
        proy.mostrar_grafo()

    def verDiagrama(self):
        proy = get_proyecto_by_id(self.id_proyecto)
        print(proy)
        proy.actualizar_bd()
        proy.actualizarCsv()
        mostrar_gantt()
    
    def calcularCamino(self):
        print()
    
    def volver(self):
        ventana = Gui_access(self.nombreUser)
        widget.addWidget(ventana)  #para el cambio de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1)

app = QApplication(sys.argv) #inicializar la aplicacion
welcome = WelcomeScreen() #crear un objeto de la clase que creamos
widget = QtWidgets.QStackedWidget() #se crea un widget que va a contener todos los widgets, nos permite mover entre ellos
widget.addWidget(welcome) #agregar un widget al widget, se agrega la ventana
widget.move(400, 80) #ponemos en la parte central de la pantalla
#widget.setFixedHeight(420)    #se le asigna un tamaño fijo al widget
#widget.setFixedWidth(380)    #se le asigna un tamaño fijo al widget
widget.show()

actividadIcon = QPixmap('icons/acti-icon.png')
editIcon = QPixmap('icons/edit-icon.png')
deleteIcon = QPixmap('icons/delete-icon.png')

try:
    sys.exit(app.exec_())
except:
    print("Error")
