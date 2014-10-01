#!/usr/bin/python
# coding=utf-8
import unittest
from heapq import heappop, heappush

class Grafo:

    def __init__(self, cantidad_vertices=0, pesos=[]):
        self.cantidad_aristas = 0
        self.cantidad_vertices = 0
        self.node_data = []
        self.vertices = []
        for i in xrange(cantidad_vertices):
            self.add_node()
        for peso in pesos:
            if peso[2] < 0:
                raise Exception('Una arista no puede tener peso negativo.')
            self.connect(peso[0], peso[1], peso[2])
        self.distancia = {}
        self.padre = {}

    def get_grado_salida(self, u):
        return len(self.vertices[u])

    def add_node(self, node_data=None):
        self.cantidad_vertices += 1
        self.vertices.append({})
        self.node_data.append(node_data)
        return self.cantidad_vertices - 1

    def get_node_data(self, u):
        return self.node_data[u]

    def connect(self, u, v, peso=1, both=False):
        self.vertices[u][v] = peso
        if both:
          self.vertices[v][u] = peso
        self.cantidad_aristas += 1

    def ady(self, v):
        return self.vertices[v]

    def calcular_camino_minimo(self, vertice):
        distancia = [None] * self.cantidad_vertices
        padre = [[]] * self.cantidad_vertices
        visitado = [False] * self.cantidad_vertices
        distancia[vertice] = 0
        heap = []
        heappush(heap, (distancia[vertice], vertice))
        cantidad_visitados = 0
        while heap:
            (_, v) = heappop(heap)
            visitado[v] = True
            cantidad_visitados += 1
            for w, peso in self.ady(v).iteritems():
                if visitado[w]:
                    continue
                if ( distancia[w] is None or 
                        distancia[v] + peso < distancia[w] ):
                    distancia[w] = distancia[v] + peso
                    heappush(heap,
                            (distancia[w], w))
                    padre[w] = [ v ]
                elif (distancia[v] + peso == distancia[w]):
                    heappush(heap,
                            (distancia[w], w))
                    padre[w].append(v)

            if cantidad_visitados == self.cantidad_vertices:
                break

        self.distancia[vertice] = distancia
        self.padre[vertice] = padre

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
                recorrido.insert(0, w[0])
                w = self.padre[u][w[0]]
            return recorrido
        if intentar_al_reves:
            return reversed(
                    self.get_recorrido(v, u, intentar_al_reves=False))
        raise Exception('Debe calcular previamente el camino mínimo.')

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


if __name__ == '__main__':
    unittest.main()
