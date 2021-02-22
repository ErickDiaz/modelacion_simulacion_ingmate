import random
import math


class Operador(object):
    def __init__(self, nombre, tiempo_prob):
        self.nombre = nombre
        self.tiempo_prob = tiempo_prob

class Evento(object):
    def __init__(self, tipo, estado):
        self.tipo = tipo
        self.estado = estado
        
class Estado(object):
    def __init__(self, tiempo, estado_operador, cola):
        self.tiempo = tiempo
        self.estado_operador = estado_operador
        self.cola = cola
        
def aleatorio_exponencial(val_lambda):
    ## Funcion que genera variable aleatoria exponencial de parameto lambda
    
    # Generar numero aleatorio
    num = random.uniform(0,1)
    
    return -1 * math.log(num)/val_lambda
    
def tiempo_aleatorio_operador(dict_operador):
    ## Genera una variable aleatoria discreta siguiendo la prob. del operador
    tiempo = 0
    num = random.uniform(0,1);

    for rango, valor in dict_operador.items():
        inicio, fin = rango
        if(num >= inicio) and (num < fin):
            tiempo = valor

    return tiempo


def get_tiempo(evento):
    return evento.estado.tiempo


def inserta_evento(evento, lista_eventos):
    lista_eventos.append(evento)
    lista_eventos.sort(key=get_tiempo)
    
    return lista_eventos


def nuevo_cliente(estado, dict_operador,evento_actual, eventos_futuros):
    
    estado.tiempo = evento_actual.estado.tiempo
    
    if estado.estado_operador == 1:
        ## Si esta ocupado
        estado.cola += 1
    else:
        estado.estado_operador = 1
        
        tiempo_fin = tiempo_aleatorio_operador(dict_operador) + evento_actual.estado.tiempo
        nuevo_estado = Estado(tiempo_fin, estado.estado_operador, estado.cola)
        
        nuevo_evento = Evento('final_cliente', nuevo_estado)
        
        eventos_futuros = inserta_evento(nuevo_evento, eventos_futuros)
        
    return eventos_futuros, estado

def final_cliente(estado, dict_operador,evento_actual, eventos_futuros):
    estado.tiempo = evento_actual.estado.tiempo
    
    if(estado.cola > 0):
        # Si hay cola se saca a uno de la cola
        estado.cola -= 1
        
        tiempo_fin = tiempo_aleatorio_operador(dict_operador) + estado.tiempo
        nuevo_estado = Estado(tiempo_fin, estado.estado_operador, estado.cola)
        
        nuevo_evento = Evento('final_cliente', nuevo_estado)
        
        eventos_futuros = inserta_evento(nuevo_evento, eventos_futuros)
    else:
        # Si no hay cola
        estado.estado_operador = 0

        
    return eventos_futuros, estado