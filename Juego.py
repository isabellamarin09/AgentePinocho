import pygame
import numpy as np
import busqueda_iterativa as algbusc


pygame.init()


class Juego:

    # Datos juego
    escenario = np.loadtxt("matriz.txt", skiprows=0)
    filas, columnas = escenario.shape[0], escenario.shape[1]
    costos = {
        0: 1,
        1: 0,
        2: 2,
        3: 0,
        4: 3,
        5: 1
    }
    
    info_tablero = {
        'obstaculo': 3,
        'meta': 5

    }

    matriz_temporal = np.loadtxt("matriz.txt", skiprows=0)

    corre = True
    FPS = 60
    reloj = pygame.time.Clock()
    # Definicion rejillas
    anchoT = 100
    altoT = 100
    NEGRO = (0, 0, 0)

    def __init__(self):
        # imagenes, se le asigna el valor correspondiente al costo inicial
        self.blanco = (pygame.image.load("imagenes/blanco.png"))
        self.pinocho = (pygame.image.load("imagenes/pinocho.png"))
        self.cigarros = (pygame.image.load("imagenes/cigarros.png"))
        self.negro = (pygame.image.load("imagenes/negro.png"))
        self.zorro = (pygame.image.load("imagenes/zorro.png"))
        self.gepetto = (pygame.image.load("imagenes/geppetto.png"))
        # ventana
        self.BLANCA = (255, 255, 255)
        self.size = 500

        self.ventana = pygame.display.set_mode((self.size, self.size-100))
        pygame.display.set_caption("Pinocho")
        self.icon = pygame.image.load("icono.jpg")
        pygame.display.set_icon(self.icon)
        self.ventana.fill(self.BLANCA)

    # dibujar rejilla
    def rejilla(self):
        for i in range(self.columnas):
            pygame.draw.line(self.ventana, self.NEGRO, (i*self.anchoT, 0), (i*self.anchoT, self.size))
        for i in range(self.filas):
            pygame.draw.line(self.ventana, self.NEGRO, (0, i*self.altoT), (self.size, i*self.altoT))
    
    def mostrar_imagenes(self, matriz):

        imagenes = {
            0: self.blanco,
            1: self.pinocho,
            2: self.cigarros,
            3: self.negro,
            4: self.zorro,
            5: self.gepetto
        }

        for i in range(self.filas):
            for j in range(self.columnas):
                escala = pygame.transform.scale(imagenes[matriz[i][j]], [self.anchoT, self.altoT])
                self.ventana.blit(escala, [j * 100, i * 100])
            self.rejilla()
            pygame.display.update()

    def agente_recorra_matriz(self, lista):
        """

        Args:
            lista: Dato retornado por algoritmo de busqueda


        """
        contador = 0
        for coordenada in lista:
            self.escenario = np.copy(self.matriz_temporal)
            ubicacion_del_agente = algbusc.buscar_agente(self.matriz_temporal, 1)
            self.matriz_temporal[ubicacion_del_agente[0], ubicacion_del_agente[1]] = 0

            self.matriz_temporal[coordenada[0], coordenada[1]] = 1
            self.mostrar_imagenes(self.matriz_temporal)
            pygame.time.wait(1000)
            contador = contador+1
       

    def run(self):
        while self.corre:
            self.eventos()
            #----------------------------------------------------------------------------
            #FUNCION PROFUNDIDAD ITERATIVA

            ruta_bpi = algbusc.encontrar_recorrido_bpi(self.escenario, self.info_tablero)
            self.corre = self.agente_recorra_matriz(ruta_bpi)
            print(ruta_bpi)


            #----------------------------------------------------------------------------
            #FUNCION COSTO

            #busquedacosto.rutaOptima(self.escenario)
            #self.corre = self.agente_recorra_matriz(ruta_costo)


            pygame.display.flip()
        self.reloj.tick(self.FPS)
        pygame.quit()


    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.corre = False

                        
juego = Juego()
juego.run()
info = {
        'obstaculo': 3,
        'meta': 5

    }
# tablero = escenario = np.loadtxt("matriz.txt", skiprows=0)
# ruta_bpi = algbusc.encontrar_recorrido_bpi(tablero, info)

# print('resultado', ruta_bpi)
