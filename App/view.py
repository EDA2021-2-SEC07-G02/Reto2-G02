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
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import prettytable
from prettytable import PrettyTable


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("-"*25+"Bienvenido"+ "-"*25)
    print("0- Cargar información en el catálogo")
    print("1- Listar cronólogicamente a artistas")
    print("2- Seleccionar n obras más antiguas para un medio específico")
    print("4- Clasificar obras dependiendo su nacionalidad ")
    print("5- Precio de transporte de obras por departamento")
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

def loadData(catalog,nArtists=6656,nArtWork=15008):
    """
    Carga los artistas y obras en la estructura de datos
    
    Párametros:
        Catalog: Catalogo en donde se añadirán obras y artistas
    
    Retorno:
        Catalogo cardgado con obras y artistas
    """
    controller.loadData(catalog,nArtists,nArtWork)
    try:
        pass
    except:
        print("Error en la carga de información, verifique que los archivos de la base de dato estén en el\
            directorio correcto")

##PrettyTable

def printNationalityArt(ord_Nationality):
    """
    Imprime los resultados del requerimiento 4

    Parámetros:
        ord_Nationality:lista con países y sus obras de arte
    
    print(NationalityPretty) >> Imprime la tabla hecha por medio de PrettyTable
    controller.limpiarVar(NationalityPretty) >> Limpia la tabla hecha (dato provisional)
    """
    NationalityPretty=PrettyTable(hrules=prettytable.ALL)
    NationalityPretty.field_names=["Nationality","ArtWorks"]
    NationalityPretty.align="l"
    NationalityPretty._max_width = {"Nationality" : 15, "ArtWorks" : 5}
    for nationality in lt.iterator(ord_Nationality):
        NationalityPretty.add_row((nationality["Nacionalidad"],nationality["Total_obras"]))
    print(NationalityPretty)

def printResultsArt(ord_artwork, cadenaOpcion, sample=3):
    """
    Esta función es usada para mostrar a las 3 primeras y últimas obras 
    en distintas opciones del view. 
    
    Parámetros:
        ord_artwork: Catalogo de obras de arte (Cargado por catalogo en la opción 1 o ordenado por fechas de la opción 3)
        sample: Hace referencia a la cantidad de primeras y últimas obras que se quieren mostrar al usuario. 
                Su valor predeterminado es 3 por requisitos del proyecto.
        cadenaOpcion: Es usado para imprimir si las obras fueron cargadas o ordenadas 
    
    print(artPretty) >> Imprime la tabla
 
    """
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=["ObjectID","Title","Artists Names","Medium",
                            "Dimensions","Date","DateAcquired","URL"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                            "Dimensions":15,"Date":12,"DateAcquired":11,"URL":10}
    
    for artwork in lt.iterator(ord_artwork):
        dispname_artwork=artwork["NombresArtistas"][0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],dispname_artwork,artwork['Medium'],
                        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL']))
    print(artPretty)

def printResultsArtists(ord_artist, sample=3):
    """
    Esta función es usada para mostrar a los 3 primeros y últimos artistas 
    en distintas opciones del view. 
    
    Parámetros:
        ord_artist: Catalogo de artistas
        sample: Hace referencia a la cantidad de primeras y últimas artistas que se quieren mostrar al usuario.
                Su valor predeterminado es 3 por requisitos del proyecto.
        cadenaOpcion: Es usado para imprimir si los artistas fueron cargados al catalogo o ordenadas 
    
    Print(artistPretty) >> Imprime la tabla
    controller.limpiarVar(artistPretty) >> Borra la tabla hecha. Dato provisional
    """
    size = ord_artist["size"]
    
    artistPretty=PrettyTable(hrules=prettytable.ALL)
    artistPretty.field_names=["ConstituentID","DisplayName","BeginDate","Nationality",
                            "Gender","ArtistBio","Wiki QID","ULAN"]
    artistPretty.align="l"
    artistPretty._max_width = {"ConstituentID":7,"DisplayName":15, "BeginDate":8,
                                "Nationality":15,"Gender":12, "ArtistBio":15,"Wiki QID":10,"ULAN":15}
    
    for artist in lt.iterator(ord_artist):
        #ArtistBio=artist["Nationality"]+"- Unknown"
        artistPretty.add_row((artist['ConstituentID'], artist['DisplayName'],artist['BeginDate'],artist['Nationality'],
                            artist['Gender'],artist['ArtistBio'],artist['Wiki QID'],artist['ULAN']))
    print(artistPretty)

