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
    print("0- Cargar información en el catálogo")
    print("1- Listar cronólogicamente a artistas")
    print("2- Seleccionar n obras más antiguas para un medio específico")
    print("4- Clasificar obras dependiendo su nacionalidad ")
    print("7- Salir")

# Funciones de inicialización de catalogo y carga de datos
catalog = None
def initCatalog(mapLab,FactorCarga):
    """
    Inicializa el catalogo de libros

    Párametros:
        ListType: Tipo de lista con la que se hará el catalogo (ARRAY_LIST o LINKED_LIST)

    Retorno:
        Catalogo inicializado
    """
    return controller.initCatalog(mapLab,FactorCarga)

def loadData(catalog,nArtists=6656,nArtWork=15008):
    """
    Carga los artistas y obras en la estructura de datos
    
    Párametros:
        Catalog: Catalogo en donde se añadirán obras y artistas
    
    Retorno:
        Catalogo cardgado con obras y artistas
    """
    try:
        controller.loadData(catalog,nArtists,nArtWork)
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
        if int(inputs[0]) == 0:
            print("\nCargando información de los archivos ....")
            mapLab0=input("(Prueba) Selecione el mapa (1- 'CHAINING' 2-'PROBING')\n")
            FactorCarga=float(input("Ingrese el factor de carga:  "))
            mapLab='PROBING'
            if mapLab0==1:
                mapLab="CHAINING"
            catalog=initCatalog(mapLab,FactorCarga)
            print("Se cargaron los mapas de Nacionalidad y Medios con "+mapLab+" Factor de carga: "+str(FactorCarga))
            loadData(catalog,nArtists=1948,nArtWork=768)
            print("\n\nSe ha completado la carga de artworks y artistas al catálogo")
            print("Tamaño de mapa artworks: ",catalog["artworks"]["size"])
            print("Tamaño de mapa artistas: ",catalog["artists"]["size"])
            print("Tamaño de mapa mediums: ",catalog["mediums"]["size"])
            print("Tamaño de mapa nacionalidades: ",catalog["nationalities"]["size"])
        
        # Caso cuando no hay datos cargados
        elif catalog==None and int(inputs[0])!=7:
            print("\nPara correr la funciones cargue la información primero.")
        
        elif int(inputs[0])==1:
            fechaInicial=input("\nIngrese el año inicial (AAAA): ")
            fechaFinal=input("\nIngrese el año final (AAAA): ")
            resultado= controller.listarArtistasCronologicamente(catalog, fechaInicial, fechaFinal)
            print("\nHay ",str(resultado[1])," artistas en este rango de fechas")
            nartistasView=0
            posInicial=1
            print("3 primeros artistas")
            while nartistasView<=3:
                fechaIn=lt.getElement(resultado[0],posInicial)
                artistasLista=mp.get(catalog["Artists_BeginDate"],str(fechaIn))["value"]["Artistas"]
                #print(artistasLista)
                for artista in lt.iterator(artistasLista):
                    nartistasView+=1
                    print(nartistasView,mp.get(catalog["artists"],artista)["value"])
                    if nartistasView>=3:
                        print(artista,nartistasView)
                        break
                posInicial+=1

        elif int(inputs[0]) == 2:
            medio=input("Ingrese el medio: ")
            n=int(input("Ingrese la cantidad de obras a seleccionar: "))
            print(controller.obrasMasAntiguas(catalog,medio,n))


            pass
        elif int(inputs[0]) == 4:
            respuesta=controller.clasificarObrasNacionalidad(catalog)
            opcion=int(input("Seleccione la respuesta que quiere ver: \n1- Lab6 \n2- Reto 2\n"))
            if opcion==1:
                print("\n--- Lab 6 ---")
                nacionalidad=input("Ingrese la nacionalidad: ")
                respuesta=controller.buscarNacionalidad(catalog,nacionalidad)
                print("Cantidad de obras en la nacionalidad:"+nacionalidad+"\nCantidad obras: "+respuesta)

            if opcion==2:
                print("\n--- Reto 2 ---")
                print("\n Top 10 países por obras")
                print(respuesta[0])
                i=1
                for nationality in lt.iterator(respuesta[0]):
                    print(str(i)+". "+nationality["Nacionalidad"]+" - Q:"+str(nationality["Total_obras"]))
                    i+=1
                    if i>10:
                        break
                print("\nPrimer Lugar: "+respuesta[1])
                print("\nObras del primer lugar:\n\n")
                # nacionalidades=mp.keySet(respuesta)
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
