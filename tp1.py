#!/usr/bin/python
# coding=utf-8
from grafo import GrafoPesoUnitario
import re
from heapq import heappop, heappush
import sys

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
        """
        O(1)
        """
        fields = line.split(',')
        return Node(id=fields[0], description=fields[1])


class TP1:

    def __init__(self, filepath, grafo=None):
        """
        O(max(|E|,|V|)*|V|)
        """
        if grafo is not None:
            self.grafo = grafo
        else:
            self.grafo = GrafoPesoUnitario()

        self.vertice_from_id = {}
        linetype = None

        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if re_nodedef.match(line):
                    linetype = NODEDEF_TYPE
                elif re_edgedef.match(line):
                    linetype = EDGEDEF_TYPE
                elif linetype == NODEDEF_TYPE: # |V|
                    # O(1)
                    node = Node.create_node_from_gdf_line(line)
                    # O(|V|)
                    # TODO Ver si aplica vertice_from_id y cambiar implementación
                    self.vertice_from_id[node.id] = self.grafo.add_node(node)
                elif linetype == EDGEDEF_TYPE: # |E|
                    id1, id2 = map(int, line.split(','))
                    # O(|V|)
                    v1, v2 = self.vertice_from_id[id1], self.vertice_from_id[id2]
                    # O(log(|V|))
                    self.grafo.connect(v1, v2, both=True)

    def get_popularidad(self):
        """
        O(|V|)
        Obtiene un listado L donde el componente L[i] contiene un 
        listado de vertices con popularidad i. len(L) == |V|.
        """

        popularidad = []

        # O(|V|)
        for i in self.grafo.iternodes():
            popularidad.append([])

        # O(|V|)
        for u in self.grafo.iternodes():
            # O(1)
            grado = self.grafo.get_grado_salida(u)
            popularidad[grado].append(self.grafo.get_node_data(u))

        return popularidad

    def mostrar_popularidad(self, popularidad):
        """
        O(|V|)
        """
        for i in xrange(len(popularidad)-1, -1, -1):
            if len(popularidad[i]) == 0:
                continue
            print "#%s: %s" % (i, [ x.description for x in popularidad[i]])

    def mostrar_influencias(self, influencias):
        """
        O(|V|**2)
        """

        vertices_por_influencia = {}

        # O(|V|**2)
        for i in xrange(len(influencias)): # |V|
            # O(|V|)
            vertices = vertices_por_influencia.get( 
                    influencias[i],set())
            # O(|V|)
            vertices.add(self.grafo.get_node_data(i).description)
            # O(|V|)
            vertices_por_influencia[influencias[i]] = vertices

        # O(|V|)
        influencias_ordenadas = [(influencia, vertices
            ) for influencia,vertices in vertices_por_influencia.iteritems()]

        # O(|V|*log(|V|))
        influencias_ordenadas.sort(reverse=True)
        
        # O(|V|)
        for x in influencias_ordenadas:
            print x

    def mostrar_recomendaciones(self, recomendaciones):
        """
        O(n*log(n))
        """

        # O(n*log(n))
        recomendaciones.sort(key=lambda x:x[2], reverse=True)

        # O(n)
        _recomendaciones = [ (
            self.grafo.get_node_data(u).description,
            self.grafo.get_node_data(v).description,
            amigos_comun ) for u, v, amigos_comun in
            recomendaciones ]

        # O(n)
        for persona, recomendacion, amigos_comun in _recomendaciones:
            print '%s: %s (%s amigo(s) en común)' % (
                    persona, recomendacion, amigos_comun)


    def get_influencias(self):
        """
        O((|V|**2)*(|V|+|E|))
        Se obtiene el índice de influencia por cada vertice.
        """
        # O(n)
        influencias = [0 for w in self.grafo.iternodes()]


        # Preprocesamiento de cantidad de caminos mínimos
        # O((|V|**2)*(|V|+|E|))
        for u in self.grafo.iternodes():  # |V|
            for v in self.grafo.iternodes():  # |V|
                cantidad_u_v = self.grafo.get_cantidad_caminos_minimos(u,v) # O(|V|+|E|)

        # O(|V|**3)
        for u in self.grafo.iternodes():  # |V|
            for v in self.grafo.iternodes():  # |V|
                if u>=v:
                    continue
                # O(1) c/preprocesamiento
                cantidad_u_v = self.grafo.get_cantidad_caminos_minimos(u,v)
                if cantidad_u_v == 0:
                    continue
                for w in self.grafo.iternodes(): # |V|
                    if w==u or w==v:
                        continue
                    influencias[w] += float(
                                # O(1) (c/preprocesamiento)
                                self.grafo.get_cantidad_caminos_minimos_con_intermediario(u,w,v)
                                ) / cantidad_u_v
        return influencias

    def calcular_caminos_minimos(self):
        """
        O(|V|*(|E|+|V|)
        """
        # |V|
        for i in self.grafo.iternodes():
            # O(|V|+|E|)
            self.grafo.calcular_camino_minimo(i)

    def get_vertice_from_id(self, id):
        """
        O(|V|)
        """
        return self.vertice_from_id[id]

    def recomendaciones_para(self, u):
        """
        Au: Cantidad de aristas que salen de u.
        O(Sum(v in V,Au+Av)) = O(Au*|V|+|A|)
        Devuelve un heap con las recomendaciones. Solo se recomienda en 
        caso que exista algún amigo en común.
        """
        # O(Au)
        recomendaciones = []
        for v in self.grafo.iternodes():
            if u==v:
                continue
            # O(log(Au))
            if self.grafo.conectados(u,v):
                continue
            # O(Au+Av)
            cantidad_conexiones_en_comun = - len(
                    self.grafo.conexiones_en_comun(u,v))
            if cantidad_conexiones_en_comun == 0:
                continue
            # O(log(|V|))
            heappush(recomendaciones, (cantidad_conexiones_en_comun, v))
        return recomendaciones

    def recomendaciones(self):
        """
        O(Sum(u in V,Au*|V|+|A|)) = O(|V|*Sum(u in V,Au)+|V|*|A|) =
        = O(|V|*|A|+|V|*|A|) = O(|V|*|A|)
        Devuelve un listado donde cada item tiene:
        (vertice, recomendacion, amigos_en_comun)
        """
        recomendaciones = []
        for u in self.grafo.iternodes():
            recomendaciones_u = self.recomendaciones_para(u) # O(Au*|V|+|A|)
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

        self.assertEqual(cantidad_total_caminos_minimos, 132/2)

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

        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 4, 38/2)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 1, 38/2)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 5, 22/2)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 6, 16/2)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 2, 10/2)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 3, 10/2)
        self.verificar_cantidad_caminos_minimos_con_intermediario(tp1, 7, 4/2)
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
        
        #for x in influencias_ordenadas:
            #print x

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


