import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

sys.path.append('database')
from proyectodata import *


def cambiar_a_2():
    # Esconde pantalla 1 y muestra pantalla 2
    Pantalla1.hide()
    Pantalla2.show()

def main():                                                        
    # Corre el main Loop (Se muestra la Ventana Principal hasta que se salga del programa)
    Main_window.show()
    Pantalla2.hide()                                              
    sys.exit(app.exec_())

def printear():
    print("Hola Mundo")

app = QApplication([])                                              # Crea una instancia de aplicación
Main_window = QWidget()                                             # Crea la pantalla principal (Nunca se deja de mostrar)
Main_window.setWindowTitle('Adminitrador - Proyectos')
Main_window.setGeometry(0, 0, 600, 500)                             # Primeros dos argumentos son posicion, los otros tamaño

Pantalla1 = QWidget(parent = Main_window)                           # La primera pantalla contiene todo lq se muestra al inicio y es hija del main
Pantalla1.setGeometry(0, 0, 600, 500)

Label_window = QWidget(parent = Pantalla1)                          # Ventana para contener al texto // Esta dentro de pantalla 1
Label_window.setGeometry(17, 80, 600, 100)

font = QFont("Berlin Sans FB Demi", 36)
label = QLabel("Adminitrador _ Proyectos")
label.setFont(font)
                                                                    # Todas las ventanas necesitan un layout para ser contenidos los widgets
Label_layout = QHBoxLayout()                                        # QHBoxLayout alinea de forma horizontal
Label_layout.addWidget(label)

Label_window.setLayout(Label_layout)

botones = QWidget(parent = Pantalla1)                               # Ventana para botones (Pantalla 1)
botones.setGeometry(0,400,600,100)
botones_layout = QHBoxLayout()                                      # QVBoxlayout alinea de forma vertical

button1 = QPushButton("Crear Proyecto")
button2 = QPushButton("Cargar Proyecto")

botones_layout.addWidget(button1)
botones_layout.addWidget(button2)

button1.clicked.connect(cambiar_a_2)                                # Cuando se presione el boton 1, llama a la funcion cambiar_a_2

botones.setLayout(botones_layout)

############################

print(get_proyectos())

Pantalla2 = QWidget(parent = Main_window)                           # Segunda Pantalla
Pantalla2.setGeometry(0, 0, 600, 500)
Pantalla2.setStyleSheet("background-color: rgb(0, 119, 255)")

botones2 = QWidget(parent = Pantalla2)
botones2.setGeometry(0,200,600,100)

botones2_layout = QVBoxLayout()
button1 = QPushButton("Crear Actividad")
button2 = QPushButton("Cargar Relacion")
button1.setStyleSheet("background-color: yellow")
button2.setStyleSheet("background-color: yellow")

botones2_layout.addWidget(button1)
botones2_layout.addWidget(button2)

divLabel2 = QWidget(parent= Pantalla2)
divLabel2.setGeometry(100, 100, 300, 50)

labelPantalla2 = QLabel(Pantalla2)
labelPantalla2.setGeometry(10, 0, 600, 80)
labelPantalla2.setText("Arriba Luque CARAJOOO!")
labelPantalla2.setStyleSheet("font-size:12pt; color: white;")

botonPrueba = QPushButton(Pantalla2)
botonPrueba.setGeometry(100,100,51,51)

addIcon = QPixmap('add-icon.png')
botonPrueba.setIcon(QIcon(addIcon))
botonPrueba.setIconSize(QSize(50,50))
botonPrueba.setStyleSheet(
    "*{border-radius: 50%;}")
botonPrueba.clicked.connect(printear)

botones2.setLayout(botones2_layout)




proyectos = get_proyectos() * 2

table = QTableWidget(Pantalla1)

table.setRowCount(len(proyectos)+1)
table.setColumnCount(4)

table.setItem(0,0, QTableWidgetItem("Nombre"))
table.setItem(0,1, QTableWidgetItem("Descripcion"))
table.setItem(0,2, QTableWidgetItem("Editar"))
table.setItem(0,3, QTableWidgetItem("Eliminar"))

for i in range(len(proyectos)):
    table.setItem(i+1, 0, QTableWidgetItem(proyectos[i][1]))
    table.setItem(i+1, 1, QTableWidgetItem(proyectos[i][3]))
    btn = QPushButton(table)
    btn.setText('Eliminar')
    table.setCellWidget(i+1, 2, btn)

    btn2 = QPushButton(table)
    btn2.setText('Editar')
    table.setCellWidget(i+1, 3, btn2)

table.setGeometry(40,180, 500, 200)

table.horizontalHeader().setStretchLastSection(True)
table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

main()





