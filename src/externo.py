#!/usr/bin/python3

I = True
print('proceso externo')
while I:
    DATOS = str(input('>'))
    if DATOS.upper == 'SALIR':
        break
    print('datos: '+DATOS) 