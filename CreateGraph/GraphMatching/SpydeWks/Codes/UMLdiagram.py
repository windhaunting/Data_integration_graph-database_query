# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:31:57 2016

@author: fubao
"""
import sys

sys.path.insert(3, 'lib')
sys.path.insert(3, 'lib/pycana')

from mainEntry import dataMatching

from pycana import CodeAnalyzer

import mainEntry

analyzer= CodeAnalyzer(mainEntry)
relations= analyzer.analyze()
analyzer.draw_relations(relations, 'class_diagramxx.png')