#!/usr/bin/python
# coding=utf-8

from grafo import Grafo

class GrafoPesoUnitario(Grafo):

    def bfs(self, u):
        """
        O(|V|+|E|)
        Devuelve un listado comenzando poe la raiz (u) y terminando 
        por los vertices a mayor distancia de u.
        Es requisito que ya se hayan calculado los caminos mínimos
        para el vértice u
        """

        s=[]

        visitado = [False] * self.cantidad_vertices
        q = [u]

        while len(q)>0:
            w = q.pop(0)

            if visitado[w]:
                continue

            visitado[w] = True

            s.append(w)

            for a in self.ady(w):
                if ( self.distancia[u][w] + 1 == self.distancia[u][a] ):
                    q.append(a)
        return s

    def __acumular_influencias(self, u):
        # O(|V|+|E|)
        S = self.bfs(u)

        # O(|E|)
        # Se acumulan las influencias a partir del calculo de
        # dependencias del vertice u hacia el resto.
        dependencias = [0 for i in self.iternodes()]
        while len(S) > 0:
            w = S.pop()
            for v in self.padre[u][w]:
                dependencias[v] += (float(self.cantidad_caminos_minimos[u][v]) /
                        float(self.cantidad_caminos_minimos[u][w])) * (
                                1 + dependencias[w])
                if w <> u:
                    self.influencias[w] += dependencias[w]

    def calcular_influencias(self):
        """
        # O(|V|*(|V|+|E|))
        """
        for u in self.iternodes(): #|V|
            self.__acumular_influencias(u) # O(|V|+|E|)

    def calcular_camino_minimo(self, u):
        """
        Calcula las distancias de u al resto de los vertices.
        O(|E|+|V|)
        """

        distancia = [None] * self.cantidad_vertices
        padre = [set() for i in self.iternodes()]
        visitado = [False] * self.cantidad_vertices
        q = [u]
        distancia[u] = 0
        cantidad_caminos_minimos = [0] * self.cantidad_vertices
        cantidad_caminos_minimos[u] = 1

        while len(q)>0:
            w = q.pop(0)

            if visitado[w]:
                continue

            visitado[w] = True

            for adyacente in self.ady(w):

                if ( distancia[adyacente] is None or 
                        distancia[w] + 1 < distancia[adyacente] ):
                    q.append(adyacente)
                    distancia[adyacente] = distancia[w] + 1
                    padre[adyacente] = set([ w ])
                    cantidad_caminos_minimos[adyacente] = cantidad_caminos_minimos[w] 
                elif (distancia[w] + 1 == distancia[adyacente]):
                    padre[adyacente].add(w)
                    cantidad_caminos_minimos[adyacente] += cantidad_caminos_minimos[w] 

        self.distancia[u] = distancia
        self.padre[u] = padre
        self.cantidad_caminos_minimos[u] = cantidad_caminos_minimos

    def get_cantidad_caminos_minimos(self, u, v, intentar_al_reves=True):
        """
        O(1)
        """
        return self.cantidad_caminos_minimos[u][v]




