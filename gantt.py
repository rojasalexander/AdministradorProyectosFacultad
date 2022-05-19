import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mdates
import matplotlib.dates as mdates 
import numpy as np
from datetime import datetime, timedelta

data = pd.read_csv('data.csv') # datos del archivo csv 


#convertir los datos str a datetime AAAA-MM-DD
data['inicio'] = pd.to_datetime(data['inicio'], format='%Y-%m-%d')
data['fin'] = pd.to_datetime(data['fin'], format='%Y-%m-%d')

#ordenar las tareas por fecha de inicio
data.sort_values("inicio",axis=0, ascending=True, inplace=True) #axis=0 para ordenar por columnas #ascending=True para ordenar de menor a mayor #inplace=True para que se modifique el dataframe original
# resetear el index
data.reset_index(drop=True, inplace=True) #drop = True el indice actual se elimina y el indice numerico lo reemplaza #inplace=True para que se modifique el dataframe original

# añade la duracion de la tarea
data["duracion"] = data["fin"] - data["inicio"] + timedelta(days=1)  
# añadir columna: la fecha de inicio de cada tarea 




