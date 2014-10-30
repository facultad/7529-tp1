#!/usr/bin/python
# coding=utf-8
from lista_ordenada import ListaOrdenada

class CaminoInexistente(Exception):

    def __init__(self, u, v, *args, **kwargs):

        super(CaminoInexistente, self).__init__(
                'Camino inexistente de %s a %s.' % (u, v),
                *args, **kwargs)

class Grafo:

    def __init__(self):
        """
        O(1) 
        """
        self.cantidad_aristas = 0
        self.cantidad_vertices = 0
        self.node_data = []
        self.pesos = []
        self.cantidad_caminos_minimos = []
        self.recorridos = []
        self.lista_ady = []
        self.influencias = []
        self.distancia = {}
        self.padre = {}

    def get_grado_salida(self, u):
        """
        O(1)
        Obtiene el grado de salida de u.
        """
        return len(self.pesos[u])

    def add_node(self, node_data=None):
        """
        Complejidad: O(1)
        """
        self.cantidad_vertices += 1
        self.pesos.append({})
        self.node_data.append(node_data)
        self.lista_ady.append(ListaOrdenada())
        self.cantidad_caminos_minimos.append(
            [0 for i in xrange(self.cantidad_vertices - 1)])
        self.recorridos.append(
            [None for i in xrange(self.cantidad_vertices - 1)])
        for i in self.iternodes():
            self.cantidad_caminos_minimos[i].append(0)
            self.recorridos[i].append(None)
        self.influencias.append(0)
            
        return self.cantidad_vertices - 1

    def get_node_data(self, u):
        """
        Complejidad: O(1)
        """
        return self.node_data[u]

    def connect(self, u, v, peso=1, both=False):
        """
        O(log(Au)) si no se conecta a ambos.
        O(max(log(Au),log(Av))) si se conecta a ambos.
        """
        self.pesos[u][v] = peso
        # O(log(|V|))
        self.lista_ady[u].insert(v)
        if both:
            self.pesos[v][u] = peso
            # O(log(|V|))
            self.lista_ady[v].insert(u)
        self.cantidad_aristas += 1

    def ady(self, v):
        return self.pesos[v]

    def verificar_existe_camino(self, u, v):
        """
        O(1)
        """
        self.get_distancia(u,v)

    def get_distancia(self, u, v, intentar_al_reves=True):
        """
        Se obtiene la distancia.
        Previamente se debe haber llamado a calcular_camino_minimo(u)
        o calcular_camino_minimo(v).
        """
        if u in self.distancia:
            distancia = self.distancia[u][v]
            if distancia is None:
                raise CaminoInexistente(u,v)
            return distancia
        if intentar_al_reves:
            return self.get_distancia(v, u, intentar_al_reves=False)
        raise Exception('Debe calcular previamente el camino mínimo.')

    def get_recorrido(self, u, v, intentar_al_reves=True):
        """
        Se obtiene uno de los posibles recorridos.
        Previamente se debe haber llamado a calcular_camino_minimo(u)
        o calcular_camino_minimo(v).
        """
        if u in self.padre:
            w = [v]
            recorrido = []
            while len(w) > 0:
                recorrido.insert(0, iter(w).next())
                w = self.padre[u][iter(w).next()]
            return recorrido
        if intentar_al_reves:
            return reversed(
                    self.get_recorrido(v, u, intentar_al_reves=False))
        raise Exception('Debe calcular previamente el camino mínimo.')

    def get_recorridos(self, u, v):
        if u==v:
          return [[u]]
        if u in self.padre:
            if self.recorridos[u][v] is None:
                self.recorridos[u][v] = []
                for w in self.padre[u][v]:
                    for recorrido in self.get_recorridos(u,w):
                        self.recorridos[u][v].append(recorrido+[v])
            return self.recorridos[u][v]
        raise Exception('Debe calcular previamente el camino mínimo.')

    def conectados(self, u, v):
        """
        O(log(|V|))
        Verifica si u y v están conectados.
        """
        # O(log(n))
        return self.lista_ady[u].has(v)

    def conexiones_en_comun(self, u, v):
        """
        Au: Cantidad de aristas que salen de u.
        Av: Cantidad de aristas que salen de v.
        O(Au+Av)
        """
        return self.lista_ady[u].intersection(
                self.lista_ady[v])

    def iternodes(self):
        return xrange(self.cantidad_vertices)

    def get_influencia(self, u):
        """
        O(1)
        """
        return self.influencias[u]

    def calcular_caminos_minimos(self):
        """
        O(|V|*(|E|+|V|)
        """
        # |V|
        for i in self.iternodes():
            # O(|V|+|E|)
            self.calcular_camino_minimo(i)

    def get_recorrido_anchura_caminos_minimos(self, u, v):
        """
        Obtiene el recorrido en anchura por caminos mínimos 
        desde u hasta v.
        O(|E|+|V|)
        Está claro que por cada vertice que no hayamos visitado
        intentamos acceder a sus padres para el camino minimo
        buscado, con lo cual iteraremos como máximo sobre todos
        los vertices y sobre todas las aristas.
        """
        # Se verifica que exista un camino de u a v
        self.verificar_existe_camino(u,v)

        visitado = [False for i in self.iternodes()]
        q = [v]
        recorrido = []
        while len(q)>0:
            w = q.pop(0)
            if visitado[w]:
                continue
            visitado[w] = True
            recorrido.insert(0,w)
            for padre in self.padre[u][w]:
                q.append(padre)
        return recorrido

    def get_cantidad_caminos_minimos(self, u, v, intentar_al_reves=True):
        """
        O(1) mejor caso si hubo preprocesamiento.
        O(|V|+|E|) en caso que no haya habido preprocesamiento.
        Se obtiene la cantidad de recorridos de u a v.
        Previamente se debe haber llamado a calcular_camino_minimo(u)
        o calcular_camino_minimo(v).
        """
        if self.cantidad_caminos_minimos[u][v] <> 0:
            return self.cantidad_caminos_minimos[u][v]

        try:
            recorrido = self.get_recorrido_anchura_caminos_minimos(u,v)
        except CaminoInexistente:
            return 0

        # O(|V|+|E|): Idem explicación get_recorrido_anchura_caminos_minimos
        for w in recorrido:
            if self.cantidad_caminos_minimos[u][w] <> 0:
                continue
            if w==u:
                self.cantidad_caminos_minimos[u][w] = 1
            else:
                for padre in self.padre[u][w]:
                    self.cantidad_caminos_minimos[u][w] += (
                        self.cantidad_caminos_minimos[u][padre] )
        return self.cantidad_caminos_minimos[u][v]

    def get_cantidad_caminos_minimos_con_intermediario(self, u, w, v):
        """
        O(1) mejor caso si hubo preprocesamiento.
        O(|V|+|E|) en caso que no haya habido preprocesamiento.
        Se obtiene la cantidad de caminos mínimos entre u y v que
        pasan por w.
        """
        try:
            if (self.get_distancia(u,w) + self.get_distancia(w,v) 
                ) > self.get_distancia(u,v):
                return 0
            return ( self.get_cantidad_caminos_minimos(u,w) *
                self.get_cantidad_caminos_minimos(w,v))
        except CaminoInexistente:
            return 0


