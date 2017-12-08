#!/usr/bin/python3

import math
import os, sys
##Clase de entrada en tabla
class EntradaTabla:
    pid = -1
    dir_fisica_inicio = -1
    dir_fisica_fin = -1
    size = -1
    unidad = -1
    ## Constructor del objeto
    def __init__(self, pid, dir_fisica, size, unidad):
        self.pid = pid
        self.size = size
        self.dir_fisica_inicio = dir_fisica
        self.dir_fisica_fin = dir_fisica + size
        self.unidad = unidad

##Clase de Datos
class Datos:
    ## Constructor del objeto
    def __init__(self, pid, datos):
        self.pid = pid
        self.datos = datos

##Clase del administrador
class AdministradorMemoria:
    tabla = []
    ram = []
    swap = []
    ## Constructor del objeto
    def __init__(self):
        for i in range(0, 500):
            datos = Datos(-1, '0')
            self.ram.append(datos)
            datos = Datos(-1, '0')
            self.swap.append(datos)
    ## Crea un nuevo proceso
    def agregar_proceso(self, pid, tam):
        tam = self.convertir_tamanio(tam)
        inicio = self.obtener_segmento_libre(tam, self.ram)
        if inicio == -1:
            print('No hay memoria RAM suficiente')
            return
        foo = EntradaTabla(pid, inicio, tam, 'ram')
        self.tabla.append(foo)
        self.cargar_en_unidad(foo, self.ram)

    ## Inserta datos a partir del PID
    # Busca la entrada en la tabla a paritr del pid,
    # y la pasa para cargar datos.
    def insertar_datos(self, pid, datos):
        for entry in self.tabla:
            if entry.pid == pid:
                if entry.unidad == 'ram':
                    self.cargar_datos_en_unidad(entry, datos, self.ram)
                    return 0
                return -1
        print('Proceso no encontrado')
        return -2

    ## Inserta los datos a una unidad deseada a partir de una entrada de tabla
    def cargar_datos_en_unidad(self, entrada, datos, unidad):
        for i in range(entrada.dir_fisica_inicio, entrada.dir_fisica_fin):
            unidad[i].datos = datos
    ## Le inidica a la unidad seleccionda la zona de memoria que ha sido usada
    def cargar_en_unidad(self, entrada, unidad):
        for i in range(entrada.dir_fisica_inicio, entrada.dir_fisica_fin):
            unidad[i].pid = entrada.pid

    def convertir_tamanio(self, tam):
        return math.ceil(float(tam/4))
    ## Conseguir l a direccion de memoria de una unidad
    # con un tamaño suficientemente grande
    def obtener_segmento_libre(self, tam, unidad):
        inicio = -1
        cont = 0
        for i in range(0, 500):
            if unidad[i].pid == -1: ## Verificamos que la zona este libre
                cont = 0
                inicio = i
                for j in range(inicio, 500):
                    cont = cont+1
                    ## Si una localidad de memoria esta usada o si se alcanzo el tamaño deseado
                    # se rompe el ciclo
                    if unidad[j].pid!= -1 or cont == tam:
                        break
            if cont == tam: ## Si se consiguio la cantidad de ram deseada se regresa el indice del inicio
                return inicio
        return -1 ## En caso de error se retorna un -1
    ## Mata el proceso especificado mediante el PID
    def matar_proceso(self, pid):
        for entry in self.tabla:
            if entry.pid == pid: ## Verificamos que el proceso Existe
                if entry.unidad == 'ram': ## Verificamos si esta en ram
                    self.descargar_de_unidad(entry, self.ram)
                elif entry.unidad == 'swap': ## Verificamos si esta en swap
                    self.descargar_de_unidad(entry, self.swap)
                ## Eliminamos la entrada de la tabla
                self.tabla.remove(entry)
                return
        print('Proceso no econtrado')
    ## Quita todos los datos de la zona de memoria asignada y regresa los datos a 0
    def descargar_de_unidad(self, entry, unidad):
        for i in range(entry.dir_fisica_inicio, entry.dir_fisica_fin):
            unidad[i].datos = '0'
            unidad[i].pid = -1
    ## Funcion para dibujar una unidad de memoria
    def dibujar(self, unidad):
        contador = 0
        for entry in unidad:
            print(' '+entry.datos, end='')
            contador = contador+1
            if contador.__mod__(25) == 0:
                print(' 0x'+str(contador))

    #Funcion para mover un proceso a ram
    def mover_ram(self, pid):
        for entry in self.tabla:
            if entry.pid == pid: ## Verificamos que el proceso exista
                if entry.unidad != 'swap': ## Verificamos que este en swap
                    print('El proceso no esta en SWAP')
                    return -3
                inicio = self.obtener_segmento_libre(entry.size, self.ram)
                if inicio == -1: ## Verificamos que exista ram disponible
                    print('No hay suficiente memoria RAM')
                    return -1
                ## Movemos a ram
                self.tabla.remove(entry)
                datos = self.swap[entry.dir_fisica_inicio].datos
                self.descargar_de_unidad(entry, self.swap)
                entry.unidad = 'ram'
                foo = EntradaTabla(entry.pid,inicio,entry.size, 'ram')
                self.tabla.append(foo)
                self.cargar_en_unidad(foo,self.ram)
                self.cargar_datos_en_unidad(foo, datos, self.ram)
                return 0
        print('No se encontro el proceso')
        return -2

    ## Funcion para mover un proceso a swap
    def mover_swap(self, pid):
        for entry in self.tabla:
            if entry.pid == pid: ## Verificamos que el proceso existe
                if entry.unidad != 'ram': ## Verificamos que el proceso esta en RAM
                    print('El proceso no esta en RAM')
                    return -3
                inicio = self.obtener_segmento_libre(entry.size, self.swap)
                if inicio == -1: ## Verificamos que hay suficiente memoria SWAP
                    print('No hay suficiente memoria SWAP')
                    return -1
                ## Movemos el proceso a SWAP
                self.tabla.remove(entry)
                datos = self.ram[entry.dir_fisica_inicio].datos
                self.descargar_de_unidad(entry, self.ram)
                entry.unidad = 'swap'
                foo = EntradaTabla(entry.pid, inicio, entry.size, 'swap')
                self.tabla.append(foo)
                self.cargar_en_unidad(foo, self.swap)
                self.cargar_datos_en_unidad(foo, datos, self.swap)
                return 0
        print('No se econtro el proceso')
        return -2

    def desfragmentar(self):
        inicio = 0
        self.tabla = sorted(self.tabla, key=lambda entrada: entrada.dir_fisica_inicio)
        for entry in self.tabla:
            if entry.unidad == 'ram':
                if entry.dir_fisica_inicio != inicio:
                    for i in range(0, entry.size):
                        d = self.ram[entry.dir_fisica_inicio+i]
                        t = Datos(d.pid,d.datos)
                        self.ram[entry.dir_fisica_inicio+i].datos = '0'
                        self.ram[entry.dir_fisica_inicio+i].pid = -1
                        self.ram[inicio+i] = t
                    entry.dir_fisica_inicio = inicio
                    entry.dir_fisica_fin = inicio+entry.size
                inicio = entry.dir_fisica_fin

