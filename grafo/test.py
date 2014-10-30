#!/usr/bin/python
# coding=utf-8

import unittest
from grafo import CaminoInexistente
from grafo_pesado import GrafoPesado
from grafo_no_pesado import GrafoPesoUnitario

class GrafoPesoUnitarioTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GrafoPesoUnitarioTestCase, self).__init__(*args,**kwargs)
        self.clase_grafo = GrafoPesoUnitario

    def test_cantidad_caminos_minimos(self):

        grafo = self.clase_grafo()

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
 
        grafo = self.clase_grafo()

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
 
        grafo = self.clase_grafo()

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
 
        grafo = self.clase_grafo()

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

    def test_grafo_no_conexo(self):
 
        grafo = self.clase_grafo()

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
        grafo.connect(10,11,both=True)
        grafo.connect(10,12,both=True)
        grafo.connect(11,13,both=True)
        grafo.connect(12,13,both=True)

        for i in grafo.iternodes():
            grafo.calcular_camino_minimo(i)

        self.assertRaises(CaminoInexistente,
                grafo.get_distancia,0,10)
        self.assertEqual(
                grafo.get_distancia(8,9), 6)

        self.assertRaises(CaminoInexistente,
                grafo.get_recorrido_anchura_caminos_minimos,
                0,13)

        self.verificar_recorrido_anchura(
                grafo.get_recorrido_anchura_caminos_minimos(0,9),
                [
                    set([0]),
                    set([2]),
                    set([5,6,7]),
                    set([9]),
                    ])

        self.verificar_recorrido_anchura(
                grafo.get_recorrido_anchura_caminos_minimos(13,10),
                [
                    set([13]),
                    set([11,12]),
                    set([10]),
                    ])

        self.validar_recorrido(grafo,0,8,
            [[0,1,3,8],
              [0,1,4,8],
              ])
        self.validar_recorrido(grafo,0,10,
            [])
        self.validar_recorrido(grafo,7,3,
            [[7,2,0,1,3],
              ])
        self.validar_recorrido(grafo,13,4,
            [])
        self.validar_recorrido(grafo,11,12,
            [[11,10,12],
              [11,13,12],
              ])


        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(0,13,10),
            0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(0,10,13),
            0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(0,1,8),
            2)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(2,5,11),
            0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos_con_intermediario(2,5,11),
            0)
 
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(2,10),0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(0,10),0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(0,13),0)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(4,5),1)
        self.assertEqual(
            grafo.get_cantidad_caminos_minimos(8,9),6)


class GrafoPesadoTestCase(GrafoPesoUnitarioTestCase):

    def test_camino_minimo(self):

        grafo = self.clase_grafo(cantidad_vertices=7, pesos=[
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


    def __init__(self, *args, **kwargs):
        super(GrafoPesadoTestCase, self).__init__(*args,**kwargs)
        self.clase_grafo = GrafoPesado


if __name__ == '__main__':
    unittest.main()