def printTableTransPricesArtworks(ord_artwork, cadena, sample=5):
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=["ObjectID","Title","ArtistsNames","Medium",
                            "Date","Dimensions","Classification","TransCost (USD)","URL"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"ArtistsNames":13,"Medium":15,
                            "Date":12,"Dimensions":10,"Classification":11,"TransCost (USD)":11,"URL":10}
    size=ord_artwork["size"]
    if size>=sample:
        print("\nTOP "+str(sample) +" de las obras más "+cadena+" de transportar")
        indices=range(1,sample+1)
    else:
        print("\nTOP "+str(size) +" de las obras más "+cadena+" de transportar")
        indices=range(size)

    for i in indices:
        if i >= lt.size(ord_artwork):
            break
        artwork = lt.getElement(ord_artwork,i)
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],artwork['NombresArtistas'],artwork['Medium'],
                            artwork['Date'],artwork['Dimensions'],artwork['Classification'],
                            round(artwork['TransCost (USD)'],3),artwork['URL'] ))
    print(artPretty)


def printFirstLastsResultsArt(ord_artwork, cadenaOpcion, sample=3):
    """
    Esta función es usada para mostrar a las 3 primeras y últimas obras 
    en distintas opciones del view. 
    
    Parámetros:
        ord_artwork: Catalogo de obras de arte (Cargado por catalogo en la opción 1 o ordenado por fechas de la opción 3)
        sample: Hace referencia a la cantidad de primeras y últimas obras que se quieren mostrar al usuario. 
                Su valor predeterminado es 3 por requisitos del proyecto.
        cadenaOpcion: Es usado para imprimir si las obras fueron cargadas o ordenadas 
    
    print(artPretty) >> Imprime la tabla
    controller.limpiarVar(artPretty) >> Borra la tabla hecha. Dato provisional
    """
    size = ord_artwork["size"]
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=["ObjectID","Title","Artists Names","Medium",
                            "Dimensions","Date","DateAcquired","URL"]
    artPretty.align="l"
    artPretty._max_width = {"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                            "Dimensions":15,"Date":12,"DateAcquired":11,"URL":10}
    
    if size > sample*2: #Esto evita errores de list out of range
        print("\nLas "+ str(sample)+" primeras y últimas obras "+cadenaOpcion) #se hace un rango de recorrido
        indices=list(range(1,sample+1))+list(range(size-sample,size))
    else:
        indices=range(size)
        print("\nLas "+ str(size)+" obras "+cadenaOpcion)
    
    for i in indices:
        artwork = lt.getElement(ord_artwork,i)
        dispname_artwork=(controller.getArtistName(catalog,artwork["ConstituentID"]))[0:-1]
        artPretty.add_row((artwork['ObjectID'],artwork['Title'],dispname_artwork,artwork['Medium'],
                        artwork['Dimensions'],artwork['Date'],artwork['DateAcquired'],artwork['URL']))
    print(artPretty)
    controller.limpiarVar(artPretty) #Se elimina la tabla dado que es un dato provisional


def printPrettyTable(lista, keys, field_names, max_width, sample=3, ultimas=False):
    artPretty=PrettyTable(hrules=prettytable.ALL)
    artPretty.field_names=field_names
    artPretty._max_width = max_width

    cont=1

    for elemento in lt.iterator(lista):
        valoresFila=[]
        for key in keys:
            valoresFila.append(elemento[key])
        artPretty.add_row(tuple(valoresFila))
        if cont>=sample:
            break
        cont+=1
    
    if ultimas:
        ultimo_index=lt.size(lista) # aRRAY LIST
        cont2=1
        while cont2<=sample:
            indice=ultimo_index-sample+cont2
            if indice>cont and indice>=0 and lt.size(lista)>=indice:
                elemento=lt.getElement(lista,indice)
                valoresFila=[]
                for key in keys:
                    valoresFila.append(elemento[key])
                artPretty.add_row(valoresFila)
            cont2+=1
            
            
    
    print(artPretty)

def printRequerimiento2(resultado):
    if resultado[2] > 0:

        maxWidth={"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                            "Dimensions":15,"Date":12,"DateAcquired":11,"URL":10}
        fieldNames= ["ObjectID","Title","Artists Names","Medium",
                            "Dimensions","Date","DateAcquired","URL"]

        keys= ["ObjectID","Title","ArtistsNames","Medium",
                            "Dimensions","Date","DateAcquired","URL"]
        
        print("\nEl total de obras en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[2]))
        print("\nEl total de diferentes artistas para la obras seleccionadas en el rango: "+str(resultado[3]))
        print("\nEl total de obras compradadas ('Purchase') en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[1]))
        print("\nLas tres primeras y tres ultimas obras del rango se registran en la siguiente tabla:")

        printPrettyTable(resultado[0],keys,fieldNames,maxWidth,sample=3,ultimas=True)

    else:
        print("\nNo  existe ninguna obra en las base de datos que haya sido registrada entre",fechaInicial,"y",fechaFinal,"o las fechas ingresadas no siguen el formato correcto.")
    controller.limpiarVar(resultado) #Se borra el resultado - Dato provisional

def printMediums(ord_mediums,top=5):
    medPretty=PrettyTable(hrules=prettytable.ALL)
    medPretty.field_names=["Tecnica","Cantidad"]
    medPretty.align="l"
    medPretty._max_width = {"Tecnica" : 15, "Cantidad" : 5}
    cont=0
    for tecnica in lt.iterator(ord_mediums):
        nombreTecnica=lt.getElement(tecnica,0)["Medium"]
        medPretty.add_row((nombreTecnica,str(lt.size(tecnica))))
        cont+=1
        if(cont>=top):
            break
    print(medPretty)

def printRequerimiento3(respuesta,nombreArtista):
    tecnicas=respuesta[0]
    totalObras=respuesta[1]
    if totalObras!=0:
        obrasTecnica=lt.getElement(tecnicas,0)
        tecnica=lt.getElement(obrasTecnica,0)["Medium"]
        print("El artista",str(nombreArtista),"tiene",totalObras,"obras en total. De las",lt.size(tecnicas),"ténicas empleadas la más utilizada es",\
            str(tecnica)+".\n")
        print("La lista de las 5 técnica más utilizadas")

        printMediums(tecnicas)


        print("\nA continuación se presentan 3 primera obras y 3 ultimas obras realizadas con la técnica",str(tecnica)+":")

        keys=["ObjectID","Title","Medium","Date","Dimensions",
                            "DateAcquired","Department","Classification","URL"]
        fieldNames=["ObjectID","Title","Medium","Date","Dimensions",
                            "DateAcquired","Department","Classification","URL"]
        maxWidth = {"ObjectID" : 10, "Title" : 15,"Medium":13,
                            "Date":12,"Dimensions":15,"DateAcquired":11,"Department":10,"Classification":10,"URL":10}

        printPrettyTable(obrasTecnica,keys,fieldNames,maxWidth,sample=3,ultimas=True)
    else:
        print("El artista",nombreArtista,"no existe en la base de datos o no tiene ninguna obra registrada.")

def printRequerimiento6(respuesta,fecha_inicial,fecha_final,n):
    artistas=respuesta[0]
    numArtistas=respuesta[1]
    if(numArtistas>0):
        print("\n Hay",numArtistas,"en el periodo de",str(fecha_inicial),"a",str(fecha_final))
        print("\nLos",str(n),"artistas más prolíficos son:")
        keys=["ConstituentID","DisplayName","BeginDate","Gender","ArtistBio",
                            "Wiki QID","ULAN","ArtworkNumber","MediumNumber","TopMedium"]
        fieldNames=["ConstituentID","DisplayName","BeginDate","Gender","ArtistBio",
                            "Wiki QID","ULAN","ArtworkNumber","MediumNumber","TopMedium"]
        maxWidth = {"ConstituentID":10,"DisplayName":10,"BeginDate":5,"Gender":5,"ArtistBio":10,
                            "Wiki QID":5,"ULAN":10,"ArtworkNumber":5,"MediumNumber":5,"TopMedium":5}
        printPrettyTable(artistas,keys,fieldNames,maxWidth,sample=n,ultimas=False)

    else:
        print("\nNo hay artistas en el rango seleccionado")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs.isnumeric:
        if int(inputs[0]) == 0:
            tiempoInicial=time.process_time()
            print("\nCargando información de los archivos ....")
            catalog=initCatalog()
            loadData(catalog,nArtists=1948,nArtWork=768)
            print("\n\nSe ha completado la carga de artworks y artistas al catálogo")
            print("Tamaño de LISTA artworks: ",catalog["artworks"]["size"])
            print("Tamaño de mapa artistas: ",catalog["artists"]["size"])


            print("\nTamaño de mapa mediums: ",catalog["mediums"]["size"])
            print("Capacidad final mapa nacionalidades: ",catalog["mediums"]["capacity"])

            print("\nTamaño de mapa nacionalidades: ",catalog["nationalities"]["size"])
            print("Capacidad final mapa nacionalidades: ",catalog["nationalities"]["capacity"])
            #catalog["Artists_BeginDate"]
            print("\nTamaño de mapa fechas de nacimiento: ",catalog["Artists_BeginDate"]["size"])
            print("\nTamaño de mapa deptos museo: ",catalog["Department"]["size"])
        
        # Caso cuando no hay datos cargados
        elif catalog==None and int(inputs[0])!=7:
            print("\nPara correr la funciones cargue la información primero.")
        
        elif int(inputs[0])==1:
            tiempoInicial=time.process_time()
            fechaInicial=input("\nIngrese el año inicial (AAAA): ")
            fechaFinal=input("\nIngrese el año final (AAAA): ")
            resultado= controller.listarArtistasCronologicamente(catalog, fechaInicial, fechaFinal)
            print("\nHay ",str(resultado[1])," artistas en este rango de fechas")
            nartistasView=0
            posInicial=1
            print("3 primeros artistas")
            print("Func Lista",resultado[2])
            print("PRETTY TABLEEEEEEE")
            print(printResultsArtists(resultado[2]))
            # while nartistasView<=3:
            #     fechaIn=lt.getElement(resultado[0],posInicial)
            #     artistasLista=mp.get(catalog["Artists_BeginDate"],str(fechaIn))["value"]["Artistas"]
            #     #print(artistasLista)
            #     for artista in lt.iterator(artistasLista):
            #         nartistasView+=1
            #         print(nartistasView,mp.get(catalog["artists"],artista)["value"])
            #         if nartistasView>=3:
            #             print(artista,nartistasView)
            #             break
            #     posInicial+=1


        elif int(inputs[0]) == 2:
            fechaInicial=input("\nIngrese la fecha inicial (AAAA-MM-DD): ")
            fechaFinal=input("\nIngrese la fecha final (AAAA-MM-DD): ")
            tiempoInicial=time.process_time()
            resultado= controller.listarAdquisicionesCronologicamente(catalog, fechaInicial, fechaFinal)
            printRequerimiento2(resultado)

        
        elif int(inputs[0]) == 3:
            tiempoInicial=time.process_time()
            nombre=input("Ingrese el nombre del artista: ")
            resultado= controller.tecnicasObrasPorArtista(catalog,nombre)
            printRequerimiento3(resultado,nombre)


            pass
        elif int(inputs[0]) == 4:
            tiempoInicial=time.process_time()
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
                print("\n Total países: " + str(respuesta[3]))
                print(respuesta[0])
                i=1
                printNationalityArt(respuesta[0])
                print("\nPrimer Lugar: "+respuesta[1])
                print("Obras únicas: "+str(respuesta[5]))
                print("Las primera y últimas obras del primer lugar:\n")
                printResultsArt(respuesta[4],"")
                # nacionalidades=mp.keySet(respuesta)
                # for pais in lt.iterator(nacionalidades):
                #     obras=mp.get(respuesta,pais)
                #     cantidadobras=me.getValue(obras)["Total_obras"]
                #     print(pais,"--- Q obras: ",str(cantidadobras))
        # Opción 0: Salir
        elif int(inputs[0]) == 5:
            tiempoInicial=time.process_time()
            nombreDepartamento=input("\nIngrese el nombre del departamento: ")
            tiempoInicial=time.process_time()
            respuesta=controller.transportarObrasDespartamento(catalog,nombreDepartamento)
            listaObrasDepartamentoPrecio=respuesta[3]
            listaObrasDepartamentoAntiguedad=respuesta[2]
            precioTotal=respuesta[0]
            pesoTotal=respuesta[1]
            sizeLista=respuesta[4]
            if sizeLista>0:
                print("MoMA trasnportará",lt.size(listaObrasDepartamentoPrecio),"obras del departamento de",nombreDepartamento)
                print("\nEl peso total estimado es",str(pesoTotal)+"kg")
                print("El precio estimado de transportar todas las obras del departamento es",str(precioTotal)+"USD")
                
                print("Obras más antiguas")
                printTableTransPricesArtworks(listaObrasDepartamentoAntiguedad," ANTIGUAS ")
                print("Obras más costosas")
                printTableTransPricesArtworks(listaObrasDepartamentoPrecio," COSTOSAS ")
            else:
                print("El departamento",nombreDepartamento,"no existe o no tiene obras registradas.")

        elif int(inputs[0]) == 6:
            tiempoInicial=time.process_time()
            n=int(input("Ingrese el top (#) de artistas más prolíficos: "))
            fechaInicial=int(input("Ingrese el limite inferior del año de nacimiento (AAAA): "))
            fechaFinal=int(input("Ingrese el limite superior del año de nacimiento (AAAA): "))
            resultado= controller.artistasMasProlificos(catalog,fechaInicial,fechaFinal,n)
            printRequerimiento6(resultado,fechaInicial,fechaFinal,n)



        elif int(inputs[0]) == 7:
            sys.exit(0)
        else:
            print("Seleccione una opción válida")
    else:
        print("Seleccione una opción válida")
    input("\nDuración: "+str((time.process_time()-tiempoInicial)*1000)+"ms\nPresione enter para continuar...")
    print("")
sys.exit(0)
