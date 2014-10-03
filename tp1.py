#!/usr/bin/python
# coding=utf-8
from grafo import Grafo
import re
from heapq import heappop, heappush

NODEDEF_TYPE = 1
EDGEDEF_TYPE = 2
re_nodedef = re.compile('^nodedef>.*')
re_edgedef = re.compile('^edgedef>.*')

class Node:

    def __init__(self, id, description):
        self.id = int(id)
        self.description = description

    @staticmethod
    def create_node_from_gdf_line(line):
        fields = line.split(',')
        return Node(id=fields[0], description=fields[1])


class TP1:

    def __init__(self, filepath):
        self.grafo = Grafo()
        self.vertice_from_id = {}
        linetype = None

        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if re_nodedef.match(line):
                    linetype = NODEDEF_TYPE
                elif re_edgedef.match(line):
                    linetype = EDGEDEF_TYPE
                elif linetype == NODEDEF_TYPE:
                    node = Node.create_node_from_gdf_line(line)
                    self.vertice_from_id[node.id] = self.grafo.add_node(node)
                elif linetype == EDGEDEF_TYPE:
                    id1, id2 = map(int, line.split(','))
                    self.grafo.connect(
                            self.vertice_from_id[id1],
                            self.vertice_from_id[id2], both=True)

    def get_popularidad(self):

        popularidad = []
        for i in xrange(self.grafo.cantidad_vertices):
            popularidad.append([])

        for u in self.grafo.iternodes():
            grado = self.grafo.get_grado_salida(u)
            popularidad[grado].append(self.grafo.get_node_data(u))

        return popularidad

    def get_influencias(self):
        """
        Con preprocesamiento previo de obtencion de cantidad de caminos
        minimos: O(n^3)
        """
        # O(n)
        influencias = [0 for w in self.grafo.iternodes()]

        # O(n^3)
        for u in self.grafo.iternodes():  # O(n)
            for v in self.grafo.iternodes():  # O(n)
                if u>=v:
                    continue
                # O(1) (c/preprocesamiento)
                cantidad_u_v = self.grafo.get_cantidad_caminos_minimos(u,v)
                for w in self.grafo.iternodes(): # O(n)
                    if w==u or w==v:
                        continue
                    influencias[w] += float(
                                # O(1) (c/preprocesamiento)
                                self.grafo.get_cantidad_caminos_minimos_con_intermediario(u,w,v)
                                ) / cantidad_u_v
        return influencias

    def calcular_caminos_minimos(self):
        for i in self.grafo.iternodes():
            self.grafo.calcular_camino_minimo(i)

    def get_vertice_from_id(self, id):
        return self.vertice_from_id[id]

    def recomendaciones_para(self, u):
        """
        O(|V|^2)
        Devuelve un heap con las recomendaciones. Solo se recomienda en 
        caso que exista algún amigo en común.
        """
        # O(|V|)
        recomendaciones = []
        for v in self.grafo.iternodes():
            if u==v:
                continue
            # O(log(|V|))
            if self.grafo.conectados(u,v):
                continue
            # O(|V|)
            cantidad_conexiones_en_comun = - len(
                    self.grafo.conexiones_en_comun(u,v))
            if cantidad_conexiones_en_comun == 0:
                continue
            # O(log(|V|))
            heappush(recomendaciones, (cantidad_conexiones_en_comun, v))
        return recomendaciones

    def recomendaciones(self):
        """
        O(|V|^3)
        Devuelve un listado donde cada item tiene:
        (vertice, recomendacion, amigos_en_comun)
        """
        recomendaciones = []
        for u in self.grafo.iternodes(): # O(|V|)
            recomendaciones_u = self.recomendaciones_para(u) # O(|V|^2)
            max_amigos_comun = None
            while len(recomendaciones_u) > 0:
                # O(1)
                amigos_comun, recomendacion = heappop(recomendaciones_u)
                if max_amigos_comun is not None and amigos_comun > max_amigos_comun:
                    break
                recomendaciones.append(
                        (u, recomendacion, -amigos_comun))
                max_amigos_comun = amigos_comun
        return recomendaciones


import unittest


