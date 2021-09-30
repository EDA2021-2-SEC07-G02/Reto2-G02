"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Salir")
    print("1- Cargar información en el catálogo")
    print("2- Seleccionar n obras más antiguas para un medio específico")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=controller.initCatalog()
        controller.loadData(catalog)
        lista_llaves=mp.keySet(catalog["mediums"])
        print("Tamaño de mapa ",lt.size(lista_llaves))
        

    elif int(inputs[0]) == 2:
        medio=input("Ingrese el medio: ")
        n=int(input("Ingrese la cantidad de obras a seleccionar: "))
        print(controller.obrasMasAntiguas(catalog,medio,n))

        pass

    # Opción 0: Salir
    elif int(inputs[0]) == 0:
        sys.exit(0)
    else:
        print("Seleccione una opción válida") 
sys.exit(0)
