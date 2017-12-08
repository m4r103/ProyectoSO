import math
from src.entrada_tabla import EntradaTabla
from src.datos_unidad import Datos

##Clase del administrador
class AdministradorMemoria:
    tabla = []
    ram = []
    swap = []
    ## Constructor del objeto
    def __init__(self):
        for i in range(0, 500):
            datos = Datos(-1, '0')
            self.ram.append(datos)
            datos = Datos(-1, '0')
            self.swap.append(datos)
    ## Crea un nuevo proceso
    def agregar_proceso(self, pid, tam):
        tam = self.convertir_tamanio(tam)
        inicio = self.obtener_segmento_libre(tam, self.ram)
        if inicio == -1:
            print('No hay memoria RAM suficiente')
            return
        foo = EntradaTabla(pid, inicio, tam, 'ram')
        self.tabla.append(foo)
        self.cargar_en_unidad(foo, self.ram)

    ## Inserta datos a partir del PID
    # Busca la entrada en la tabla a paritr del pid,
    # y la pasa para cargar datos.
    def insertar_datos(self, pid, datos):
        for entry in self.tabla:
            if entry.pid == pid:
                if entry.unidad == 'ram':
                    self.cargar_datos_en_unidad(entry, datos, self.ram)
                    return 0
                return -1
        print('Proceso no encontrado')
        return -2

    ## Inserta los datos a una unidad deseada a partir de una entrada de tabla
    def cargar_datos_en_unidad(self, entrada, datos, unidad):
        for i in range(entrada.dir_fisica_inicio, entrada.dir_fisica_fin):
            unidad[i].datos = datos
    ## Le inidica a la unidad seleccionda la zona de memoria que ha sido usada
    def cargar_en_unidad(self, entrada, unidad):
        for i in range(entrada.dir_fisica_inicio, entrada.dir_fisica_fin):
            unidad[i].pid = entrada.pid

    def convertir_tamanio(self, tam):
        return math.ceil(float(tam/4))
    ## Conseguir l a direccion de memoria de una unidad
    # con un tamaño suficientemente grande
    def obtener_segmento_libre(self, tam, unidad):
        inicio = -1
        cont = 0
        for i in range(0, 500):
            if unidad[i].pid == -1: ## Verificamos que la zona este libre
                cont = 0
                inicio = i
                for j in range(inicio, 500):
                    cont = cont+1
                    ## Si una localidad de memoria esta usada o si se alcanzo el tamaño deseado
                    # se rompe el ciclo
                    if unidad[j].pid!= -1 or cont == tam:
                        break
            if cont == tam: ## Si se consiguio la cantidad de ram deseada se regresa el indice del inicio
                return inicio
        return -1 ## En caso de error se retorna un -1
    ## Mata el proceso especificado mediante el PID
    def matar_proceso(self, pid):
        for entry in self.tabla:
            if entry.pid == pid: ## Verificamos que el proceso Existe
                if entry.unidad == 'ram': ## Verificamos si esta en ram
                    self.descargar_de_unidad(entry, self.ram)
                elif entry.unidad == 'swap': ## Verificamos si esta en swap
                    self.descargar_de_unidad(entry, self.swap)
                ## Eliminamos la entrada de la tabla
                self.tabla.remove(entry)
                return
        print('Proceso no econtrado')
    ## Quita todos los datos de la zona de memoria asignada y regresa los datos a 0
    def descargar_de_unidad(self, entry, unidad):
        for i in range(entry.dir_fisica_inicio, entry.dir_fisica_fin):
            unidad[i].datos = '0'
            unidad[i].pid = -1
    ## Funcion para dibujar una unidad de memoria
    def dibujar(self, unidad):
        contador = 0
        for entry in unidad:
            print(' '+entry.datos, end='')
            contador = contador+1
            if contador.__mod__(25) == 0:
                print(' 0x'+str(contador))

    #Funcion para mover un proceso a ram
    def mover_ram(self, pid):
        for entry in self.tabla:
            if entry.pid == pid: ## Verificamos que el proceso exista
                if entry.unidad != 'swap': ## Verificamos que este en swap
                    print('El proceso no esta en SWAP')
                    return -3
                inicio = self.obtener_segmento_libre(entry.size, self.ram)
                if inicio == -1: ## Verificamos que exista ram disponible
                    print('No hay suficiente memoria RAM')
                    return -1
                ## Movemos a ram
                self.tabla.remove(entry)
                datos = self.swap[entry.dir_fisica_inicio].datos
                self.descargar_de_unidad(entry, self.swap)
                entry.unidad = 'ram'
                foo = EntradaTabla(entry.pid,inicio,entry.size, 'ram')
                self.tabla.append(foo)
                self.cargar_en_unidad(foo,self.ram)
                self.cargar_datos_en_unidad(foo, datos, self.ram)
                return 0
        print('No se encontro el proceso')
        return -2

    ## Funcion para mover un proceso a swap
    def mover_swap(self, pid):
        for entry in self.tabla:
            if entry.pid == pid: ## Verificamos que el proceso existe
                if entry.unidad != 'ram': ## Verificamos que el proceso esta en RAM
                    print('El proceso no esta en RAM')
                    return -3
                inicio = self.obtener_segmento_libre(entry.size, self.swap)
                if inicio == -1: ## Verificamos que hay suficiente memoria SWAP
                    print('No hay suficiente memoria SWAP')
                    return -1
                ## Movemos el proceso a SWAP
                self.tabla.remove(entry)
                datos = self.ram[entry.dir_fisica_inicio].datos
                self.descargar_de_unidad(entry, self.ram)
                entry.unidad = 'swap'
                foo = EntradaTabla(entry.pid, inicio, entry.size, 'swap')
                self.tabla.append(foo)
                self.cargar_en_unidad(foo, self.swap)
                self.cargar_datos_en_unidad(foo, datos, self.swap)
                return 0
        print('No se econtro el proceso')
        return -2
    #  Fucnion para desfragmentar 
    #  La desfragmentacion se hace mediante el ordenado de la tabla
    #  de forma ascendente a partir de la direccion fisica de inicio
    #  de cada entrada de la tabla, posteriormente se recorren los datos
    #  a la nueva localidad iniciando desde cero
    def desfragmentar(self):
        inicio = 0
        self.tabla = sorted(self.tabla, key=lambda entrada: entrada.dir_fisica_inicio)
        for entry in self.tabla:
            # Solo si esta en ram se movera el proceso
            if entry.unidad == 'ram':
                # Si la nueva direccion de inicio es distinta a su antigua direccion,
                # entonces el proceso se movera
                if entry.dir_fisica_inicio != inicio:
                    # Se barre el segmento
                    for i in range(0, entry.size):
                        # Debido a la naturaleza de python, los objetos se pasan por
                        # referencia y no por valor, asi que es necesario crear
                        # un nuevo objeto de tipo dato con los datos del anterio
                        # para evitar parasitaje
                        d = self.ram[entry.dir_fisica_inicio+i]
                        t = Datos(d.pid,d.datos)
                        # Se modifica la ram
                        self.ram[entry.dir_fisica_inicio+i].datos = '0'
                        self.ram[entry.dir_fisica_inicio+i].pid = -1
                        self.ram[inicio+i] = t
                    # Se actualiza la entra de la tabla
                    entry.dir_fisica_inicio = inicio
                    entry.dir_fisica_fin = inicio+entry.size
                # Ahora la direccion de inicio del proximo proceso
                # será a partir de la dirección fisica del proceso anterior
                inicio = entry.dir_fisica_fin