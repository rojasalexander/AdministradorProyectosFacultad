dias_en_mes = [31,28,31,30,31,30,31,31,30,31,30,31]

def sumardias(fecha : str, dias): # fecha = AAAA/MM/DD
    año = int(fecha[:4])
    mes = int(fecha[5:7])
    dia = int(fecha[8:])
    bisiesto(año)

    suma = dia + dias
    while suma > dias_en_mes[mes - 1]:
        suma -= dias_en_mes[mes - 1]
        mes += 1
        if mes > 12:
            mes = 1
            año += 1
    
    return f"{año}".rjust(4,'0') + "/" + f"{mes}".rjust(2,'0') + "/" + f"{suma}".rjust(2,'0')

def restardias(fecha : str , dias):
    año = int(fecha[:4])
    mes = int(fecha[5:7])
    dia = int(fecha[8:])
    bisiesto(año)
    resta = dia - dias
    while resta < 1:
        resta = dias_en_mes[mes - 2] + resta
        mes -= 1
        if mes < 1:
            mes = 12
            año -= 1

    return f"{año}".rjust(4,'0') + "/" + f"{mes}".rjust(2,'0') + "/" + f"{resta}".rjust(2,'0')
    
def compfechas(fecha1, fecha2):
    # Retorna 1 si f1 < f2, -1 si f1 > f2, y 0 si f1 == f2

    if fecha1 == "":
        return 1
    elif fecha2 == "":
        return -1

    año1 = int(fecha1[:4])
    mes1 = int(fecha1[5:7])
    dia1 = int(fecha1[8:])

    año2 = int(fecha2[:4])
    mes2 = int(fecha2[5:7])
    dia2 = int(fecha2[8:])

    if año1 > año2:
        return -1
    elif año1 < año2:
        return 1
    elif año1 == año2:
        if mes1 > mes2:
            return -1
        elif mes1 < mes2:
            return 1
        elif mes1 == mes2:
            if dia1 > dia2:
                return -1
            elif dia1 < dia2:
                return 1
            elif dia1 == dia2:
                return 0


def bisiesto(año):
    # Para determinar si un año es bisiesto, siga estos pasos:

    # Si el año es uniformemente divisible por 4, vaya al paso 2. De lo contrario, vaya al paso 5.
    # Si el año es uniformemente divisible por 100, vaya al paso 3. De lo contrario, vaya al paso 4.
    # Si el año es uniformemente divisible por 400, vaya al paso 4. De lo contrario, vaya al paso 5.
    # El año es un año bisiesto (tiene 366 días).
    # El año no es un año bisiesto (tiene 365 días).

    if año % 4 == 0:
        if año % 100:
            if año % 400:
                ok = True
            else:
                ok = False
        else:
            ok = True
    else:
        ok = False

    if ok == True:
        dias_en_mes[1] += 1
