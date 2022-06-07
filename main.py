import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import *
from database.proyectodata import *
from database.feriadodata import *
from packages.proyecto import *
from gantt2 import *

# Clase para la ventana de bienvenida
class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi('ui/fabri.ui', self) #carga la interfaz
        self.ingre.clicked.connect(self.window_access) #relacionar boton con funcion correspondiente
    
    def window_access(self):
        self.name = self.nameLine.text()
        ventana2 = ventanaProyectos(self.name)
        
        widget.addWidget(ventana2)  #agregamos la ventana al widget
        widget.setCurrentIndex(widget.currentIndex() + 1) #cambiamos de ventana

# Clase para la ventana de proyectos
class ventanaProyectos(QDialog):
    def __init__(self, nombreUser):
        super(ventanaProyectos, self).__init__()
        loadUi('ui/vistaproyectosmai.ui', self) #carga la interfaz

        #inicializacion de variables
        self.nombreUser = nombreUser
        self.proyectos = []
        self.currentProyecto = {}
        self.fechaInicio = ''
        self.name.setText(nombreUser)

        #ocultamos los popups
        self.crp.hide()
        self.editarp.hide()
        self.eliminar.hide()
        self.calendarioW.hide()

        widget.move(0, 0) #mover la ventana 
        
        #ajustamos el tamaño de las columnas de la tabla
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

        #relacionamos los botones con sus funciones correspondientes
        self.botoMAS.clicked.connect(self.aggPopUp)
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
        self.botoFERIADO.clicked.connect(self.feriado)
        self.pushButton_4.clicked.connect(self.buscar)

        self.tableWidget.verticalHeader().setVisible(False) #ocultar la cabecera de enumeracion de la tabla
        self.loadData() #mostramos los datos en la tabla 
    
    #funcion para mostrar los datos de la base de datos
    def loadData(self, busqueda = ''):
        #traemos los proyectos de la base de datos mediante un get con un keyword 'busqueda'
        #si el keyword esta vacio trae todos los proyectos, si no, trae los proyectos que coincidan con el keyword
        self.proyectos = buscar_proyectos(busqueda)
        self.tableWidget.setRowCount(len(self.proyectos)) #establecemos el numero de filas de la tabla
        for i in range(len(self.proyectos)):
            #establecemos los datos de cada fila
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.proyectos[i].nombre))
            self.tableWidget.item(i, 0).setForeground(QBrush(QColor(213, 213, 213))) #establecemos el color de la letra
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.proyectos[i].descripcion))
            self.tableWidget.item(i, 1).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.proyectos[i].fechaInicio))
            self.tableWidget.item(i, 2).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(self.proyectos[i].fechaFin))
            self.tableWidget.item(i, 3).setForeground(QBrush(QColor(213, 213, 213)))
            
            #establecemos botones de acciones para cada fila
            #boton para ver actividades del proyecto
            btnActi = QPushButton(self.tableWidget)
            btnActi.setIcon(QIcon(actividadIcon))
            btnActi.setIconSize(QSize(25,25))
            btnActi.setStyleSheet("*{border-radius: 50%;}") #estilo del boton
            #relacionamos el boton con la funcion correspondiente
            btnActi.clicked.connect(lambda state, x=i: self.ventanaActi(x)) 
            self.tableWidget.setCellWidget(i, 4, btnActi) #establecemos el boton en la celda

            #boton para editar el proyecto
            btn = QPushButton(self.tableWidget)
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(25,25))
            btn.setStyleSheet("*{border-radius: 50%;}") #estilo del boton
            #relacionamos el boton con la funcion correspondiente
            btn.clicked.connect(lambda state, x=i: self.editarPopup(x)) 
            self.tableWidget.setCellWidget(i, 5, btn) #establecemos el boton en la celda

            #boton para eliminar el proyecto
            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(25,25))
            btn2.setStyleSheet("*{border-radius: 50%;}") #estilo del boton
            #relacionamos el boton con la funcion correspondiente
            btn2.clicked.connect(lambda state, x=i: self.deletePopup(x)) 
            self.tableWidget.setCellWidget(i, 6, btn2) #establecemos el boton en la celda
    
    #funcion para mostrar el popup de agregar proyecto
    def aggPopUp(self):
        self.crp.show() #mostramos el popup
        #incializamos los campos del popup
        self.nom.setText('')
        self.des.setText('')
        self.lunesBox.setChecked(False)
        self.martesBox.setChecked(False)
        self.miercolesBox.setChecked(False)
        self.juevesBox.setChecked(False)
        self.viernesBox.setChecked(False)
        self.sabadoBox.setChecked(False)
        self.domingoBox.setChecked(False)
        #establecemos la fecha de inicio como el dia actual
        self.fechaInicio = str(date.today())
        self.fechaIniLabel.setText(self.fechaInicio) #mostramos la fecha de inicio
        self.fechaIniLabel_2.setText('')
        
    #funcion para crear el proyecto en base de datos
    def crear(self):
        diasNoLaborales = [] #lista de los dias no laborales
        #si el dia no laboral esta seleccionado, agregamos el dia a la lista
        if self.lunesBox.isChecked():
            diasNoLaborales.append(0)
        if self.martesBox.isChecked():
            diasNoLaborales.append(1)
        if self.miercolesBox.isChecked():
            diasNoLaborales.append(2)
        if self.juevesBox.isChecked():
            diasNoLaborales.append(3)
        if self.viernesBox.isChecked():
            diasNoLaborales.append(4)
        if self.sabadoBox.isChecked():
            diasNoLaborales.append(5)
        if self.domingoBox.isChecked():
            diasNoLaborales.append(6)
        
        #creamos una nueva clase proyecto con los datos ingresados del popup
        newProyecto = Proyecto(self.nom.text(), self.des.text(), self.fechaInicio, noLaborales=diasNoLaborales)
        create_proyecto(newProyecto) #creamos el proyecto en base de datos
        self.loadData() #actualizamos la tabla
        self.crp.hide() #ocultamos el popup
    
    #funcion para mostrar el popup de editar proyecto
    def editarPopup(self, indice):
        self.editarp.show() #mostramos el popup
        self.currentProyecto = self.proyectos[indice] #establecemos el proyecto actual
        #incializamos los campos del popup con los datos del proyecto actual
        self.nom_2.setText(self.currentProyecto.nombre) 
        self.des_2.setText(self.currentProyecto.descripcion)
        self.fechaInicio = self.currentProyecto.fechaInicio
        self.fechaIniLabel_2.setText(self.fechaInicio)
        self.fechaIniLabel.setText('')
        
        #establecemos los dias no laborales del proyecto actual
        if 0 in self.currentProyecto.noLaborales:
            self.lunesBox_3.setChecked(True)
        if 1 in self.currentProyecto.noLaborales:
            self.martesBox_3.setChecked(True)
        if 2 in self.currentProyecto.noLaborales:
            self.miercolesBox_3.setChecked(True)
        if 3 in self.currentProyecto.noLaborales:
            self.juevesBox_3.setChecked(True)
        if 4 in self.currentProyecto.noLaborales:
            self.viernesBox_3.setChecked(True)
        if 5 in self.currentProyecto.noLaborales:
            self.sabadoBox_3.setChecked(True)
        if 6 in self.currentProyecto.noLaborales:
            self.domingoBox_3.setChecked(True)

    #funcion para editar el proyecto en base de datos
    def editar(self):
        diasNoLaborales = [] #lista de los dias no laborales
        #si el dia no laboral esta seleccionado, agregamos el dia a la lista
        if self.lunesBox.isChecked():
            diasNoLaborales.append(0)
        if self.martesBox.isChecked():
            diasNoLaborales.append(1)
        if self.miercolesBox.isChecked():
            diasNoLaborales.append(2)
        if self.juevesBox.isChecked():
            diasNoLaborales.append(3)
        if self.viernesBox.isChecked():
            diasNoLaborales.append(4)
        if self.sabadoBox.isChecked():
            diasNoLaborales.append(5)
        if self.domingoBox.isChecked():
            diasNoLaborales.append(6)
        #creamos una nueva clase proyecto con los datos ingresados del popup
        newProyecto = Proyecto(self.nom_2.text(), self.des_2.text(), self.fechaInicio, noLaborales=diasNoLaborales)
        modify_proyecto(self.currentProyecto.identificador, newProyecto) #modificamos el proyecto en base de datos
        self.loadData() #actualizamos la tabla
        self.editarp.hide() #ocultamos el popup

    #funcion para mostrar la ventana de actividades de proyecto
    def ventanaActi(self, indice):
        self.currentProyecto = self.proyectos[indice] #establecemos el proyecto actual
        ventana3 = ventanaActividades(self.nombreUser, self.currentProyecto) #nueva ventana de actividades
        widget.addWidget(ventana3)  #agregamos la ventana a la lista de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1) #mostramos la ventana

    #funcion del boton cancelar de los popup
    def cancelar(self):
        #ocultamos los popups
        self.crp.hide()
        self.editarp.hide()
        self.eliminar.hide()

    #funcion para mostrar el popup de eliminar proyecto
    def deletePopup(self, indice):
        self.eliminar.show() #mostramos el popup
        self.currentProyecto = self.proyectos[indice] #establecemos el proyecto actual
        self.nom_proy.setText(self.currentProyecto.nombre) #mostramos el nombre del proyecto actual

    #funcion para eliminar el proyecto en base de datos
    def delete(self):
        id = self.currentProyecto.identificador #obtenemos el id del proyecto actual
        delete_proyecto(id) #eliminamos el proyecto en base de datos
        self.eliminar.hide() #ocultamos el popup
        self.loadData() #actualizamos la tabla

    #funcion para mostrar el popup del calendario
    def calendarioPopup(self):
        self.calendarioW.show() #mostramos el popup
        fecha = self.fechaInicio.split('-') #separamos la fecha de inicio en una lista
        date = QDate(int(fecha[0]), int(fecha[1]), int(fecha[2])) #creamos una nueva fecha con los datos de la fecha de inicio
        self.calendario.setSelectedDate(date) #seleccionamos la fecha de inicio en el calendario

    #funcion para cambiar la fecha de inicio del proyecto
    def selectFecha(self):
        fecha = self.calendario.selectedDate() #obtenemos la fecha seleccionada en el calendario
        self.fechaInicio = date.isoformat(fecha.toPyDate()) #convertimos la fecha a un formato de fecha
        
        if(self.fechaIniLabel.text() != ''): 
            self.fechaIniLabel.setText(self.fechaInicio) #mostramos la fecha en el label de crear proyecto
        else:
            self.fechaIniLabel_2.setText(self.fechaInicio) #mostramos la fecha en el label de editar proyecto
        
        self.calendarioW.hide() #ocultamos el popup

    #funcion para ocultar el popup del calendario
    def cancelarCalendario(self):
        self.calendarioW.hide() #ocultamos el popup

    #funcion para mostrar la ventana de feriados de los proyectos
    def feriado(self):
        ventana4 = ventanaFeriados(self.nombreUser) #creamos una nueva ventana de feriados
        widget.addWidget(ventana4)  #agregamos la ventana a la lista de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1) #cambiamos la ventana

    #funcion para accionar el buscador de proyectos
    def buscar(self):
        self.loadData(self.lineEdit.text()) #cargamos los datos de la tabla con el texto ingresado en el buscador
        self.lineEdit.setText('') #limpiamos el buscador

