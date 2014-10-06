#!/usr/bin/python
# coding=utf-8

import bisect

class ListaAdy():

    def __init__(self):
        self.lista = []

    def iteritems(self):
        return iter(self.lista)

    def insert(self, node):
        """
        O(n*log(n))
        """
        i = bisect.bisect_left(self.lista, node)
        if i <> len(self.lista) and self.lista[i] == node: 
            raise Exception('El nodo %s ya existe en la lista.' % node)
        return self.lista.insert(i, node)

    def has(self, node):
        """
        O(n*log(n))
        """
        i = bisect.bisect_left(self.lista, node)
        if i <> len(self.lista) and self.lista[i] == node: 
            return True
        return False

    def intersection(self, other):
        """
        O(len(self.lista)+len(other.lista)) = O(n1+n2)
        """
        len_self = len(self.lista)
        len_other = len(other.lista)
        i_self = 0
        i_other = 0
        intersection = []

        while i_self < len_self and i_other < len_other:
            x_self = self.lista[i_self]
            x_other = other.lista[i_other]

            if x_self < x_other:
                i_self += 1
            elif x_self > x_other:
                i_other += 1
            else:
                intersection.append(x_self)
                i_self += 1
                i_other += 1

        return intersection


import unittest


class ListaAdyTestCase(unittest.TestCase):
    
    def test_insert(self):

        l = ListaAdy()

        l.insert(10)
        l.insert(1)
        l.insert(3)
        l.insert(5)
        l.insert(2)

        items = [ x for x in l.iteritems()]

        self.assertEqual(items, [1,2,3,5,10])

    def test_has(self):

        l = ListaAdy()

        l.insert(10)
        l.insert(1)
        l.insert(3)
        l.insert(5)
        l.insert(2)

        self.assertFalse(l.has(9))
        self.assertTrue(l.has(1))
        self.assertTrue(l.has(5))
        self.assertTrue(l.has(10))

    def test_intersection(self):

        l1 = ListaAdy()
        l2 = ListaAdy()

        self.assertEqual(l1.intersection(l2), [])

        l1.insert(10)
        l1.insert(1)
        l1.insert(3)
        l1.insert(5)
        l1.insert(2)

        l2.insert(10)
        l2.insert(1)
        l2.insert(2)
        l2.insert(6)

        self.assertEqual(l1.intersection(l2), [1,2,10])

        self.assertEqual(l1.intersection(l1), l1.lista)
        self.assertEqual(l2.intersection(l2), l2.lista)



if __name__ == '__main__':
    unittest.main()
