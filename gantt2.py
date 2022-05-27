from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
import datetime as dt


# Importamos el archivo de datos
data = pd.read_csv('data.csv')
data.head() #retorna las filas

#convertir a datetime
data.Inicio = pd.to_datetime(data.Inicio)
data.Fin = pd.to_datetime(data.Fin)


# se anade la duracion de las tareas
data['Duracion'] = (data.Fin-data.Inicio)
data.Duracion = data.Duracion.apply(lambda x: x.days+1) #se convierte a dias y se suma 1 por si se termine el mismo dia

#ordenar las fechas en orden ascendente
data = data.sort_values(by='Inicio', ascending=True) #ordena en base a la columna de inicio

#etiquetas del proyecto
p_inicio = data.Inicio.min() #fecha de inicio del proyecto
p_fin = data.Fin.max() #fecha de fin del proyecto
p_duracion = (p_fin - p_inicio).days+1 #duracion del proyecto

data['Desde_Inicio'] = data.Inicio.apply(lambda x: (x - p_inicio).days) #dias desde el inicio del proyecto

# etiquetas para el grafico
x_etiqueta = [i for i in range(p_duracion+1)] #etiquetas para el eje x
x_labels= [(p_inicio + dt.timedelta(days=i)).strftime('%d-%b') for i in x_etiqueta] 



#grafico
#Agregar color por trabajo critico o no
diccionario_color = {'Y': 'mediumturquoise', 'N': 'midnightblue'}
plt.figure(figsize=(10,5))  
plt.title('Diagrama de Gantt', size = 16)

for i in range(data.shape[0]):
    color = diccionario_color[data.Critico[i]]
    plt.barh(y=data.Tarea[i],left=data.Desde_Inicio[i], width= data.Duracion[i], color = color, label= data.Critico[i])
    plt.barh(y=data.Tarea[i],left=0, width=data.Desde_Inicio[i], color = '#f0f0f0')
plt.gca().invert_yaxis() #invertir eje y
plt.xticks(ticks=x_etiqueta[::int(len(x_etiqueta)/12)], labels=x_labels[::int(len(x_etiqueta)/12)]) #etiquetas para el eje x, /12 para que quede de manera prederteminada
plt.grid(axis='x')                            


#agregar referencia 
handles, labels = plt.gca().get_legend_handles_labels()
exist_list = []
handle_lista, label_lista = [], []
for handle,label in zip(handles,labels):
    if label not in exist_list:
        exist_list.append(label)
        handle_lista.append(handle)
        label_lista.append(label)

plt.gcf().autofmt_xdate(rotation=30)
plt.legend(handle_lista, label_lista, fontsize ='medium', title='Critico', title_fontsize='large')

plt.show()

