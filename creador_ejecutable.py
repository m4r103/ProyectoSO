#!/usr/bin/python3
import os
from src.creador_procesos import CreadorProcesos
## Funcion Main
if __name__ == '__main__':
    path = "/tmp/com1"
    path2 = "/tmp/com2"
    try:
        os.mkfifo(path)
        os.mkfifo(path2)
        print('fifo created!')
    except OSError:
        print('fifo existe')
    objeto = CreadorProcesos(path, path2)
    I = True
    while I:
        DATOS = str(input('>'))
        if DATOS.upper() == 'CREAR':
            try:
                DATOS = int(input('size > '))
                objeto.crear_proceso(DATOS)
            except ValueError:
                print('el valor especificado no es un numero')
        elif DATOS.upper() == 'MATAR':
            try:
                DATOS = int(input('proceso > '))
                objeto.matar_proceso(DATOS)
            except ValueError:
                print('el valor especificado no es un numero')                
        elif DATOS.upper() == 'LISTAR':
            objeto.listar()
        elif DATOS.upper() == 'MOVER_SWAP':
            try:
                DATOS = int(input('proceso > '))
                REQUEST = objeto.mover(DATOS, 'swap')
                if REQUEST == '0':
                    objeto.pausar(DATOS)
            except ValueError:
                print('el valor especificado no es un numero')                
        elif DATOS.upper() == 'MOVER_RAM':
            try:
                DATOS = int(input('proceso > '))
                REQUEST = objeto.mover(DATOS, 'ram')
                if REQUEST == '0':
                    objeto.continuar(DATOS)
            except ValueError:
                print('el valor especificado no es un numero')
        elif DATOS.upper() == 'DEFRAG':
            objeto.desfragmentar()
        elif DATOS.upper() == 'SALIR':
            for entry in objeto.lista_fea:
                entry.kill()
            with open(path, 'w') as file:
                file.write('salir')
            break
    os.unlink(path)
    os.unlink(path2)
