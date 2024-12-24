# Entendemos target ln al objeto de abstracción n
# donde la abstracción n consiste en la clase de equivalencia n veces
# definido de manera recursiva, donde dos target l(n-1) son equivalentes
# como target ln si su sucesores coinciden en l(n-1)

from itertools import product, combinations, permutations, takewhile
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
    # Condicionadores de existencia
def blq(t: tuple, i: int, c_pos = True): # c_pos = condición de positividad
    try:
        if c_pos and 0 > i: raise IndexError
        return t[i]
    except IndexError: return 0

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
    C  = [0] + reduce(
                lambda c, i: c + ((blq(c, -2, False) + i) % 2, ),
                fri_s[:-1], tuple())
    MC = (blq(C, i-1) + blq(C, i+1) for i in range(len(C)))
    MC = MC[:-1] + tuple(MC[-1] + blq(C, -1 - paridad, False))
    
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

        for r in range(len(sec_nueves[0]) + 1):
            for j in combinations(sec_nueves[0], r):
                yield j + tuple(sec_nueves[1])

    def alterar_bloques(set_bloques): # Optimizar código, no lógica
        # Setear el conjunto de posiciones que vamos a quitar definitivamente
        # y luego quitarlo.
        quitados    = set(b for b in set_bloques if len(b) == 1)
        quitados_nt = set(set_bloques) - quitados
        blqs3       = set(b for b in quitados_nt if len(b) > 2)

        formateo = lambda rmv: [
                                tuple(
                                    fri_s[j] for j in range(len(fri_s))
                                    if j not in set(sum(rmv, ()))),
                                sorted(sum(rmv, ()))
                                ]

        if not quitados_nt:
            yield formateo(quitados)

        elif len(quitados_nt) == 1:
            # Quitarlo por completo (ninguno)
            yield formateo(set_bloques)
            # Variar si tiene tamaño mayor a 2
            pass
            # Dejarle uno (uno)
            # FALTA VER QUE HACER--------------------------------------------------
            yield formateo(set_bloques[:-1] + set_bloques[-1][1:])
            izq = yield

        elif blqs3:
            for set_dos in powerset(blqs3):
                particiones = ([set(s), quitados_nt - set_dos - set(s)]
                                for s in powerset(quitados_nt - set(set_dos)))
                var_set_d =  (ti for ti in product(*(b[:-1] for b in set_dos)))

                for set_ninguno, set_uno in particiones:
                    # Quitar los que no dejan ningun nueve
                    variacion = quitados.union(set_ninguno)

                    # Variar las posiciones de los que dejan dos
                    for items in var_set_d:
                        variacion.add((i for i in b if i not in items and i + 1 not in items) for b in set_dos)

                        # Controlamos el lado de los que dejan uno
                        yield formateo(variacion.union({(b[1:],) for b in set_uno})) # Pantallamos (dejamos el de más a la izq)
                        izq : dict[tuple: int] = yield # Esperamos para rectificar
                            # Rectificamos
                        yield sorted(sum(variacion.union({tuple(b[1:] if izq[b[1:]] < 10 else b[:-1]) for b in set_uno}), ()))

        else:
            pass
            # yield formateo(sorted(sum(
            #         quitados,
            #         ())))

    def there_is_singlenine(ant, pos) -> dict[tuple: int]:
        # Separo bloques de nueves unicos
        sec_unueves = dict()
        sec_uactual = []
        nivelador   = 0
        
            # Iteramos sobre la fri_s
        for indice, num in enumerate(ant[1:-1], 1):
            nivelador = indice + len([pos_rmv for pos_rmv in pos if pos_rmv < nivelador])
            if num == 9:
                sec_uactual.append(nivelador)
            elif len(sec_uactual) == 1:
                bloque = tuple(takewhile(lambda i: i in pos, range(sec_uactual[0] + 1, sec_uactual[0] + 1 +  len(pos))))
                sec_unueves[bloque] = sec_uactual[0] - 1
                sec_uactual = [] 
        
            # Si al final de la iteración aún hay una secuencia de 9's
        if len(sec_uactual) == 1:
            bloque = tuple(takewhile(lambda i: i in pos, range(sec_uactual[0] + 1, sec_uactual[0] + 1 +  len(pos))))
            sec_unueves[bloque] = sec_uactual

        return sec_unueves

    for set_blqs in all_combinations():
        g = alterar_bloques(set_blqs)
        for s_candidato, pos_nves in g:
            if not is_seed_t1l9(s_candidato, paridad):
                a_candidato = list(next(T1l9(s_candidato, paridad)))

                rectificador = there_is_singlenine(a_candidato)
                if rectificador:
                    g.next() # Esto es necesario para pasar a la linea donde se asigna valor
                    pos_nves = g.send(rectificador)

                # Colocamos los nueves que fueron removidos
                yield tuple(a_candidato.insert(i, 9) for i in pos_nves)

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