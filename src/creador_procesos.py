#!/usr/bin/python3

import subprocess

class CreadorProcesos:
    lista_fea = []
    def crear_proceso(self, param):
        self.lista_fea.append(subprocess.Popen(['xterm', '-e', './externo.py', param]))
    def matar_proceso(self, param):
        foo = self.lista_fea[param]
        self.lista_fea.remove(foo)
        foo.kill()
        
if __name__ == '__main__':
    objeto = CreadorProcesos()
    I = True
    while I:
        DATOS = str(input('>'))
        if DATOS.upper() == 'CREAR':
            objeto.crear_proceso('')
        elif DATOS.upper() == 'MATAR':
            DATOS = int(input('proceso > '))
            objeto.matar_proceso(DATOS)
        elif DATOS.upper() == 'SALIR':
            break
