import pickle
from itertools import permutations as perm
from sys import getsizeof
from ramas import Rama
from utilities import guardar

# Este programa debe tener la capacidad de:
# 1. Catalogar los distintos grafos
# 2. Indicar el progreso de la operación
# 3. Permitir guardar el progreso cuando se sale del programa mientras el
#    programa está corriendo.
# Después, se pedirá correrlo al inicio y que deje de funcionar cuando se    |
# apague.

#--- 1. Catalogar los distintos grafos ---
SEED   = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    # Carga de datos
with open("clases.pkl", "rb") as data:
    CLASES = pickle.load(data)
with open("punto_de_reinicio.pkl", "rb") as data:
    reset = pickle.load(data)

    # Comienzo de proceso
recoleccion = {graph: [] for graph in CLASES}
try:
    for c, s_fri in enumerate(perm(SEED)):
        # Reinicio
        if c < reset: continue
        reset = c

        rama = Rama(s_fri[ s_fri[0]==0 :])
        if rama in CLASES:
        	recoleccion[rama].append(rama.fri)
            if getsizeof(recoleccion[rama]) >= 10**6:
                fri_cls = next(filter(
                                lambda clss: clss == rama,
                                CLASES # Quiero obtener el fri representativo
                                )).fri # de la clase
                print("Se han almacenados suficientes elementos de una clase.")
                guardar(recoleccion[rama], fri_cls) # Limpiamos paquetes de
                recoleccion[rama] = []              # más de 1MB pues no sé
                                                    # cuantas clases hay.
        else:
            CLASES.add(rama)
            recoleccion[rama] = []

#--- 2. Indicar el progreso de la operación ---
        print(f"{c/3628800}%", end="\r") # 36... = 10!

#--- 3. Permitir guardar el progreso ---
except KeyboardInterrupt: # Dectectamos CTR-C
    print(f"Quedamos en un {reset/3628800}%, guardamos los grafos...")
    with open("clases.pkl", "wb") as data:
        pickle.dump(CLASES, data)

    print("Guardamos los residuos de la recoleccion...")
    for clase in CLASES:
        guardar(recoleccion[clase], clase.fri)

    print("Guardamos punto de reinicio...")
    with open("punto_de_reinicio.pkl", "wb") as data:
        pickle.dump(reset, data)

    print("Listo, nos vemos.")