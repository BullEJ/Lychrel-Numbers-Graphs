# E.L.: Explicación línea.

from itertools import product, pairwise, combinations
from shutil import copy, move
from os.path import join, exists
from os import remove
from functools import reduce
from more_itertools import powerset

##########                       Para main.py                        ##########
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

##########                       Para ramas.py                       ##########
    # Extras
def blq(t: tuple, i: int, c_pos = True):
    try:
        if c_pos and 0 > i: raise IndexError
        return t[i]
    except IndexError: return 0

    # Condicionadores de existencia
def is_seed_t1l9(fri_s, paridad): # Adaptable al caso (9 -> 0).
    # Supondré que no eres un perkin y el primer digito es mayor a 0.
    c = reduce(   # Esto se tiene que pasar a generador para que valga la pena.
            lambda c, i: c + ((blq(c, -2, False) + i) % 2, ),
            fri_s[:-1], tuple())
    for i, s in enumerate(fri_s[1:-1], 1):                               # (M2)
        if ((s == 0  and blq(c, i - 1) == 0 and c[i] == 1) or
            (s == 18 and blq(c, i - 1) == 1 and c[i] == 0)):
            return True

    if ((paridad and (fri_s[-1] - 2 * blq(c, -2, False)) % 4) or         # (M3)
        (not paridad and (fri_s[-1]
                          + blq(c, -1, False)
                          + blq(c, -2, False)) % 2)):
        return True
    return False


def is_seed_t1ln9(fri_s, paridad):
    pass

def is_seed_t2l9(fri_s, paridad):
    pass

def is_seed_t2ln9(fri_s, paridad):
    pass

def is_seed(fri_s: tuple[int]) -> bool:
    return (is_seed_t1l9(fri_s) or is_seed_t1ln9(fri_s) or
            is_seed_t2l9(fri_s) or is_seed_t2ln9(fri_s))

    ##########         Algoritmos para obtener antecesores         ##########
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

def T1ln9(fri_s: tuple[int], paridad: int):
    ##########                    Funcionamiento                     ##########
    # 1) Obtengo los bloques de nueves.
    # 2) A cada bloque le asigno un numero entre el 0 y su tamaño.
    #    Este numero representa la cantidad de nueves que le quitaremos al
    #    bloque, donde supondremos que esa es la cantidad de nueves inoportunos
    #    en el bloque.
    # 3) Pantallamos, obteniendo a la vez, el T1l9 del modificado.
    # 4) Devolvemos todas las variaciones de las posibles posiciones donde se
    #    le puede colocar los nueves inoportunos al T1l9 del modificado.

    ##########             Obtener los bloques de nueves             ##########
    # Extraer posiciones nueves.
    sec_nvs, sec_actual = [], []
    
    # Iteramos sobre la fri_s
    for indice, num in enumerate(fri_s[1:-1], 1):
        if num == 9: sec_actual.append(indice)
        elif sec_actual: 
            sec_nvs.append(sec_actual)
            sec_actual = [] 
    
    # Si al final de la iteración aún hay una secuencia de 9's
    if sec_actual:
        sec_nvs.append(sec_actual)

    del sec_actual # Que se joda. Me molesta que exista.

    ##########              Gestión de las alteraciones              ##########
    for conf_scrs in product(                                                   # conf_scrs es una tupla que indica cuantos nueves se
                                *(range(len(blq) + 1) for blq in sec_nvs)       # suponen que son inoportunos dentro de cada bloque.
                            ):                                                  # scrs : screenshot (pantallazo).
        # Eliminamos la cantidad de nueves que se dictan en cada bloque.
        s_mod = tuple(
                    j for i, j in enumerate(fri_s)
                      if i not in sum(
                                        sec_nvs[b][r:]
                                        for b, r in enumerate(conf_scrs), []
                                    )
                    )
        
        # Pantallamos para ver si la configuración vale la pena.
        if is_seed_t1l9(s_mod, paridad): continue

        # Obtenemos las posiciones donde podemos colocar nueves inoportunos.
        a_mod = list(next(T1l9(s_mod, paridad)))

        cuadre = lambda i, p: sec_nvs[i][p] - sum(conf_scrs[:i - p]) # Pendiente, aquí puede que ocurra un error cuando se eliminan colas
        p_dispo = tuple(                                                        # En esta variable se busca obtener las posiciones donde
                        tuple(                                                  # se puede colocar nueves inoportunos por bloque en T1l9.
                              cuadre(i, 0) - 1 + j                              # Explicación: Tengo len(conf_scrs) bloques, pero de
                              for j, (l, r) in enumerate(pairwise(              # ellos me interesan solo los que les remuevo algo.
                                  a_mod[cuadre(i, 0) - 1 : cuadre(i, -1) + 2]   # Por cada bloque, evaluo su correspondiente en el T1l9
                                ), 1) if {l // 10, r // 10} == {0, 1}           # del modificado. Si una pareja está formada por uno que
                            ) + (conf_scrs[i],)                                 # acarrea y otro que no, considero la posición que coloca
                        for i in range(len(conf_scrs)) if conf_scrs[i]          # el nueve en medio de ellos.
                        )
        # Variamos
        for b, distr in enumerate(
                            product(
                                *(MS(len(blk) - 1, blk[-1]) for blk in p_dispo)
                            )):
            a_mod_variado = a_mod.copy()
            for i, n in enumerate(distr):
                for _ in range(n): a_mod_variado.insert(
                                                        p_dispo[b]       +
                                                        sum(distr[:i])   +
                                                        sum(
                                                            k[-1]
                                                            for k in p_dispo[:b]
                                                            ),
                                                        9
                                                    )

            yield a_mod_variado


# for i in T1ln9((7,1,0,2,17,9,9,9,9,7,14,18,18,9,9,13,7,9,9,7,18,6,17,6,18), 1):
#     print(i) #== (3,10,9,10,18,9,9,9,9,3,7,9,9,4,9,16,13,9,9,3,9,3,8,13,8))

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

    ##########                      Miscelaneos                      ##########
def falta_completar(nodos) -> tuple[tuple]:
    return tuple(filter(                                                        # Retorna los FRI que no son semilla.
                    lambda nodo: not is_seed(nodo),                             # Se espera que nodos sea un generador.
                    nodos))                                                     #

def MS(largo: int, suma: int):                                                  # MS : Maneras de sumar
    if largo == 1:                                                              # Obtiene todas las maneras de sumar "suma" en una tupla
        yield (suma,)                                                           # de "largo" números.
    else:                                                                       # Explicación: Recursivamente, cada manera se puede
        for r in range(suma + 1):                                               # expresar como una tupla de largo "largo" - 1,
            for t in MS(largo - 1, r):                                          # añadiendole al final, lo que le falta para dar "suma".
                yield t + (suma - r, )                                          # Observar que MS es inyectiva en la segunda variable.