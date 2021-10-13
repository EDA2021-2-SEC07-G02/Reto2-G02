"""
 * Copyright 2020, Departamento de sistemas y Computación,
 *  Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from DISClib.ADT import list as lt
assert cf

"""
  Los algoritmos de este libro están basados en la implementación
  propuesta por R.Sedgewick y Kevin Wayne en su libro
  Algorithms, 4th Edition
"""


def sort(lst, cmpfunction):
    size = lt.size(lst)
    pos1 = 1
    while pos1 < size:
        minimum = pos1    # minimun tiene el menor elemento
        pos2 = pos1 + 1
        while (pos2 <= size):
            if (cmpfunction(lt.getElement(lst, pos2),
               (lt.getElement(lst, minimum)))):
                minimum = pos2  # minimum = posición elemento más pequeño
            pos2 += 1
        lt.exchange(lst, pos1, minimum)  # elemento más pequeño -> elem pos1
        pos1 += 1
    return lst

#Hicimos algunos cambios al algoritomo de selection sort

def sortEdit(lst, cmpfunction,posAOrdenar,ordenarInicio=True,ordenarFinal=False):
    """
    !!!Algoritmo de selection sort con modificaciones para el reto.

    Este algoritmo solamente ordenará las n primeras y últimas posiciones en la lista,
    es decir, no se ordenará la lista completa. 
        Parámetro extra:
            posAOrdenar: Número entero que hace referencia a cuántas posiciones iniciales y finales deben ser
            ordenas.
    """
    size = lt.size(lst)
    pos1 = 1
    iteraciones=0
    while pos1 < size and iteraciones<posAOrdenar and ordenarInicio: #El algoritmo se detendrá al tener ordenado las x primeras posiciones
        minimum = pos1    # minimun tiene el menor elemento
        pos2 = pos1 + 1
        while (pos2 <= size):
            if (cmpfunction(lt.getElement(lst, pos2),
               (lt.getElement(lst, minimum)))):
                minimum = pos2  # minimum = posición elemento más pequeño
            pos2 += 1
        lt.exchange(lst, pos1, minimum)  # elemento más pequeño -> elem pos1
        pos1 += 1
        iteraciones+=1
    
    pos1M=size
    iteraciones=0
    while pos1M > 1 and iteraciones<posAOrdenar and ordenarFinal: #El algoritmo se detendrá al tener ordenado las x últimas posiciones
        maximum = pos1M    # maximum tiene el maximo elemento
        pos2 = pos1M - 1
        while (pos2 > 1):
            if not (cmpfunction(lt.getElement(lst, pos2),
                (lt.getElement(lst, maximum)))):
                maximum = pos2  # maximum = posición elemento más grande
            pos2 -= 1
        lt.exchange(lst, pos1M, maximum)  # elemento más grande -> elem pos1
        pos1M -= 1
        iteraciones+=1
    return lst
