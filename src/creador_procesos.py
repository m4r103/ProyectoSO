#!/usr/bin/python3

import subprocess
import os
import signal

## Clase creadora de procesos
class CreadorProcesos:
    ## Lista para almacenar los objetos Popen de los subprocesos
    # Se usa un Popen para tener control sobre los procesos crados
    lista_fea = []
    ## Funcion que crea el proceso
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

    ## Obtiene el objeto Popen de la lista
    def obtener_proceso(self, pid):
        for entry in self.lista_fea:
            if entry.pid == pid:
                return entry
        return -1

    ## Desfragmenta la unidad seleccionada
    def desfragmentar(self):
        with open(path, 'w') as f:
            f.write('defrag')

    ## Envia una peticion al administrador de tarea para
    ## mover un proceso a ram o swap
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
        return request
    ## Mata al proceso selecionado a partir de su PID
    def matar_proceso(self, pid):
        entry = self.obtener_proceso(pid)
        if entry == -1:
            print('no existe el proceso')
            return
        with open(path, 'w') as f:
            f.write('matar:'+str(pid))
        self.lista_fea.remove(entry)
        entry.kill()
    ## Lista el pid de todos los procesos creados
    def listar(self):
        for i in self.lista_fea:
            print(str(i.pid))

    ## Envia una señal para pausar el proceso especificado
    def pausar(self, pid):
        for i in self.lista_fea:
            if i.pid == pid:
                try:
                    os.kill(pid, signal.SIGTSTP)
                except OSError:
                    print('error')

    ## Envia una señal para continuar el proceso especificado
    def continuar(self, pid):
        for i in self.lista_fea:
            if i.pid == pid:
                try:
                    os.kill(pid, signal.SIGCONT)
                except OSError:
                    print('error')
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
    objeto = CreadorProcesos()
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
