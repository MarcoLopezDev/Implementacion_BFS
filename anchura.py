
from curses import noecho
from urllib.request import proxy_bypass
from grafos import Accion
from grafos import Estado
from grafos import Nodo
from grafos import Problema


# %%
def anchura(problema):
    raiz = crea_nodo_raiz(problema)
    if problema.es_objetivo(raiz.estado):
        return raiz
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = frontera.pop(0)
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estado_frontera = [nodo.estado for nodo in frontera]
            if(hijo.estado not in explorados and hijo.estado not in estado_frontera):
                if problema.es_objetivo(hijo.estado):
                    return hijo
                frontera.append(hijo)

# %%


def crea_nodo_raiz(problema):
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, None, acciones_raiz, None)
    return raiz

# %%


def crea_nodo_hijo(problema, padre, accion):
    nuevo_estado = problema.resultado(padre.estado, accion)
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    padre.hijos.append(hijo)
    return hijo

# %%


def muestra_solucion(objetivo=None):
    if not objetivo:
        print("No hay solucion")
        return
    nodo = objetivo
    while nodo:
        msg = "Estado: {0}"
        print(msg.format(nodo.estado.nombre))
        if nodo.accion:
            msg = "<--- {0} ---"
            print(msg.format(nodo.accion.nombre))
        nodo = nodo.padre


# %%%
if __name__ == '__main__':
    accN = Accion('N')
    accS = Accion('S')
    accE = Accion('E')
    accO = Accion('O')
    accNE = Accion('NE')
    accNO = Accion('NO')
    accSE = Accion('SE')
    accSO = Accion('SO')

    buenaVista = Estado('Buena Vista', [accE])
    montero = Estado('Montero', [accS, accO, accNE])
    sanJulian = Estado('San Julian', [accSO])
    warnes = Estado('Warnes', [accN, accS])
    santaCruz = Estado('Santa Cruz de la Sierra', [accN, accE, accSO])
    sanJose = Estado('San Jose', [accO, accSE])
    comarapa = Estado('Comarapa', [accE, accSE])
    samaipata = Estado('Samaipata', [accS, accE, accO])
    elTorno = Estado('El Torno', [accO, accNE])
    robore = Estado('Robore', [accNO])
    vallegrande = Estado('Vallegrande', [accN, accNO])

    viajes = {'Buena Vista': {'E': montero},
              'Montero': {'S': warnes,
                          'O': buenaVista,
                          'NE': sanJulian},
              'San Julian': {'SO': montero, },
              'Warnes': {'N': montero,
                         'S': santaCruz, },
              'Santa Cruz de la Sierra': {'N': warnes,
                                          'E': sanJose,
                                          'SO': elTorno},
              'San Jose': {'O': santaCruz,
                           'SE': robore, },
              'Comarapa': {'E': samaipata,
                           'SE': vallegrande, },
              'Samaipata': {'S': vallegrande,
                            'E': elTorno,
                            'O': comarapa},
              'El Torno': {'O': samaipata,
                           'NE': santaCruz, },
              'Robore': {'NO': sanJose},
              'Vallegrande': {'N': samaipata,
                              'NO': comarapa, }
              }
    objetivo_1 = [vallegrande]
    problema_1 = Problema(buenaVista, objetivo_1, viajes)
    problema_resolver = problema_1

    solucion = anchura(problema_resolver)
    muestra_solucion(solucion)

# %%
