#!/usr/bin/python3

import os

path = '/tmp/com1'
I = True
print('proceso externo')
while I:
    print('Mi pid es: '+str(os.getppid()))
    DATOS = str(input('>'))
    fifo = open(path, 'w')
    fifo.write('insertar:'+str(os.getppid())+":"+DATOS)
    fifo.close()
    print('datos: '+DATOS) 