def inicio_seccion(nombre):
    """
    O(1)
    """
    print '-----------------%s-----------------' % nombre

def fin_seccion():
    """
    O(1)
    """
    print '-------------------------------------------'
    print

def reporte_amigos_facebook_gdf(filepath):
    """
    O((|V|**2)*(|V|+|A|))
    """
    
    tp1 = TP1(filepath) # O(max(|E|,|V|)*|V|)

    tp1.calcular_caminos_minimos() # O(|V|*(|E|+|V|)

    inicio_seccion('Archivo %s' % filepath)

    inicio_seccion('popularidad')
    popularidad = tp1.get_popularidad() # O(|V|)
    tp1.mostrar_popularidad(popularidad) # O(|V|)
    fin_seccion()

    inicio_seccion('influencias')
    influencias = tp1.get_influencias() # O((|V|**2)*(|V|+|A|))
    tp1.mostrar_influencias(influencias) # O(|V|**2)
    fin_seccion()

    inicio_seccion('recomendaciones')
    recomendaciones = tp1.recomendaciones() # O(|V|*|A|)
    tp1.mostrar_recomendaciones(recomendaciones) # O(n*log(n))
    fin_seccion()

    fin_seccion()

def reporte_amigos_facebook():
    for filepath in sys.argv[1:]:
        reporte_amigos_facebook_gdf(filepath) # O((|V|**2)*(|V|+|A|))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    else:
        reporte_amigos_facebook()
