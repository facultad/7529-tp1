#!/usr/bin/python
# coding=utf-8
import unittest
from heapq import heappop, heappush
from lista_ady import ListaAdy

class Grafo:

    def __init__(self, cantidad_vertices=0, pesos=[]):
        self.cantidad_aristas = 0
        self.cantidad_vertices = 0
        self.node_data = []
        self.pesos = []
        self.cantidad_caminos_minimos = []
        self.recorridos = []
        self.lista_ady = []
        for i in xrange(cantidad_vertices):
            self.add_node()
        for peso in pesos:
            if peso[2] < 0:
                raise Exception('Una arista no puede tener peso negativo.')
            self.connect(peso[0], peso[1], peso[2])
        self.distancia = {}
        self.padre = {}

    def get_grado_salida(self, u):
        """
        Complejidad: O(1)
        """
        return len(self.pesos[u])

    def add_node(self, node_data=None):
        """
        Complejidad: O(1)
        """
        self.cantidad_vertices += 1
        self.pesos.append({})
        self.node_data.append(node_data)
        self.lista_ady.append(ListaAdy())
        self.cantidad_caminos_minimos.append(
            [0 for i in xrange(self.cantidad_vertices - 1)])
        self.recorridos.append(
            [None for i in xrange(self.cantidad_vertices - 1)])
        for i in self.iternodes():
            self.cantidad_caminos_minimos[i].append(0)
            self.recorridos[i].append(None)
            
        return self.cantidad_vertices - 1

    def get_node_data(self, u):
        """
        Complejidad: O(1)
        """
        return self.node_data[u]

    def connect(self, u, v, peso=1, both=False):
        """
        O(log(n))
        """
        self.pesos[u][v] = peso
        # O(log(n))
        self.lista_ady[u].insert((v,peso))
        if both:
            self.pesos[v][u] = peso
            # O(log(n))
            self.lista_ady[v].insert((u,peso))
        self.cantidad_aristas += 1

    def ady(self, v):
        return self.pesos[v]

    def calcular_camino_minimo(self, vertice):
        distancia = [None] * self.cantidad_vertices
        padre = [set() for i in self.iternodes()]
        visitado = [False] * self.cantidad_vertices
        distancia[vertice] = 0
        heap = []
        heappush(heap, (distancia[vertice], vertice))
        while heap:
            (_, v) = heappop(heap)
            visitado[v] = True
            for w, peso in self.ady(v).iteritems():
                if visitado[w]:
                    continue
                if ( distancia[w] is None or 
                        distancia[v] + peso < distancia[w] ):
                    distancia[w] = distancia[v] + peso
                    heappush(heap,
                            (distancia[w], w))
                    padre[w] =set([ v ])
                elif (distancia[v] + peso == distancia[w]):
                    heappush(heap,
                            (distancia[w], w))
                    padre[w].add(v)

        self.distancia[vertice] = distancia
        self.padre[vertice] = padre

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
        Se obtiene la cantidad de recorridos de u a v.
        Previamente se debe haber llamado a calcular_camino_minimo(u)
        o calcular_camino_minimo(v).
        O(|V|+|E|)
        """
        # O(|V|+|E|)
        recorrido = self.get_recorrido_anchura_caminos_minimos(u,v)

        # O(|V|+|E|): Idem explicación get_recorrido_anchura_caminos_minimos
        for w in recorrido: # O(|V|)
            if self.cantidad_caminos_minimos[u][w] <> 0:
                continue
            if w==u:
                self.cantidad_caminos_minimos[u][w] = 1
            else:
                for padre in self.padre[u][w]: #(|V|)
                    self.cantidad_caminos_minimos[u][w] += (
                        self.cantidad_caminos_minimos[u][padre] )
        return self.cantidad_caminos_minimos[u][v]

        if u==v:
          return 1
        if u in self.padre:
            if self.cantidad_caminos_minimos[u][v] is None:
                self.cantidad_caminos_minimos[u][v] = 0
                for w in self.padre[u][v]:
                    self.cantidad_caminos_minimos[u][v] += self.get_cantidad_caminos_minimos(u,w)
            return self.cantidad_caminos_minimos[u][v]
        if intentar_al_reves:
            return self.get_cantidad_caminos_minimos(v, u, intentar_al_reves=False)
        raise Exception('Debe calcular previamente el camino mínimo.')

    def get_cantidad_caminos_minimos_con_intermediario(self, u, w, v):
        if (self.get_distancia(u,w) + self.get_distancia(w,v) 
            ) > self.get_distancia(u,v):
            return 0
        return ( self.get_cantidad_caminos_minimos(u,w) *
            self.get_cantidad_caminos_minimos(w,v))

    def get_distancia(self, u, v, intentar_al_reves=True):
        """
        Se obtiene la distancia.
        Previamente se debe haber llamado a calcular_camino_minimo(u)
        o calcular_camino_minimo(v).
        """
        if u in self.distancia:
            return self.distancia[u][v]
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
        self.lista_ady[u].has(v)

    def conexiones_en_comun(self, u, v):
        """
        O(|V|)
        """
        return self.lista_ady[u].intersection(
                self.lista_ady[v])

    def iternodes(self):
        return xrange(self.cantidad_vertices)


class DijkstraTestCase(unittest.TestCase):

    def test_camino_minimo(self):

        grafo = Grafo(cantidad_vertices=7, pesos=[
            (0,1,5),
            (0,2,3),
            (1,2,2),
            (1,4,3),
            (1,6,1),
            (2,3,7),
            (2,4,7),
            (3,0,2),
            (3,5,6),
            (4,3,2),
            (4,5,1),
            (6,4,1),
            ])
        grafo.calcular_camino_minimo(0)
        self.assertEqual(grafo.get_distancia(0,0), 0)
        self.assertEqual(grafo.get_distancia(0,1), 5)
        self.assertEqual(grafo.get_distancia(0,2), 3)
        self.assertEqual(grafo.get_distancia(0,3), 9)
        self.assertEqual(grafo.get_distancia(0,4), 7)
        self.assertEqual(grafo.get_distancia(0,5), 8)
        self.assertEqual(grafo.get_distancia(0,6), 6)

        self.assertEqual(
                [0,1,6,4,5],
                grafo.get_recorrido(0,5))

    def test_cantidad_caminos_minimos(self):

        grafo = Grafo()

        for i in xrange(14):
            grafo.add_node()

        grafo.connect(0,1,both=True)
        grafo.connect(0,2,both=True)
        grafo.connect(1,3,both=True)
        grafo.connect(1,4,both=True)
        grafo.connect(2,5,both=True)
        grafo.connect(2,6,both=True)
        grafo.connect(2,7,both=True)
        grafo.connect(3,8,both=True)
        grafo.connect(4,8,both=True)
        grafo.connect(5,9,both=True)
        grafo.connect(6,9,both=True)
        grafo.connect(7,9,both=True)
        grafo.connect(8,10,both=True)
        grafo.connect(9,10,both=True)
        grafo.connect(10,11,both=True)
        grafo.connect(10,12,both=True)
        grafo.connect(11,13,both=True)
        grafo.connect(12,13,both=True)

        for i in grafo.iternodes():
            grafo.calcular_camino_minimo(i)

        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(2,10),3)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(0,10),5)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(0,13),10)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(4,5),2)

    def test_cantidad_caminos_minimos_con_intermediario(self):
 
        grafo = Grafo()

        for i in xrange(14):
            grafo.add_node()

        grafo.connect(0,1,both=True)
        grafo.connect(0,2,both=True)
        grafo.connect(1,3,both=True)
        grafo.connect(1,4,both=True)
        grafo.connect(2,5,both=True)
        grafo.connect(2,6,both=True)
        grafo.connect(2,7,both=True)
        grafo.connect(3,8,both=True)
        grafo.connect(4,8,both=True)
        grafo.connect(5,9,both=True)
        grafo.connect(6,9,both=True)
        grafo.connect(7,9,both=True)
        grafo.connect(8,10,both=True)
        grafo.connect(9,10,both=True)
        grafo.connect(10,11,both=True)
        grafo.connect(10,12,both=True)
        grafo.connect(11,13,both=True)
        grafo.connect(12,13,both=True)

        for i in grafo.iternodes():
            grafo.calcular_camino_minimo(i)

        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(0,13,10),
            0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(0,10,13),
            10)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(0,1,8),
            2)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(2,5,11),
            1)
       
    def validar_recorrido(self, grafo, u, v, recorridos_esperados):
        recorridos = grafo.get_recorridos(u,v)
        self.assertEqual(len(recorridos), len(recorridos_esperados))
        for r in recorridos:
            self.assertIn(r, recorridos_esperados)

    def test_recorridos(self):
 
        grafo = Grafo()

        for i in xrange(14):
            grafo.add_node()

        grafo.connect(0,1,both=True)
        grafo.connect(0,2,both=True)
        grafo.connect(1,3,both=True)
        grafo.connect(1,4,both=True)
        grafo.connect(2,5,both=True)
        grafo.connect(2,6,both=True)
        grafo.connect(2,7,both=True)
        grafo.connect(3,8,both=True)
        grafo.connect(4,8,both=True)
        grafo.connect(5,9,both=True)
        grafo.connect(6,9,both=True)
        grafo.connect(7,9,both=True)
        grafo.connect(8,10,both=True)
        grafo.connect(9,10,both=True)
        grafo.connect(10,11,both=True)
        grafo.connect(10,12,both=True)
        grafo.connect(11,13,both=True)
        grafo.connect(12,13,both=True)

        for i in grafo.iternodes():
            grafo.calcular_camino_minimo(i)

        self.validar_recorrido(grafo,0,8,
            [[0,1,3,8],
              [0,1,4,8],
              ])
        self.validar_recorrido(grafo,0,10,
            [[0,1,3,8,10],
              [0,1,4,8,10],
              [0,2,5,9,10],
              [0,2,6,9,10],
              [0,2,7,9,10],
              ])
        self.validar_recorrido(grafo,7,3,
            [[7,2,0,1,3],
              [7,9,10,8,3],
              ])

    def verificar_recorrido_anchura(self, recorrido, esperado):
        recorrido_standarizado = []
        desde = 0
        for x in esperado:
            recorrido_standarizado.append(
                    set(recorrido[desde:desde+len(x)]))
            desde+=len(x)
        self.assertEqual(recorrido_standarizado, esperado)


    def test_recorrido_anchura_caminos_minimos(self):
 
        grafo = Grafo()

        for i in xrange(14):
            grafo.add_node()

        grafo.connect(0,1,both=True)
        grafo.connect(0,2,both=True)
        grafo.connect(1,3,both=True)
        grafo.connect(1,4,both=True)
        grafo.connect(2,5,both=True)
        grafo.connect(2,6,both=True)
        grafo.connect(2,7,both=True)
        grafo.connect(3,8,both=True)
        grafo.connect(4,8,both=True)
        grafo.connect(5,9,both=True)
        grafo.connect(6,9,both=True)
        grafo.connect(7,9,both=True)
        grafo.connect(8,10,both=True)
        grafo.connect(9,10,both=True)
        grafo.connect(10,11,both=True)
        grafo.connect(10,12,both=True)
        grafo.connect(11,13,both=True)
        grafo.connect(12,13,both=True)

        for i in grafo.iternodes():
            grafo.calcular_camino_minimo(i)

        self.verificar_recorrido_anchura(
                grafo.get_recorrido_anchura_caminos_minimos(0,13),
                [
                    set([0]),
                    set([1,2]),
                    set([3,4,5,6,7]),
                    set([8,9]),
                    set([10]),
                    set([11,12]),
                    set([13]),
                    ])
        




if __name__ == '__main__':
    unittest.main()
