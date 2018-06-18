#!/usr/bin/env python3

"""
Title:      Python Colors
Author:     Jason Scott
Email:      jgs85@protonmail.com
Version:    1.0
Date:       11 Jun 2018

PEP 8 COMPLIANT
"""


def col(n, text):
    color = {
        'thin': 2, 'i': 3, 'u': 4, 'neg': 7, 'black': 8, 'strike': 9, 'gr': 30, 'r': 31, 'g': 32, 'y': 33, 'b': 34,
        'p': 35, 'c': 36, 'w': 37, 'rbg': 41, 'gbg': 42, 'ybg': 43, 'bbg': 44, 'pbg': 45, 'cbg': 46, 'gr2': 90,
        'r2': 91, 'g2': 92, 'y2': 93, 'b2': 94, 'p2': 95, 'c2': 96, 'grbg2': 100, 'rbg2': 101, 'gbg2': 102,
        'ybg2': 103, 'bbg2': 104, 'pbg2': 105, 'cbg2': 106, 'n':0
    }
    return '\33[{}m{}\33[0m'.format(color[n], text)