# Clase para la ventana de feriados
class ventanaFeriados(QDialog):
    def __init__(self, nombreUser):
        super(ventanaFeriados, self).__init__()
        loadUi('ui/vistaferiados.ui', self) #cargamos la interfaz grafica
        #inicializamos los componentes de la ventana
        self.nombreUser = nombreUser
        self.feriados = []
        self.currentFeriado = {}
        #ocultamos los popups
        self.calendarioW.hide()
        self.eliminar.hide()

        widget.move(0, 0) #posicionamos la ventana 
        
        #relacionamos los botones con sus funciones correspondientes
        self.botoMAS.clicked.connect(self.aggPopUp)
        self.botoMAS_2.clicked.connect(self.volver)
        self.eliminarbtn.clicked.connect(self.delete)
        self.cancelarbtn_2.clicked.connect(self.cancelar)
        self.seleccionarbtn.clicked.connect(self.crear)
        self.cancelarbtn_4.clicked.connect(self.cancelar)

        self.tableWidget.verticalHeader().setVisible(False) #ocultamos la cabecera de enumeracion de la tabla
        self.loadData() #cargamos los datos de la tabla
        
    #funcion para cargar los datos de la tabla feriados
    def loadData(self):
        self.feriados = get_feriados() #obtenemos los feriados de la base de datos
        self.tableWidget.setRowCount(len(self.feriados)) #establecemos la cantidad de filas de la tabla
        for i in range(len(self.feriados)):
            #establecemos los datos de la tabla
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.feriados[i]))
            self.tableWidget.item(i, 0).setForeground(QBrush(QColor(213, 213, 213))) #establecemos el color de la letra

            #establecemos las acciones de los botones de la tabla
            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(25,25))
            btn2.setStyleSheet("*{border-radius: 50%;}") #establecemos el estilo del boton
            btn2.clicked.connect(lambda state, x=i: self.deletePopup(x)) #establecemos la funcion del boton
            self.tableWidget.setCellWidget(i, 1, btn2)
    
    #funcion para mostrar el popup de agregar feriado
    def aggPopUp(self):
        self.calendarioW.show() #mostramos el popup
    
    #funcion para crear un feriado en base de datos
    def crear(self):
        fecha = self.calendario.selectedDate() #obtenemos la fecha seleccionada en el calendario
        fecha = date.isoformat(fecha.toPyDate()) #convertimos la fecha a un formato de fecha
        create_feriado(fecha) #creamos el feriado en la base de datos
        self.loadData() #cargamos los datos de la tabla
        self.calendarioW.hide() #ocultamos el popup

    #funcion para accionar el boton de cancelar en los popups
    def cancelar(self):
        #ocultamos los popups
        self.calendarioW.hide()
        self.eliminar.hide()

    #funcion para mostrar el popup de eliminar feriado
    def deletePopup(self, indice):
        self.eliminar.show() #mostramos el popup
        self.nom_fecha.setText(self.feriados[indice]) #establecemos el nombre del feriado en el label
        self.currentFeriado = self.feriados[indice] #establecemos el feriado actual

    #funcion para eliminar un feriado de la base de datos
    def delete(self):
        delete_feriado(self.currentFeriado) #eliminamos el feriado de la base de datos
        self.eliminar.hide() #ocultamos el popup
        self.loadData() #cargamos los datos de la tabla

    #funcion para seleccionar un feriado en el calendario
    def selectFecha(self):
        fecha = self.calendario.selectedDate() #obtenemos la fecha seleccionada en el calendario
        self.calendario = date.isoformat(fecha.toPyDate()) #convertimos la fecha a un formato de fecha
        
        if(self.fechaIniLabel.text() != ''):
            self.fechaIniLabel.setText(self.fechaInicio) #establecemos la fecha de inicio en el label de crear feriado
        else:
            self.fechaIniLabel_2.setText(self.fechaInicio) #establecemos la fecha de inicio en el label de editar feriado
        self.calendarioW.hide()

    #funcion para volver a la ventana de proyectos
    def volver(self):
        ventana = ventanaProyectos(self.nombreUser) #nueva ventana de proyectos
        widget.addWidget(ventana)  #agregamos la nueva ventana a la lista de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1) #camibamos la ventana actual

