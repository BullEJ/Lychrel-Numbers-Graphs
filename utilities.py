# Entendemos target ln al objeto de abstracción n
# donde la abstracción n consiste en la clase de equivalencia n veces
# definido de manera recursiva, donde dos target l(n-1) son equivalentes
# como target ln si su sucesores coinciden en l(n-1)

from itertools import product, combinations, chain
from shutil import copy, move
from os.path import join, exists
from os import remove
from functools import reduce
from more_itertools import powerset

# Para main.py
def guardar(coleccion: list[tuple], clase: tuple) -> None:
    try:
        if exists(join("clases", f"{clase}.txt")):
            copy(
                join("clases", f"{clase}.txt"),
                join("clases", f"{clase}.tmp"))

        with open(join("clases", f"{clase}.tmp"), "a") as file:
            file.write("".join(f"{fri}" for fri in coleccion))
        
        # Si todo salió bien, reemplazamos el archivo original con el temporal
        move(
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

# Para ramas.py
    # Extras
def blq(t: tuple, i: int, c_pos = True): # c_pos = condición de positividad
    try:
        if c_pos and 0 > i: raise IndexError
        return t[i]
    except IndexError: return 0

    # Condicionadores de existencia
def is_seed_t1l9(fri, paridad):
    # Debe considerar incluso los 0 provenientes de nueves.
    pass

def is_seed_t1ln9(fri, paridad):
    pass

def is_seed_t2l9(fri, paridad):
    pass

def is_seed_t2ln9(fri, paridad):
    pass

def is_seed(fri: tuple[int]) -> bool:
    return (is_seed_t1l9(fri) or is_seed_t1ln9(fri) or
            is_seed_t2l9(fri) or is_seed_t2ln9(fri))

    # Algoritmos para obtener antecesores.
    # Acá se presupone que los fri_s entregados cumplen las condiciones para
    # poseer antecesor de cierto tipo.
def T1l9(fri_s: tuple[int], paridad: int):
    C  = (0,) + reduce(
                lambda c, i: c + ((blq(c, -2, False) + i) % 2, ),
                fri_s[:-1], tuple())
    MC = tuple(blq(C, i-1) + blq(C, i+1) for i in range(len(C)))
    MC = MC[:-1] + (MC[-1] + blq(C, -1 - paridad, False), )
    
    yield tuple(int(0.5 * (fri_s[i] - MC[i])) + 10 * C[i]
             for i in range(len(C)))

def T1ln9(fri_s: tuple[int], paridad: int): # Optimizar código
    
    def all_combinations():
        # Extraer posiciones nueves.
        # Cada generado contiene los de largo mayor a 2 por lema que dice:
        #   Si un fri tiene una cadena de 9's mayor a 2, no tiene T1l9.
        sec_nueves = [[], []] # [[de largos menor a 3], [de largos mayor a 2]]
        sec_actual = []
        
            # Iteramos sobre la fri_s
        for indice, num in enumerate(fri_s[1:-1], 1):
            if num == 9:
                sec_actual.append(indice)
            elif sec_actual: 
                sec_nueves[len(sec_actual) > 2].append(sec_actual)
                sec_actual = [] 
        
            # Si al final de la iteración aún hay una secuencia de 9's
        if sec_actual:
            sec_nueves[len(sec_actual) > 2].append(sec_actual)

        for j in powerset(sec_nueves[0]):
            yield j + tuple(sec_nueves[1])

    def alterar_bloques(set_bloques: tuple[list[int]]):
        # Setear el conjunto de posiciones que vamos a quitar definitivamente
        # para después quitarlo.

        linker = lambda rmv, sms = "": sorted(sum(rmv, ())) + [sms]

        for set_dos in powerset(tuple(b) for b in set_bloques if len(b) > 2):
            # No ocupamos todos los bloques > 2 porque pueden ser ocupados para
            # dejar uno o ninguno.
            no_trvls = {tuple(b) for b in set_bloques
                                 if len(b) > 1 and b not in set_dos}

            for set_ninguno, set_uno in ([no_trvls - set(s), s] # Particiones
                                         for s in powerset(no_trvls)):
                # Aquí es donde se tiene que comenzar a retornar
                # todas las alteraciones.
            
                # Quitar los que no dejan ningun nueve
                variacion = set_ninguno.union(tuple(b) for b in set_bloques
                                                if len(b) == 1)

                # Controlamos el lado de los que dejan uno
                if set_uno:
                    # Aquí pantallamos, y pedimos la respuesta para rectificar
                    # las posiciones de los que dejan uno.
                    izq = yield linker(
                                    chain(
                                        variacion,
                                        (b[1:] for b in set_uno),
                                        (B[2:] for B in set_dos)
                                        ),
                                    (b[1] for b in set_uno)
                                    )

                    variacion.update(b[1:] if izq[b[1]] < 10 else b[:-1]
                                     for b in set_uno)
                    del izq

                # Variar las posiciones de los que dejan dos:
                for items in product(*(b[:-1] for b in set_dos)):
                    # La forma en la que funciona este bucle es el siguiente:
                    # 1) Tomo una tupla con un elemento de cada bloque.
                    # 2) Creo una nueva coleccion de tuplas donde cada tupla es
                    #    una copia de alguno de set_dos sin el elemento que
                    #    tomé en 1) ni el siguiente a él.
                    if not set_dos: continue # *() como argumento devuelve algo

                    alt = chain( # Alteración en los bloques de dos
                                variacion,
                                (tuple(i for i in b
                                         if not (i in items or i - 1 in items))
                                for b in set_dos)
                                )

                    yield linker(alt)

                if not set_dos: # En caso que no halla para variar posiciones:
                    yield linker(variacion)

                yield ["out"]

    for set_blqs in all_combinations():
        g = alterar_bloques(set_blqs)
        for nves in g:
            s_suitor = tuple(
                                fri_s[j] for j in range(len(fri_s))
                                if j not in nves
                            )
            if not is_seed_t1l9(s_suitor, paridad):
                a_suitor = list(next(T1l9(s_suitor, paridad)))

                if nves and type(nves[-1]) != str: # Indicativo para rectificar
                    nves = g.send({
                                    i: a_suitor[i - len([n for n in nves[:-1]
                                                           if n < i])]
                                    for i in nves[-1]
                                })

                # Colocamos los nueves que fueron removidos
                while nves and nves[-1] != "out":
                    for i in nves[:-1]: a_suitor.insert(i, 9)
                    yield tuple(a_suitor)
                    nves = next(g)

# for i in T1ln9((4,1,2,17,7,14,18,18,9,13,7,7,18,6,17,6,18), 1): # T1l9 lanza error, averiguar qué onda
#     print(i) # Debería retornar (3,10,10,18,3,7,9,9,4,16,13,3,9,3,8,13,8)

# Averiguar qué pasa aquí
# for i in T1ln9((4,1,0,2,17,9,9,9,9,7,14,18,18,9,9,13,7,9,9,7,18,6,17,6,18), 1):
    # print(i == (3,10,9,10,18,9,9,9,9,3,7,9,9,4,9,16,13,9,9,3,9,3,8,13,8))

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