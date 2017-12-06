#!/usr/bin/python3

import subprocess
import os

class CreadorProcesos:
    lista_fea = []
    def crear_proceso(self, param):
        with open(path, 'w') as f:
            f.write('hay_memoria:'+str(param)+':ram')
        with open(path2, 'r') as f:
            request = f.read()
        if request == '-1':
            print('No hay RAM suficiente')
            return
        proceso = subprocess.Popen(['xterm', '-e', './externo.py'])
        print('pid: '+str(proceso.pid))
        with open(path, 'w') as f:
            f.write('crear:'+str(proceso.pid)+':'+str(param))
        self.lista_fea.append(proceso)
    def obtener_proceso(self, pid):
        for entry in self.lista_fea:
            if entry.pid == pid:
                return entry
        return -1

    def mover(self, pid, unidad):
        if self.obtener_proceso(pid) == -1:
            print('No existe el proceso')
        with open(path, 'w') as f:
            f.write('mover_'+unidad+':'+str(pid))
        with open(path2, 'r') as f:
            request = f.read()
        if request == '-1':
            print('No hay espacio suficiente en '+unidad.upper())
            return
        elif request == '-2':
            print('No existe el proceso en la tabla')
            return
        elif request == '-3':
            print('El proceso no esta en '+unidad.upper())
        elif request == '0':
            print('El proceso se ha movido a '+unidad.upper())
                
                    

    def matar_proceso(self, pid):
        entry = self.obtener_proceso(pid)
        if entry == -1:
            print('no existe el proceso')
            return
        with open(path, 'w') as f:
            f.write('matar:'+str(pid))
        self.lista_fea.remove(entry)
        entry.kill()

    def listar(self):
        for i in self.lista_fea:
            print(str(i.pid))

if __name__ == '__main__':
    path = "/tmp/com1"
    path2 = "/tmp/com2"
    try:
        os.mkfifo(path)
        os.mkfifo(path2)
        print('fifo created!')
    except OSError:
        print('fifo existe')
    objeto = CreadorProcesos()
    I = True
    while I:
        DATOS = str(input('>'))
        if DATOS.upper() == 'CREAR':
            DATOS = int(input('size > '))
            objeto.crear_proceso(DATOS)
        elif DATOS.upper() == 'MATAR':
            DATOS = int(input('proceso > '))
            objeto.matar_proceso(DATOS)
        elif DATOS.upper() == 'LISTAR':
            objeto.listar()
        elif DATOS.upper() == 'MOVER_SWAP':
            DATOS = int(input('proceso > '))
            objeto.mover(DATOS,'swap')
        elif DATOS.upper() == 'MOVER_RAM':
            DATOS = int(input('proceso > '))
            objeto.mover(DATOS,'ram')
        elif DATOS.upper() == 'SALIR':
            for entry in objeto.lista_fea:
                entry.kill()
            with open(path, 'w') as file:
                file.write('salir')
            break
    os.unlink(path)
    os.unlink(path2)
