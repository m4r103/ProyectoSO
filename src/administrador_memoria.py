#!/usr/bin/python3

import math
##Clase de entrada en tabla
class EntradaTabla:
    pid = -1
    dir_fisica_inicio = -1
    dir_fisica_fin = -1
    size = -1
    unidad = -1
    def __init__(self, pid, dir_fisica, size):
        self.pid = pid
        self.size = size
        self.dir_fisica_inicio = dir_fisica
        self.dir_fisica_fin = dir_fisica + size
    
    def get_pid(self):
        return self.pid

    def get_dir_inicio(self):
        return self.dir_fisica_inicio

    def get_dir_fin(self):
        return self.dir_fisica_fin

    def get_unidad(self):
        return self.unidad
    def set_unidad(self, unidad):
        self.unidad = unidad

##Clase de Datos
class Datos:
    def __init__(self, pid, datos):
        self.pid = pid
        self.datos = datos

    def set_datoss(self, datos):
        self.datos = datos

    def get_pid(self):
        return self.pid
    def get_datos(self):
        return self.datos

##Clase del administrador
class AdministradorMemoria:
    tabla = []
    ram = []
    swap = []
    def __init__(self):
        for i in range(0, 500):
            datos = Datos(-1, '0')
            self.ram.append(datos)
            self.swap.append(datos)

    def agregar_proceso(self, pid, tam):
        tam = self.convertir_tamanio(tam)
        inicio = self.obtener_segmento_libre(tam)
        if inicio == -1:
            print('No hay memoria suficiente')
            return 
        entrada = EntradaTabla(pid, inicio, tam)
        self.tabla.append(entrada)
        self.cargar_en_ram(entrada)
        
    
    def cargar_en_ram(self,entrada):
        for i in range(entrada.dir_fisica_inicio,entrada.dir_fisica_fin):
            self.ram[i].pid = entrada.get_pid()
            self.ram[i].datos = entrada.get_pid()
        

    def convertir_tamanio(self, tam):
        return math.ceil(float(tam/4))

    def obtener_segmento_libre(self, tam):
        inicio = -1
        cont = 0
        for i in range(0, 500):
            if self.ram[i].get_pid() == -1:
                cont = 0
                inicio = i
                for j in range(inicio, 500):
                    cont = cont+1
                    if self.ram[j].get_pid() != -1 or cont == tam:
                        break
            if cont == tam:
                return inicio
        return -1

    def matar_proceso(self, pid):
        for entry in self.tabla:
            if entry.pid == pid:
                self.descargar_de_ram(entry)
                self.tabla.remove(entry)
                return
        print('Proceso no econtrado')

    def descargar_de_ram(self, entry):
        for i in range(entry.dir_fisica_inicio, entry.dir_fisica_fin):
            self.ram[i].datos = '0'
            self.ram[i].pid = -1

    def dibujar(self):
        contador = 0
        for entry in self.ram :
            print(' '+entry.datos,end='')
            contador =  contador + 1
            if contador.__mod__(25) == 0:
                print(' 0x'+str(contador))



##Aqui se implementara una maquina de estados que recibe
#ordenes desde una fifo
if __name__ == '__main__':
    ADMIN = AdministradorMemoria()
    I = True
    while I:
        entrada = input('prompt > ')
        if entrada == 'crear':
            pid = int(input('pid > '))
            tam = int(input('tam > '))
            ADMIN.agregar_proceso(pid,tam)
        elif entrada == 'matar':
            pid = int(input('pid > '))
            ADMIN.matar_proceso(pid)
        elif entrada == 'salir':
            break
        elif entrada == 'dibujar':
            ADMIN.dibujar()