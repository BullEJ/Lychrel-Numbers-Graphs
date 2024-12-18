# Entendemos target ln al objeto de abstracción n
# donde la abstracción n consiste en la clase de equivalencia n veces
# definido de manera recursiva, donde dos target l(n-1) son equivalentes
# como target ln si su sucesores coinciden en l(n-1)

import shutil
from os.path import join, exists
from os import remove
from functools import reduce
from itertools import product, combinations, dropwhile, takewhile

import time

# Para ramas.py
    # Condicionadores de existencia
def blq(t: tuple, i: int, c_pos = True): # c_pos = condición de positividad
    try:
        if c_pos and 0 > i: raise IndexError
        return t[i]
    except IndexError: return 0

def is_seed_t1l9(fri):
    pass

def is_seed_t1ln9(fri):
    pass

def is_seed_t2l9(fri):
    pass

def is_seed_t2ln9(fri):
    pass

def is_seed(fri: tuple[int]) -> bool:
    return (is_seed_t1l9(fri) or is_seed_t1ln9(fri) or
            is_seed_t2l9(fri) or is_seed_t2ln9(fri))

    # Algoritmos para obtener antecesores.
    # Acá se presupone que los fri_s entregados cumplen las condiciones para
    # poseer antecesor de cierto tipo.
def T1l9(fri_s: tuple[int], paridad: int):
    C  = [0] + reduce(
                lambda c, i: c + ((blq(c, -2, False) + i) % 2, ),
                fri_s[:-1], tuple())
    MC = (blq(C, i-1) + blq(C, i+1) for i in range(len(C)))
    MC = MC[:-1] + tuple(MC[-1] + blq(C, -1 - paridad, False))
    
    yield tuple(int(0.5 * (fri_s[i] - MC[i])) + 10 * C[i]
             for i in range(len(C)))

def T1ln9(fri_s: tuple[int]):#, paridad: int):
    
    def all_combinations():
        # Extraer posiciones nueves.
        secuencias_nueves = []
        secuencia_actual  = []
        
            # Iteramos sobre la fri_s
        for indice, num in enumerate(fri_s[1:-1], 1):
            if num == 9:
                secuencia_actual.append(indice)
            else:
                if secuencia_actual: 
                    secuencias_nueves.append(tuple(secuencia_actual))
                    secuencia_actual = [] 
        
            # Si al final de la iteración aún hay una secuencia de 9's
        if secuencia_actual:
            secuencias_nueves.append(tuple(secuencia_actual))

        for r in range(1, len(secuencias_nueves) + 1):
            yield from combinations(secuencias_nueves, r)

    def remover_bloques(set_bloques):
        for bloque in set_bloques:
            if len(bloque) > 2:
                return tuple()

    for set_blqs in all_combinations():


def T2l9(fri_s: tuple[int], paridad: int):
    BS = reduce(
            lambda c, i: c + tuple(i - blq(c, -1, False), ),
            fri_s, tuple())

    for infc in product({0, 1}, repeat = len(fri_s) - 1 - paridad):
        yield tuple(BS[i] + 9 * ((1,) + infc)[i] for i in range(len(infc) + 1))

def T2ln9(fri: tuple[int]):
    pass

def antecesores(fri: tuple[int], paridad):
    yield from T1l9(fri, paridad)
    yield from T1ln9(fri, paridad)
    yield from T2l9(fri, paridad)
    yield from T2ln9(fri, paridad)

    #Miscelaneos
def falta_completar(nodos) -> tuple[tuple]:
    # Retorna los FRI que no son semilla
    # nodos es un generador
    return tuple(filter(
                    lambda nodo: not is_seed(nodo),
                    nodos))

# Para main.py
def guardar(coleccion: list[tuple], clase: tuple) -> None:
    try:
        if exists(join("clases", f"{clase}.txt")):
            shutil.copy(
                join("clases", f"{clase}.txt"),
                join("clases", f"{clase}.tmp"))

        with open(join("clases", f"{clase}.tmp"), "a") as file:
            file.write("".join(f"{fri}" for fri in coleccion))
        
        # Si todo salió bien, reemplazamos el archivo original con el temporal
        shutil.move(
            join("clases", f"{clase}.tmp"),
            join("clases", f"{clase}.txt"))

        print(f"Recolectamos de {clase}")
    
    except:
        print(f"Ocurrió un error durante la escritura de {clase}")
        
        # Si ocurre algún error, eliminamos el archivo temporal
        if  exists(join("clases", f"{clase}.tmp")):
            remove(join("clases", f"{clase}.tmp"))
        
        print("El archivo no ha sido modificado.")
        raise(KeyboardInterrupt)

# Sin usar:
# def sucesor_l0(numero: int) -> int:
#     # Sucesor desde el target l0
#     return numero + int(str(numero)[::-1])

# def denotar(numero: int) -> list[int]:
#     # Pasa de un target de l0 a l1
#     l1, formato = list(), str(numero)
#     for k in range((len(formato)+1)//2):
#         l1.append(int(formato[k])+int(formato[-k-1]))
    
#     del formato
#     return l1