# Clase para la ventana de actividades
class ventanaActividades(QDialog):
    def __init__(self, nombreUser, proyecto: Proyecto):
        super(ventanaActividades, self).__init__()
        loadUi('ui/abrirMAIA.ui', self) #cargamos la interfaz grafica

        #inicializamos los componentes de la ventana
        self.proyecto = proyecto
        self.nombreUser = nombreUser
        self.proy_name.setText(proyecto.nombre)
        self.id_proyecto = proyecto.identificador
        self.actividades = []
        self.currentActividad = {}

        #ocultamos los popups
        self.crear_act.hide()
        self.editar_act.hide()
        self.eliminar.hide()
        self.relacionar_w.hide()
        self.desrelacionar_w.hide()
        
        widget.move(0, 0) #movemos la ventana a la posicion deseada

        #relacionamos los botones con sus funciones correspondientes
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
        
        #reajustamos el tamaño de las columnas de la tabla
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch) #reajustamos el tamaño que ocupe el maximo espacio posible
        for i in range(1,7):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)  #reajustamos el tamaño que ocupe el minimo espacio posible

        self.loadData() #cargamos los datos de la tabla

    #funcion para cargar los datos de la tabla
    def loadData(self):
        self.actividades = get_actividades(self.id_proyecto) #obtenemos las actividades del proyecto
        self.tableWidget.setRowCount(len(self.actividades)) #establecemos la cantidad de filas de la tabla
        for i in range(len(self.actividades)):
            #establecemos los datos de cada columna
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.actividades[i].nombre))
            self.tableWidget.item(i, 0).setForeground(QBrush(QColor(213, 213, 213))) #establecemos el color de la letra
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.actividades[i].duracion)))
            self.tableWidget.item(i, 1).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.actividades[i].fechaInicioTemprano))
            self.tableWidget.item(i, 2).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(self.actividades[i].fechaFinTardio)))
            self.tableWidget.item(i, 3).setForeground(QBrush(QColor(213, 213, 213)))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem("Si" if (self.actividades[i].critico) else "No"))
            self.tableWidget.item(i, 4).setForeground(QBrush(QColor(213, 213, 213)))

            #establecemos los botones de acciones de cada fila
            #boton de editar
            btn = QPushButton(self.tableWidget) 
            btn.setIcon(QIcon(editIcon))
            btn.setIconSize(QSize(25,25))
            btn.setStyleSheet("*{border-radius: 50%;}") #establecemos el estilo del boton
            btn.clicked.connect(lambda state, x=i: self.editarPopup(x)) #conectamos el boton con su funcion correspondiente
            self.tableWidget.setCellWidget(i, 5, btn)
            #boton de eliminar
            btn2 = QPushButton(self.tableWidget)
            btn2.setIcon(QIcon(deleteIcon))
            btn2.setIconSize(QSize(25,25))
            btn2.setStyleSheet("*{border-radius: 50%;}") #establecemos el estilo del boton
            btn2.clicked.connect(lambda state, x=i: self.deletePopup(x)) #conectamos el boton con su funcion correspondiente
            self.tableWidget.setCellWidget(i, 6, btn2)
    
    #funcion para mostrar el popup de creacion de actividades
    def crearPopup(self):
        self.crear_act.show() #mostramos el popup
        self.nom_2.setText('') #iniciamos los campos de texto
        self.dur_2.setText('')
        
    #funcion para crear una actividad en la base de datos
    def crear(self):
        newActividad = Actividad(self.nom_2.text(), self.dur_2.text()) #creamos una nueva clase actividad
        create_actividad(newActividad, self.id_proyecto) #creamos la actividad en la base de datos
        self.loadData() #actualizamos la tabla
        self.crear_act.hide() #ocultamos el popup

    #funcion para accionar el boton de cancelar en los popups
    def cancelar(self):
        #ocultamos los popups
        self.crear_act.hide()
        self.editar_act.hide()
        self.eliminar.hide()
        self.relacionar_w.hide()
        self.desrelacionar_w.hide()

    #funcion para mostrar el popup de edicion de actividades
    def editarPopup(self, indice):
        self.currentActividad = self.actividades[indice] #guardamos la actividad actual
        self.editar_act.show() #mostramos el popup
        #establecemos los campos de texto con los datos de la actividad actual
        self.nom_1.setText(self.currentActividad.nombre)
        self.dur.setText(str(self.currentActividad.duracion))

    #funcion para editar una actividad en la base de datos
    def editar(self):
        newActividad = Actividad(self.nom_1.text(), self.dur.text()) #creamos una nueva clase actividad
        modify_actividad(self.currentActividad.identificador, newActividad, self.id_proyecto) #modificamos la actividad en la base de datos
        self.loadData() #actualizamos la tabla
        self.editar_act.hide() #ocultamos el popup

    #funcion para mostrar el popup de eliminacion de actividades
    def deletePopup(self, indice):
        self.currentActividad = self.actividades[indice] #guardamos la actividad actual
        self.nom_acti.setText(self.currentActividad.nombre) #mostramos el nomnbre de la actividad
        self.eliminar.show() #mostramos el popup

    #funcion para eliminar una actividad de la base de datos
    def delete(self):
        id = self.currentActividad.identificador #obtenemos el id de la actividad
        delete_actividad(id, self.proyecto) #eliminamos la actividad de la base de datos
        self.eliminar.hide() #ocultamos el popup
        self.loadData() #actualizamos la tabla

    #funcion para mostrar el popup de relacionar actividades
    def relacionarPopup(self):
        self.relacionar_w.show() #mostramos el popup
        self.anterior_box.clear() #limpiamos los campos
        self.siguiente_box.clear() 
        #rellenamos los campos con las actividades
        for i in range(len(self.actividades)):
            self.anterior_box.addItem(str(i+1))
            self.siguiente_box.addItem(str(i+1))
        
    #funcion para relacionar dos actividades en la base de datos
    def relacionar(self):
        self.relacionar_w.hide() #ocultamos el popup

        anteriorIndex = self.anterior_box.currentIndex() #obtenemos el indice de la actividad anterior
        siguienteIndex = self.siguiente_box.currentIndex() #obtenemos el indice de la actividad siguiente

        anteriorId = self.actividades[anteriorIndex].identificador #obtenemos el id de la actividad anterior
        siguienteId = self.actividades[siguienteIndex].identificador #obtenemos el id de la actividad siguiente

        newRelacion = Relacion(anteriorId, siguienteId) #creamos una nueva clase relacion
        create_relacion(newRelacion, self.id_proyecto) #relacionamos las actividades en la base de datos

        self.loadData() #actualizamos la tabla

    #funcion para mostrar el popup de desrelacionar actividades
    def desrelacionarPopup(self):
        self.desrelacionar_w.show() #mostramos el popup
        self.relacion_box.clear() #limpiamos el campo
        relaciones = get_relaciones(self.id_proyecto) #obtenemos las relaciones de la base de datos

        #rellenamos el campo con las relaciones
        try:
            for relacion in relaciones:
                anterior = get_actividad_by_id(relacion.actividadPrecedente, self.id_proyecto) #obtenemos la actividad anterior
                siguiente = get_actividad_by_id(relacion.actividadSiguiente, self.id_proyecto) #obtenemos la actividad siguiente

                #obtenemos los indices de las activiades relacionadas
                for i in range(len(self.actividades)):
                    if self.actividades[i].identificador == anterior.identificador:
                        anteriorIndex = i+1 #indice de la actividad anterior
                    if self.actividades[i].identificador == siguiente.identificador:
                        siguienteIndex = i+1 #indice de la actividad siguiente

                self.relacion_box.addItem(f"{anteriorIndex} -> {siguienteIndex}") #mostramos la relacion
        except:
            error("No hay relaciones en la base de datos") #mostramos un error si no hay relaciones

    #función para desrelacionar dos actividades en la base de datos
    def desrelacionar(self):
        try: 
            relaciones = get_relaciones(self.id_proyecto) #obtenemos las relaciones de la base de datos
            index = self.relacion_box.currentIndex() #obtenemos el indice de la relacion actual
            id = relaciones[index].identificador #obtenemos el id de la relacion actual
            delete_relacion(id, self.id_proyecto) #eliminamos la relacion de la base de datos
            self.loadData() #actualizamos la tabla
            self.desrelacionar_w.hide() #ocultamos el popup
        except:
            error("Error al desrelacionar") #mostramos un error
    
    #funcion para mostrar el grafo de actividades
    def verGrafo(self):
        try:
            proy = get_proyecto_by_id(self.id_proyecto) #obtenemos el proyecto actual
            proy.actualizar_bd() #actualizamos la base de datos
            proy.mostrar_grafo() #mostramos el grafo
        except:
            error("Error al mostrar el grafo")

    #funcion para mostrar el diagrama de Gantt
    def verDiagrama(self):
        try:
            proy = get_proyecto_by_id(self.id_proyecto) #obtenemos el proyecto actual
            proy.actualizar_bd() #actualizamos la base de datos
            proy.actualizarCsv() #actualizamos el excel
            mostrar_gantt() #mostramos el diagrama de Gantt
        except:
            error("Error al mostrar el diagrama de Gantt")

    #funcion para calcular el camino de las actividades
    def calcularCamino(self):
        try: 
            proy = get_proyecto_by_id(self.id_proyecto) #obtenemos el proyecto actual
            proy.actualizar_bd() #actualizamos la base de datos
            proy.actualizarCsv() #actualizamos el excel
            modify_proyecto(self.id_proyecto, proy) #actualizamos el proyecto en la base de datos
            self.loadData() #actualizamos la tabla
        except:
            error("Error al calcular el camino")
            
    #funcion para volver a la ventana de proyectos
    def volver(self):
        ventana = ventanaProyectos(self.nombreUser) #creamos una nueva clase ventana
        widget.addWidget(ventana)  #agregamos la ventana a la lista de ventanas
        widget.setCurrentIndex(widget.currentIndex() + 1) #cambiamos de ventana

#funcion para mostrar un mensaje de error
def error(mensaje):
    pupupError = QMessageBox() #creamos un popup
    pupupError.setWindowTitle("Error") #le damos un titulo al popup
    pupupError.setText(mensaje) #le damos el mensaje
    pupupError.setIcon(QMessageBox.Critical)
    x = pupupError.exec_()  # mostramos el popup

app = QApplication(sys.argv) #inicializar la aplicacion
welcome = WelcomeScreen() #crear un objeto de la clase que creamos
widget = QtWidgets.QStackedWidget() #se crea un widget que va a contener todos los widgets, nos permite mover entre ellos
widget.addWidget(welcome) #agregar un widget al widget, se agrega la ventana
widget.move(400, 80) #ponemos en la parte central de la pantalla
widget.show()

actividadIcon = QPixmap('ui/checklist.png')
editIcon = QPixmap('ui/edit.png')
deleteIcon = QPixmap('ui/trash.png')

try:
    sys.exit(app.exec_())
except:
    print("Error")
