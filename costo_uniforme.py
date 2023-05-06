import numpy as np
import queue as Queue


#Carga de datos txt, interpretacion de valores
tablero = np.loadtxt('matriz.txt', skiprows=0)
costos = {
    0: 1,
    1: 0,
    2: 2,
    3: 0,
    4: 3,
    5: 0
}


def crear_matriz_costo(matriz_base, costo):
    #Funcion retorna matriz que contiene el costo de cada casilla

#costo (dict): diccionario de costos
#matriz_base (undefined): matriz del tablero

    #numPy, matriz de ceros
    matriz_costo = np.zeros(matriz_base.shape)
    for i in range(matriz_base.shape[0]):
        for j in range(matriz_base.shape[1]):
            matriz_costo[i, j] = costo[matriz_base[i][j]]
#shape funcion -> posicion desde hasta
    return matriz_costo


def ubicacionDelJugador(matriz_base):
#Retorna la ubicacion del jugador en la matriz que se ingrese
#matriz_base (undefined): matriz del tablero

    for i in range(matriz_base.shape[0]):
        for j in range(matriz_base.shape[1]):
            if matriz_base[i, j] == 1:
                return [i, j]

def puedeIrHacia(desde, hacia, matriz): #Comprueba si en la coordenada hay obstaculos o está fuera del mapa
    if hacia == "arriba":
        try:
            if desde[0] - 1 < 0: #Detectar si el agente intenta salirse
                # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0] - 1, desde[1]] != 3.0:
                return True
            else:
                return False
        except IndexError:
            # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    elif hacia == "abajo":
        try:
            if desde[0] + 1 > matriz.shape[0]:
                # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0] + 1, desde[1]] != 3.0:
                return True
            else:
                return False
        except IndexError:
            # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    elif hacia == "derecha":
        try:
            if desde[1] + 1 > matriz.shape[1]:
                # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0], desde[1] + 1] != 3.0:
                return True
            else:
                return False
        except IndexError:
            # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    elif hacia == "izquierda":
        try:
            if desde[1] - 1 < 0:
                # print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0], desde[1] - 1] != 3.0:
                return True
            else:
                return False
        except IndexError:
            print("La posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    else:
        print("ERROR: ingreso valor \"hacia\" no valido. Usted ingreso {} \n \n".format(hacia) * 3)


def ubicacionHacia(desde, hacia, matriz): #Devuelve la tupla de esa direccion
    if hacia == "arriba":
        try:
            if desde[0] - 1 < 0:
                # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0] - 1, desde[1]] != 3.0:
                return [desde[0] - 1, desde[1]]
            else:
                return False
        except IndexError:
            # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    elif hacia == "abajo":
        try:
            if desde[0] + 1 > matriz.shape[0]:
                # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0] + 1, desde[1]] != 3.0:
                return [desde[0] + 1, desde[1]]
            else:
                return False
        except IndexError:
            # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    elif hacia == "derecha":
        try:
            if desde[1] + 1 > matriz.shape[1]:
                # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0], desde[1] + 1] != 3.0:
                return [desde[0], desde[1] + 1]
            else:
                return False
        except IndexError:
            # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    elif hacia == "izquierda":
        try:
            if desde[1] - 1 < 0:
                # print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
                return False
            elif matriz[desde[0], desde[1] - 1] != 3.0:
                return [desde[0], desde[1] - 1]
            else:
                return False
        except IndexError:
            print("Recorcholis esa posicion esta fuera de los parametros {}".format(hacia) + "\n")
            return False
    else:
        print("ERROR: ingreso valor \"hacia\" no valido. Usted ingreso {} \n \n".format(hacia) * 3)


def ubicacionMeta(matriz_base): #Retorna posicion ganadora
    for i in range(matriz_base.shape[0]):
        for j in range(matriz_base.shape[1]):
            if matriz_base[i, j] == 5:
                return [i, j]


#Copia y lista sin afectar la informacion original
def copiarListaEnOtraLista_aux(lista_fuente, lista_destino, nodo_actual, nodo_anterior):
    if nodo_actual == nodo_anterior:
        lista_destino = [nodo_actual]
    else:
        lista_destino = []
        for i in range(len(lista_fuente)):
            lista_destino[len(lista_fuente):] = [lista_fuente[i]]


def copiarMatrizEnOtraMatriz_aux(matriz_fuente, matriz_destino):
    for i in range(matriz_fuente.shape[0]):
        for j in range(matriz_fuente.shape[1]):
            matriz_fuente[i, j] = matriz_destino[i, j]


def expandirNodoHacia(cola, nivel, lista, desde, hacia, matriz):
    ubicacion_meta = ubicacionMeta(matriz)
    prioridadHacia = 10
    if hacia == "arriba":
        prioridadHacia = 1
    elif hacia == "derecha":
        prioridadHacia = 2
    elif hacia == "abajo":
        prioridadHacia = 3
    elif hacia == "izquierda":
        prioridadHacia = 4
    else:
        print("erro en expandirNodoHacia() se ingrso {} ".format(hacia))
    if puedeIrHacia(desde, hacia, matriz):
        aux_lista = []
        for i in range(len(lista)):
            aux_lista[len(lista):] = [lista[i]]
        aux_lista[len(aux_lista):] = [ubicacionHacia(desde, hacia, matriz)]
        cola.put([nivel, prioridadHacia, aux_lista])
        ubicacion_actual_jugador = aux_lista[len(aux_lista) - 1]
        if ubicacion_actual_jugador == ubicacion_meta:
            return aux_lista


def expandirNodo(cola, nodoAnterior, nodoactual, matriz, lista, costoAcomulado, matrizCosto):
    if nodoactual == nodoAnterior:
        aux_lista = [nodoactual]
    else:
        aux_lista = []
        for i in range(len(lista)):
            aux_lista[len(lista):] = [lista[i]]

    if puedeIrHacia(nodoactual, "arriba", matriz):
        if nodoAnterior != ubicacionHacia(nodoactual, "arriba", matriz):

            aux_lista[len(aux_lista):] = [
                ubicacionHacia(nodoactual, "arriba", matriz)]
            cola.put([costoAcomulado + matrizCosto[
                ubicacionHacia(nodoactual, "arriba", matriz)[0], ubicacionHacia(nodoactual, "arriba", matriz)[1]],
                      aux_lista])

            aux_lista = []
            if nodoactual == nodoAnterior:
                aux_lista = [nodoactual]
            else:
                aux_lista = []
                for i in range(len(lista)):
                    aux_lista[len(lista):] = [lista[i]]

    if puedeIrHacia(nodoactual, "abajo", matriz):
        if nodoAnterior != ubicacionHacia(nodoactual, "abajo", matriz):

            aux_lista[len(aux_lista):] = [
                ubicacionHacia(nodoactual, "abajo", matriz)]
            cola.put([costoAcomulado + matrizCosto[
                ubicacionHacia(nodoactual, "abajo", matriz)[0], ubicacionHacia(nodoactual, "abajo", matriz)[1]],
                      aux_lista])

            aux_lista = []
            if nodoactual == nodoAnterior:
                aux_lista = [nodoactual]
            else:
                aux_lista = []
                for i in range(len(lista)):
                    aux_lista[len(lista):] = [lista[i]]

    if puedeIrHacia(nodoactual, "derecha", matriz):
        if nodoAnterior != ubicacionHacia(nodoactual, "derecha", matriz):

            aux_lista[len(aux_lista):] = [
                ubicacionHacia(nodoactual, "derecha", matriz)]
            cola.put([costoAcomulado + matrizCosto[
                ubicacionHacia(nodoactual, "derecha", matriz)[0], ubicacionHacia(nodoactual, "derecha", matriz)[1]],
                      aux_lista])

            aux_lista = []
            if nodoactual == nodoAnterior:
                aux_lista = [nodoactual]
            else:
                aux_lista = []
                for i in range(len(lista)):
                    aux_lista[len(lista):] = [lista[i]]

    if puedeIrHacia(nodoactual, "izquierda", matriz):
        if nodoAnterior != ubicacionHacia(nodoactual, "izquierda", matriz):

            aux_lista[len(aux_lista):] = [ubicacionHacia(
                nodoactual, "izquierda", matriz)]
            cola.put([costoAcomulado + matrizCosto[
                ubicacionHacia(nodoactual, "izquierda", matriz)[0], ubicacionHacia(nodoactual, "izquierda", matriz)[1]],
                      aux_lista])

            aux_lista = []
            if nodoactual == nodoAnterior:
                aux_lista = [nodoactual]
            else:
                aux_lista = []
                for i in range(len(lista)):
                    aux_lista[len(lista):] = [lista[i]]


def rutaOptima(matriz):
    parada = 0
    matrizCosto = crear_matriz_costo(matriz, costos)
    ubicacionDeMeta = ubicacionMeta(matriz)
    colaDePrioridad = Queue.PriorityQueue()
    colaDePrioridad.put([0, [ubicacionDelJugador(matriz)]])

    while True:
        nodoMenorcostoAcomulado = colaDePrioridad.get()
        ubicacionActualJugador = nodoMenorcostoAcomulado[1][len(
            nodoMenorcostoAcomulado[1]) - 1]
        ubicacionAnteriorDelJugador = nodoMenorcostoAcomulado[1][len(
            nodoMenorcostoAcomulado[1]) - 2]
        ruta = nodoMenorcostoAcomulado[1]
        costoAcomulado = nodoMenorcostoAcomulado[0]
        if ubicacionActualJugador == ubicacionDeMeta:
            return nodoMenorcostoAcomulado[1]
        else:
            expandirNodo(colaDePrioridad, ubicacionAnteriorDelJugador, ubicacionActualJugador, matriz, ruta,
                         costoAcomulado, matrizCosto)
        if parada == 40:
            break
        else:
            parada = parada + 1

    # def profindidadInteractiva(matriz):
    parada = 2
    ubicacion_meta = ubicacionMeta(matriz)

    while True:
        print("a")
        nodo_mayor_prioridad = cola_de_prioridad.get()
        if nodo_mayor_prioridad[0] + 1 == parada:
            cola_de_prioridad.put(nodo_mayor_prioridad)
            break
        ubicacion_actual_jugador = nodo_mayor_prioridad[2][len(nodo_mayor_prioridad[2]) - 1]
        a = expandirNodoHacia(cola_de_prioridad, nodo_mayor_prioridad[0] + 1, nodo_mayor_prioridad[2],
                              ubicacion_actual_jugador, "arriba", matriz)
        a = expandirNodoHacia(cola_de_prioridad, nodo_mayor_prioridad[0] + 1, nodo_mayor_prioridad[2],
                              ubicacion_actual_jugador, "derecha", matriz)
        a = expandirNodoHacia(cola_de_prioridad, nodo_mayor_prioridad[0] + 1, nodo_mayor_prioridad[2],
                              ubicacion_actual_jugador, "abajo", matriz)
        a = expandirNodoHacia(cola_de_prioridad, nodo_mayor_prioridad[0] + 1, nodo_mayor_prioridad[2],
                              ubicacion_actual_jugador, "izquierda", matriz)
    parada = parada + 1
    print(parada)
    if a != [] and a != None:
        return a

# ----------- PRUEBAS --------------------------------#

print(rutaOptima(tablero))  # prueba de funcion rutaOptima(matriz)



