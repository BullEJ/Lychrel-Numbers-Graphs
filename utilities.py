# Entendemos target ln al objeto de abstracción n
# donde la abstracción n consiste en la clase de equivalencia n veces
# definido de manera recursiva, donde dos target l(n-1) son equivalentes
# como target ln si su sucesores coinciden en l(n-1)

import shutil
from os.path import join, exists
from os import remove
from functools import reduce
from itertools import product

# Para ramas.py
    # Condicionadores de existencia
def blq(l: list, i: int, c_pos = True): # c_pos = condición de positividad
    try:
        if c_pos and 0 > i: raise IndexError
        return l[i]
    except IndexError: return 0

def is_seed_t1l9(fri):
    pass

def is_seed_t1ln9(fri):
    pass

def is_seed_t2l9(fri):
    pass

def is_seed_t2ln9(fri):
    pass

def is_seed(fri: list[int]) -> bool:
    return (is_seed_t1l9(fri) or is_seed_t1ln9(fri) or
            is_seed_t2l9(fri) or is_seed_t2ln9(fri))

    # Algoritmos para obtener antecesores.
    # Acá se presupone que los fri_s entregados cumplen las condiciones para
    # poseer antecesor de cierto tipo.
def T1l9(fri_s: list[int], paridad: int) -> list[list]:
    C  = [0] + reduce(
                lambda c, i: c + [(blq(c, -2, False) + i) % 2],
                fri_s[:-1], [])
    MC = [blq(C, i-1) + blq(C, i+1) for i in range(len(C))]
    MC = MC[:-1] + [MC[-1] + C[-1 - paridad]]
    
    yield [int(0.5 * (fri_s[i] - MC[i])) + 10 * C[i]
             for i in range(len(C))]

def T1ln9(fri: list[int]) -> list[list]:
    pass

def T2l9(fri_s: list[int], paridad: int) -> list[list]:
    BS = reduce(
            lambda c, i: c + [i - blq(c, -1, False)],
            fri_s, [])

    for infc in product({0, 1}, repeat = len(fri_s) - 1 - paridad):
        yield [BS[i] + 9 * ((1,) + infc)[i] for i in range(len(infc) + 1)]

def T2ln9(fri: list[int]) -> list[list]:
    pass

def antecesores(fri: list[int], paridad):
    yield from T1l9(fri, paridad)
    yield from T1ln9(fri, paridad)
    yield from T2l9(fri, paridad)
    yield from T2ln9(fri, paridad)

    #Miscelaneos
def falta_completar(nodos: set[tuple]) -> set[tuple]:
    # Retorna los FRI que no son semilla
    return set(filter(
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