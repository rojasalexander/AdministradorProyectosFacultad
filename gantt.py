import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta


data = pd.read_csv("data.csv") # datos del archivo csv 


#convertir los datos str a datetime AAAA-MM-DD
data["Inicio"] = pd.to_datetime(data["Inicio"], format="%Y-%m-%d")
data["Fin"] = pd.to_datetime(data["Fin"], format="%Y-%m-%d")


#ordenar las tareas por fecha de inicio
data.sort_values("Inicio", axis=0, ascending=True, inplace=True) #axis=0 para ordenar por columnas #ascending=True para ordenar de menor a mayor #inplace=True para que se modifique el dataframe original
# resetear el indice de cada tarea
data.reset_index(drop=True, inplace=True) #drop = True el indice actual se elimina y el indice numerico lo reemplaza #inplace=True para que se modifique el dataframe original



# añade la duracion de la tarea
data["Duracion"] = data["Fin"] - data["Inicio"] + timedelta(days=1)  #+1 por si empezamos y terminamos una tarea el mismo dia
# se  añade la columna 
data["Desde Inicio"]= data["Inicio"] - data["Inicio"][0]




#grafico 

cantfilas = len(data)
#creamos figura
plt.figure(figsize=[8,5], dpi=100)  #figsize= pulgadas dpi= pixel
bar_width = 0.9

for i in range(cantfilas):
    irev = cantfilas - 1 -i #para que empiece de abajo hacia arriba

    # se grafica la ultima tarea primero
    plt.broken_barh([(data["Inicio"][irev], data["Duracion"][irev])], (i - bar_width / 2,bar_width), color='c') #barra horizontal, rango de la x, rango de la y, data, color de la barra
    plt.broken_barh([(data["Inicio"][0], data["Desde Inicio"][irev])], (i - bar_width / 2,bar_width), color='#f2f2f2')  #barra horizontal, rango de la x, rango de la y, data, color de la barra


y_pos = np.arange(cantfilas) #arreglo de posiciones de las tareas
plt.yticks(y_pos, labels=reversed(data["Tarea"])) #lebel = nombre de las tareas

# xticks = posicion de las fechas

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y')) #formato de las fechas




#cuadricula
plt.grid(axis="x",which="major", lw=1) 
plt.grid(axis="x",which="minor",ls= "--", lw=1)

plt.gcf().autofmt_xdate(rotation=30) #se pone el formato de las fechas
plt.xlim(data["Inicio"][0])
plt.xlabel("Fechas", fontsize=12, weight="bold")
plt.ylabel("Tareas", fontsize=12, weight="bold")
plt.title("Grafico de Gantt", fontsize=14, weight="bold")
plt.tight_layout(pad=1.8)
plt.show()