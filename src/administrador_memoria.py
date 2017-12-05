#!/usr/bin/python3

import math

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
        self.dir_fisica_fin = dir_fisica + (size-1)
    
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

class AdministradorMemoria:
    tabla = []
    ram = []
    swap = []
    def __init__(self):
        for i in range(0, 500):
            datos = Datos(-1, ' ')
            self.ram.append(datos)
            self.swap.append(datos)

    def agregar_proceso(self, pid, tam):
        tam = self.convertir_tamanio(tam)
        if tam < 500 and self.tabla.count == 0:
            self.tabla.append(EntradaTabla(pid, 0, tam))
            return
        inicio = self.obtener_segmento_libre(tam)
        if inicio != -1:
            self.tabla.append(EntradaTabla(pid,inicio,tam))
            return
        else:
            print('No hay memoria suficiente')    

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
                    if self.ram[j].get_pid() != -1:
                        break
                    cont = cont+1
            if cont == tam:
                return inicio
        return -1

    def dibujar(self):
        for entry in self.ram:
            print(entry.datos)




        
if __name__ == '__main__':
    ADMIN = AdministradorMemoria()
    I = True
    while I:
        entrada = input('prompt > ')
        if entrada == 'crear':
            pid = int(input('pid >'))
            tam = int(input('tam >'))
            ADMIN.agregar_proceso(pid,tam)
        elif entrada == 'salir':
            break