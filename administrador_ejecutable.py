#!/usr/bin/python3

import os, sys
from src.administrador_memoria import AdministradorMemoria

##Implementacion de una maquina de estados que recibe
#ordenes desde una fifo
if __name__ == '__main__':
    path = "/tmp/com1"
    path2 = "/tmp/com2"
    try:
        os.mkfifo(path)
        os.mkfifo(path2)
        print('fifo created!')
    except OSError:
        print('fifo existe')
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
            REQUEST = ADMIN.matar_proceso(int(entrada_input[1]))
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