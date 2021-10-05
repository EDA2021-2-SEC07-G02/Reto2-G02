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
    print("1- Cargar información en el catálogo")
    print("2- Seleccionar n obras más antiguas para un medio específico")
    print("4- Clasificar obras dependiendo su nacionalidad ")
    print("7- Salir")

# Funciones de inicialización de catalogo y carga de datos
catalog = None
def initCatalog():
    """
    Inicializa el catalogo de libros

    Párametros:
        ListType: Tipo de lista con la que se hará el catalogo (ARRAY_LIST o LINKED_LIST)

    Retorno:
        Catalogo inicializado
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los artistas y obras en la estructura de datos
    
    Párametros:
        Catalog: Catalogo en donde se añadirán obras y artistas
    
    Retorno:
        Catalogo cardgado con obras y artistas
    """
    try:
        controller.loadData(catalog)
    except:
        print("Error en la carga de información, verifique que los archivos de la base de dato estén en el\
            directorio correcto")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs.isnumeric:
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            catalog=initCatalog()
            loadData(catalog)
            lista_llaves_medium=mp.keySet(catalog["mediums"])
            lista_llaves_nacionality=mp.keySet(catalog["nationality"])
            print("Tamaño de mapa mediums ",lt.size(lista_llaves_medium))
            print("Tamaño de mapa nacionalidades ",lt.size(lista_llaves_nacionality))
        
        # Caso cuando no hay datos cargados
        elif catalog==None and int(inputs[0])!=7:
            print("\nPara correr la funciones cargue la información primero.")

        elif int(inputs[0]) == 2:
            medio=input("Ingrese el medio: ")
            n=int(input("Ingrese la cantidad de obras a seleccionar: "))
            print(controller.obrasMasAntiguas(catalog,medio,n))


            pass
        elif int(inputs[0]) == 4:
            respuesta=controller.clasificarObrasNacionalidad(catalog)
            nacionalidad=input("Ingrese la nacionalidad: ")
            existNationality=mp.contains(respuesta,nacionalidad)
            if existNationality:
                obras=mp.get(respuesta,nacionalidad)
                cantidadobras=me.getValue(obras)["Total_obras"]
                print(nacionalidad,"--- Q obras: ",str(cantidadobras))
            else:
                print("La nacionalidad no existe")
            #nacionalidades=mp.keySet(respuesta)
            # for pais in lt.iterator(nacionalidades):
            #     obras=mp.get(respuesta,pais)
            #     cantidadobras=me.getValue(obras)["Total_obras"]
            #     print(pais,"--- Q obras: ",str(cantidadobras))
        # Opción 0: Salir
        elif int(inputs[0]) == 7:
            sys.exit(0)
        else:
            print("Seleccione una opción válida")
    else:
        print("Seleccione una opción válida")
sys.exit(0)
