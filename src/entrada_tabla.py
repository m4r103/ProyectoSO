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