class TP1TestCase(unittest.TestCase):

    def verificar_adyacencias(self, grafo, u, adys):
        node = grafo.get_node_data(u)
        ady_ids = set([ grafo.get_node_data(v).id for v in grafo.ady(u)])
        self.assertEqual(ady_ids, adys, "%s == %s" % (ady_ids, adys))

    def test_create_grafo_from_gdf(self):

        grafo = TP1('ejemplo_enunciado.gdf').grafo

        self.assertEqual(grafo.cantidad_vertices, 11)
        self.assertEqual(grafo.cantidad_aristas, 17)

        adys = {}
        adys[1] = set([2,3,4,8,10])
        adys[2] = set([1,6,7])
        adys[3] = set([1,6,10])
        adys[4] = set([1,5,8,9,11])
        adys[5] = set([4,6,7,9])
        adys[6] = set([2,3,5,7])
        adys[7] = set([2,5,6])
        adys[8] = set([1,4])
        adys[9] = set([4,5])
        adys[10] = set([1,3])
        adys[11] = set([4])
        for i in xrange(grafo.cantidad_vertices):
            node = grafo.get_node_data(i)
            self.verificar_adyacencias(grafo, i, adys[node.id])
    
    def verificar_grado_salida(self, grafo, u, grado_esperado):
        self.assertEqual(grafo.get_grado_salida(u), grado_esperado)

    def test_get_grado_salida(self):

        grafo = TP1('ejemplo_enunciado.gdf').grafo

        grado_esperado = {}
        grado_esperado[1] = 5
        grado_esperado[2] = 3
        grado_esperado[3] = 3
        grado_esperado[4] = 5
        grado_esperado[5] = 4
        grado_esperado[6] = 4
        grado_esperado[7] = 3
        grado_esperado[8] = 2
        grado_esperado[9] = 2
        grado_esperado[10] = 2
        grado_esperado[11] = 1

        for i in grafo.iternodes():
            node = grafo.get_node_data(i)
            self.verificar_grado_salida(grafo, i, grado_esperado[node.id])

    def verificar_popularidad(self, esperados, obtenidos):
        self.assertEqual(
                set(esperados),
                set([x.description for x in obtenidos]))

    def test_get_popularidad(self):

        tp1 = TP1('ejemplo_enunciado.gdf')

        popularidad = tp1.get_popularidad()

        self.verificar_popularidad(['Juana','Roberto',], popularidad[5])
        self.verificar_popularidad(['Carlos','Esteban'], popularidad[4])
        self.verificar_popularidad(['Monica','Pablo','Milena'], popularidad[3])
        self.verificar_popularidad(['Brenda','Tomas','Lorena'], popularidad[2])
        self.verificar_popularidad(['Nora'], popularidad[1])
        self.verificar_popularidad([], popularidad[0])

    def test_cantidad_caminos_minimos(self):

        tp1 = TP1('ejemplo_enunciado.gdf')

        tp1.calcular_caminos_minimos()

        cantidad_total_caminos_minimos = 0
        for u in tp1.grafo.iternodes():
            for v in tp1.grafo.iternodes():
                if u>=v:
                    continue
                cantidad_total_caminos_minimos += (
                        tp1.grafo.get_cantidad_caminos_minimos(u,v) )

        self.assertEqual(cantidad_total_caminos_minimos, 121)

    def verificar_cantidad_caminos_minimos_con_intermediario(self, tp1, id, cantidad_esperada):

        cantidad_total_caminos_minimos = 0
        w = tp1.get_vertice_from_id(id)
        for u in tp1.grafo.iternodes():
            for v in tp1.grafo.iternodes():
                if u>=v:
                    continue
                if u == w:
                    continue
                if v == w:
                    continue
                #for recorrido in tp1.grafo.get_recorridos(u,v):
                    #print [ tp1.grafo.get_node_data(x).description for x in recorrido ]
                cantidad_total_caminos_minimos += (
                        tp1.grafo.get_cantidad_caminos_minimos_con_intermediario(u,w,v) )

        self.assertEqual(cantidad_total_caminos_minimos, cantidad_esperada)


    def test_cantidad_caminos_minimos_con_intermediario(self):

        tp1 = TP1('ejemplo_enunciado.gdf')

        tp1.calcular_caminos_minimos()

        cantidad_total_caminos_minimos = 0

        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 4, 36)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 1, 29)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 5, 16)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 6, 7)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 2, 5)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 3, 4)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 7, 3)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 11, 0)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 8, 0)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 10, 0)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 9, 0)

    def test_get_influencias(self):

        tp1 = TP1('ejemplo_enunciado.gdf')

        tp1.calcular_caminos_minimos()

        cantidad_total_caminos_minimos = 0

        influencias = tp1.get_influencias()

        vertices_por_influencia = {}
        for i in xrange(len(influencias)):
            vertices = vertices_por_influencia.get(
                    influencias[i],set())
            vertices.add(tp1.grafo.get_node_data(i).description)
            vertices_por_influencia[influencias[i]] = vertices

        influencias_ordenadas = [(influencia, vertices
            ) for influencia,vertices in vertices_por_influencia.iteritems()]

        influencias_ordenadas.sort()

        self.assertEqual(
                [ vertices for _, vertices in influencias_ordenadas],    
                [set(['Tomas', 'Brenda', 'Lorena', 'Nora']),
                    set(['Pablo']),
                    set(['Milena', 'Monica']),
                    set(['Esteban']),
                    set(['Carlos']),
                    set(['Roberto']),
                    set(['Juana'])])

    def test_recomendaciones(self):

        tp1 = TP1('ejemplo_enunciado.gdf')

        tp1.calcular_caminos_minimos()

        recomendaciones = tp1.recomendaciones()

        recomendaciones = [ (
            tp1.grafo.get_node_data(u).description,
            tp1.grafo.get_node_data(v).description,
            amigos_comun ) for u, v, amigos_comun in
            recomendaciones ]

        #for x in recomendaciones:
            #print x

        self.assertIn(('Pablo','Juana',1), recomendaciones)
        self.assertIn(('Juana','Esteban',1), recomendaciones)
        self.assertIn(('Monica','Milena',2), recomendaciones)
        self.assertIn(('Nora','Tomas',1), recomendaciones)
        self.assertIn(('Lorena','Carlos',1), recomendaciones)
        self.assertIn(('Brenda','Esteban',1), recomendaciones)
        self.assertIn(('Milena','Carlos',2), recomendaciones)
        self.assertIn(('Roberto','Esteban',2), recomendaciones)
        self.assertIn(('Carlos','Milena',2), recomendaciones)
        self.assertIn(('Tomas','Roberto',1), recomendaciones)
        self.assertIn(('Esteban','Roberto',2), recomendaciones)





 

if __name__ == '__main__':
    unittest.main()