##Implementacion de una maquina de estados que recibe
#ordenes desde una fifo
if __name__ == '__main__':
    path = "/tmp/com1"
    path2 = "/tmp/com2"
    ADMIN = AdministradorMemoria()
    I = True
    while I:    
        fifo = open(path, 'r')
        entrada_input = fifo.read().split(':')
        fifo.close()
        os.system('clear')
        if entrada_input[0] == 'hay_memoria':
            REQUEST = -1
            T = ADMIN.convertir_tamanio(int(entrada_input[1]))
            if entrada_input[2] == 'ram':
                REQUEST = ADMIN.obtener_segmento_libre(T, ADMIN.ram)
            elif entrada_input[2] == 'swap':
                REQUEST = ADMIN.obtener_segmento_libre(T, ADMIN.swap)
            with open(path2, 'w') as f:
                f.write(str(REQUEST))
        elif entrada_input[0] == 'crear':
            ADMIN.agregar_proceso(int(entrada_input[1]), int(entrada_input[2]))
        elif entrada_input[0] == 'insertar':
            REQUEST = ADMIN.insertar_datos(int(entrada_input[1]), entrada_input[2])
        elif entrada_input[0] == 'matar':
            ADMIN.matar_proceso(int(entrada_input[1]))
        elif entrada_input[0] == 'mover_swap': 
            REQUEST = ADMIN.mover_swap(int(entrada_input[1]))
            with open(path2, 'w') as f:
                f.write(str(REQUEST))
        elif entrada_input[0] == 'mover_ram':
            REQUEST = ADMIN.mover_ram(int(entrada_input[1]))
            with open(path2, 'w') as f:
                f.write(str(REQUEST))
        elif entrada_input[0] == 'salir':
            break
        elif entrada_input[0] == 'defrag':
            ADMIN.desfragmentar()

        print('\n\n:::RAM:::')
        ADMIN.dibujar(ADMIN.ram)
        print('\n\n:::SWAP:::')
        ADMIN.dibujar(ADMIN.swap)