import numpy as np


def crear_matriz_costo(matriz_base, costo):
    """
    Descripcion de crearMatrizCostoSinMontura
    # Funcion retorna matriz que contiene el costo de cada casilla

     Args:
        costo (dict): diccionario de costos
        matriz_base (undefined): matriz del tablero

    """
    matriz_costo = np.zeros(matriz_base.shape)
    for i in range(matriz_base.shape[0]):
        for j in range(matriz_base.shape[1]):
            matriz_costo[i, j] = costo[matriz_base[i][j]]

    return matriz_costo


def buscar_agente(matriz_base, id_agente=1):

    for i in range(matriz_base.shape[0]):
        for j in range(matriz_base.shape[1]):
            if matriz_base[i, j] == id_agente:
                return [i, j]


def dato_segun_coordenada(tupla, matriz_base):
    return matriz_base[tupla[0]][tupla[1]]


def tupla_es_id(tupla, matriz_base, id_agente):
    """
    Evalua si la ubicacion de la tupla es el agente indicado por el ID
    Args:
        tupla (np.array):[a,b] tupla a evaluar
        matriz_base (matriz): [matriz] donde se va a evaluar
        id_agente (int): id agente
    """
    return matriz_base[tupla[0]][tupla[1]] == id_agente


def tupla_esta_fuera(tupla, matriz_base):
    return 0 > tupla[0] or tupla[0] > matriz_base.shape[0]-1 or 0 > tupla[1] or tupla[1] > matriz_base.shape[1]-1


def esta_en_lista(lista, valor):
    return valor in lista


def elementos_iguales(lista):
    aux_bool = False
    if len(lista) == 1:
        aux = lista[0]
        return aux

    else:
        aux = lista[0]
        for i in range(1, len(lista)):
            if lista[i] == aux:
                aux_bool = True
            else:
                aux_bool = False
    return aux_bool


listaNodosNivel = []
listaNodosAux = []


def procesar_tupla_bpi(tupla, nodos_recorridos, matriz_base, info_tablero):
    """
        BPI: Busqueda por Profundidad Iterativa


        Args:
            info_tablero: dicionario con id de obstaculo y meta
            tupla: tupla a validar
            matriz_base: matriz del tablero
            nodos_recorridos: listado de nodos recorridos

        Return:
            bool: si llega a meta retorna #True
        """
    if tupla_esta_fuera(tupla, matriz_base) == False \
            and tupla_es_id(tupla, matriz_base, info_tablero['obstaculo']) == False:

        if not nodos_recorridos:
            listaNodosAux.append(tupla)
            return tupla_es_id(tupla, matriz_base, info_tablero['meta'])

        elif not esta_en_lista(nodos_recorridos, tupla):
            listaNodosAux.append(tupla)
            return tupla_es_id(tupla, matriz_base, info_tablero['meta'])

        else:
            return False

# orden: arriba, abajo, derecha, izquierda


def explorar_siguiente_nivel_bpi(nueva_raiz, lista_recorrido_total, matriz_base, info_tablero):

    if tupla_es_id(nueva_raiz, matriz_base, info_tablero['obstaculo']) == False \
            and tupla_esta_fuera(nueva_raiz, matriz_base) == False:

        # if listaNodosAux.append(nuevaRaiz)

        arriba = [nueva_raiz[0] - 1, nueva_raiz[1]]
        abajo = [nueva_raiz[0] + 1, nueva_raiz[1]]
        derecha = [nueva_raiz[0], nueva_raiz[1] + 1]
        izquierda = [nueva_raiz[0], nueva_raiz[1] - 1]

        listaNodosAux.append(nueva_raiz)  # almacenamos primero la raiz

        aux = procesar_tupla_bpi(arriba, lista_recorrido_total, matriz_base, info_tablero)
        if aux:
            return [True, arriba]
        aux = procesar_tupla_bpi(abajo, lista_recorrido_total, matriz_base, info_tablero)
        if aux:
            return [True, abajo]
        aux = procesar_tupla_bpi(derecha, lista_recorrido_total, matriz_base, info_tablero)
        if aux:
            return [True, derecha]
        aux = procesar_tupla_bpi(izquierda, lista_recorrido_total, matriz_base, info_tablero)
        if aux:
            return [True, izquierda]

        listaNodosNivel.extend(listaNodosAux)
        listaNodosAux.clear()

    return [False, []]


def encontrar_recorrido_bpi(matriz_base, info_tablero):
    contador = matriz_base.size
    meta = buscar_agente(matriz_base, info_tablero['meta'])
    jugador = buscar_agente(matriz_base)

    lista_recorrido_total = []  # el resultado final
    lista_recorriendo = [jugador]
    
    for j in range(0, contador):

        nodos_a_recorrer = len(lista_recorriendo)

        for i in range(0, nodos_a_recorrer):
            aux = explorar_siguiente_nivel_bpi(lista_recorriendo[i], lista_recorrido_total, matriz_base, info_tablero)
            # print('aqui')
            # print(lista_recorriendo[i])
            
            if aux[0]:
                if len(lista_recorriendo) == 1:
                    listaNodosNivel.append(lista_recorriendo[0])
                    listaNodosNivel.append(aux[1])
                    print('se encontro la meta en nivel ' + str(j+1))
                    return listaNodosNivel
                else:print('se encontro la meta en nivel ' + str(j))
                break

        if esta_en_lista(listaNodosNivel, meta):
            # print('Se encontro la meta en nivel ' + str(j))
            # para mejorar la gráfica
            # print(
            #    '-----------------------------------------------------------------------------------------------------')
            listanueva = []
            for i in range(0, len(listaNodosNivel)):
                if listaNodosNivel[i] == meta:
                    listanueva.append(listaNodosNivel[i])
                    break
                else:
                    listanueva.append(listaNodosNivel[i])

            lista_recorriendo.extend(listanueva)
            # print(lista_recorriendo)
            # print(
            #    '-----------------------------------------------------------------------------------------------------')
            return lista_recorriendo

        if not lista_recorrido_total == []:
            for i in range(0, len(lista_recorriendo)):
                if not esta_en_lista(lista_recorrido_total, lista_recorriendo[i]):
                    lista_recorrido_total.append(lista_recorriendo[i])
                    print(lista_recorriendo[i])

            lista_recorriendo.clear()
            lista_recorriendo.extend(listaNodosNivel)
            listaNodosNivel.clear()
            print('no encontró meta en nivel ' + str(j))
            print('Final antes de iterar nuevamente: lTotal')

        else:
            lista_recorrido_total.extend(lista_recorriendo)
            lista_recorriendo.clear()
            lista_recorriendo.extend(listaNodosNivel)
            listaNodosNivel.clear()
            print('no encontró meta en nivel ' + str(j))
            print('Final antes de iterar nuevamente: lTotal')

        print(lista_recorriendo)

# print(tupla_es_id([3, 0], tablero, informaciontablero['obstaculo']) is False )
# print(tupla_es_id([3, 0], tablero, informaciontablero['obstaculo']))

# escenario = np.loadtxt("matriz.txt", skiprows=0)
# info = {
#         'obstaculo': 3,
#         'meta': 5
#     }
# print('resultado', encontrar_recorrido_bpi(escenario, info))
