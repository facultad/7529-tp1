#!/usr/bin/python
# coding=utf-8

from grafo import Grafo
from heapq import heappop, heappush

class GrafoPesado(Grafo):

    def __init__(self, cantidad_vertices=0, pesos=[], *args, **kwargs):
        """
        O(1) si los valores de los parámetros son los definidos 
        por defecto.
        O(|E|*log(|V|))
        """
        Grafo.__init__(self, *args, **kwargs)
        for i in xrange(cantidad_vertices):
            self.add_node()
        for peso in pesos:
            if peso[2] < 0:
                raise Exception('Una arista no puede tener peso negativo.')
            # O(log(|V|))
            self.connect(peso[0], peso[1], peso[2])

    def calcular_camino_minimo(self, vertice):
        """
        O(|E|*log(|V|))
        """
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

    def calcular_influencias(self):
        # O(n)
        self.influencias = [0 for w in self.iternodes()]


        # Preprocesamiento de cantidad de caminos mínimos
        # O((|V|**2)*(|V|+|E|))
        for u in self.iternodes():  # |V|
            for v in self.iternodes():  # |V|
                cantidad_u_v = self.get_cantidad_caminos_minimos(u,v) # O(|V|+|E|)

        # O(|V|**3)
        for u in self.iternodes():  # |V|
            for v in self.iternodes():  # |V|
                if u>=v:
                    continue
                # O(1) c/preprocesamiento
                cantidad_u_v = self.get_cantidad_caminos_minimos(u,v)
                if cantidad_u_v == 0:
                    continue
                for w in self.iternodes(): # |V|
                    if w==u or w==v:
                        continue
                    influencias[w] += float(
                                # O(1) (c/preprocesamiento)
                                self.get_cantidad_caminos_minimos_con_intermediario(u,w,v)
                                ) / cantidad_u_v
        return self.influencias

    def calcular_caminos_minimos(self):
        """
        O(|V|*(|E|+|V|)
        """
        # |V|
        for i in self.iternodes():
            # O(|V|+|E|)
            self.calcular_camino_minimo(i)

