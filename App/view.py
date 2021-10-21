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
    print("0 - Cargar catálogo")
    print("1 - Listar cronológicamente los artistas")
    print("2 - Listar cronológicamente las adquisiciones")
    print("3 - Clasificar las obras de un artista por técnica")
    print("4 - Clasificar las obras por la nacionalidad de sus creadores")
    print("5 - Transportar obras de un departamento")
    print("6 - Artistas más prolíficos")
    print("7 - Salir")

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

def printRequerimiento1(resultado):
    if resultado[2]["size"] > 0:

        maxWidth= {"ConstituentID":7,"DisplayName":15, "BeginDate":8,
                    "Nationality":15,"Gender":12, "ArtistBio":15,"Wiki QID":10,"ULAN":15}

        fieldNames= ["ConstituentID","DisplayName","BeginDate","Nationality",
                    "Gender","ArtistBio","Wiki QID","ULAN"]

        keys= ["ConstituentID","DisplayName","BeginDate","Nationality",
                            "Gender","ArtistBio","Wiki QID","ULAN"]


        print("\nEl total de artistas en este rango de fechas ("+fechaInicial+" - "+fechaFinal+") es: "+str(resultado[1]))
        print("\nLos 3 primeros y últimos artistas del rango se registran en la siguiente tabla:")

        printPrettyTable(resultado[2],keys,fieldNames,maxWidth,sample=3,ultimas=True)

    else:
        print("\nNo  existe ninguna obra en las base de datos que haya sido registrada entre",fechaInicial,"y",fechaFinal,
        "o las fechas ingresadas no siguen el formato correcto.")
    controller.limpiarVar(resultado) #Se borra el resultado - Dato provisional

def printRequerimiento2(resultado):
    if resultado[2] > 0:

        maxWidth={"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                            "Dimensions":15,"Date":12,"DateAcquired":11,"URL":10}
        fieldNames= ["ObjectID","Title","Artists Names","Medium",
                            "Dimensions","Date","DateAcquired","URL"]

        keys= ["ObjectID","Title","ArtistsNames","Medium",
                            "Dimensions","Date","DateAcquired","URL"]
        
        print("\nEl total de obras en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[2]))
        print("\nEl total de artistas para la obras seleccionadas en el rango: "+str(resultado[3]))
        print("\nEl total de obras compradadas ('Purchase') en el rango de fechas "+fechaInicial+" - "+fechaFinal+" es: "+str(resultado[1]))
        print("\nLas tres primeras y tres ultimas obras del rango se registran en la siguiente tabla:")

        printPrettyTable(resultado[0],keys,fieldNames,maxWidth,sample=3,ultimas=True)

    else:
        print("\nNo  existe ninguna obra en las base de datos que haya sido registrada entre",fechaInicial,"y",fechaFinal,
        "o las fechas ingresadas no siguen el formato correcto.")
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

def printRequerimiento4(respuesta):
    #TOP10
    print("\n Top 10 países por obras")
    print("\n Total países: " + str(respuesta[3]))
    field_names1=["Nationality","ArtWorks"]
    max_width1 = {"Nationality" : 15, "ArtWorks" : 5}
    keys1=["Nacionalidad","Total_obras"]
    printPrettyTable(respuesta[0],keys1,field_names1,max_width1,sample=10)
    #PRIMER LUGAR
    print("\nPrimer Lugar: "+respuesta[1])
    print("Obras únicas: "+str(respuesta[5]))

    field_names=["ObjectID","Title","Artists Names","Medium",
                "Dimensions","Date","DateAcquired","URL"]
    max_width = {"ObjectID" : 10, "Title" : 15,"Artists Names":16,"Medium":13,
                "Dimensions":15,"Date":12,"DateAcquired":11,"URL":10}
    keys=["ObjectID","Title","NombresArtistas","Medium",
        "Dimensions","Date", "DateAcquired","URL"]
    
    print("Las primera y últimas obras del primer lugar:\n")
    printPrettyTable(respuesta[4],keys,field_names,max_width,sample=6)

def printRequerimiento5(respuesta,nombreDepartamento):
    listaObrasDepartamentoPrecio=respuesta[3]
    listaObrasDepartamentoAntiguedad=respuesta[2]
    precioTotal=respuesta[0]
    pesoTotal=respuesta[1]
    sizeLista=respuesta[4]

    field_names=["ObjectID","Title","ArtistsNames","Medium",
                            "Date","Dimensions","Classification","TransCost (USD)","URL"]
    max_width = {"ObjectID" : 10, "Title" : 15,"ArtistsNames":13,"Medium":15,
                            "Date":12,"Dimensions":10,"Classification":11,"TransCost (USD)":11,"URL":10}
    keys=["ObjectID","Title",'NombresArtistas','Medium','Date', 'Dimensions', 'Classification','TransCost (USD)','URL']
    
    print("MoMA trasnportará",sizeLista,"obras del departamento de",nombreDepartamento)
    print("\nEl peso total estimado es",str(pesoTotal)+"kg")
    print("El precio estimado de transportar todas las obras del departamento es",str(precioTotal)+"USD")
    
    print("\nTOP 5 de las obras más antiguas de transportar")
    printPrettyTable(listaObrasDepartamentoAntiguedad,keys,field_names,max_width,sample=5)
    print("\nTOP 5 de las obras más costosas de transportar")
    printPrettyTable(listaObrasDepartamentoPrecio,keys,field_names,max_width,sample=5)



def printRequerimiento6(respuesta,fecha_inicial,fecha_final,n):
    artistas=respuesta[0]
    numArtistas=respuesta[1]
    obrasArtista=respuesta[2]
    if(numArtistas>0):
        print("\n Hay",numArtistas," artistas en el periodo de",str(fecha_inicial),"a",str(fecha_final))
        print("\nLos",str(n),"artistas más prolíficos son:")
        keys=["ConstituentID","DisplayName","BeginDate","Gender","ArtistBio",
                            "Wiki QID","ULAN","ArtworkNumber","MediumNumber","TopMedium"]
        fieldNames=["ConstituentID","DisplayName","BeginDate","Gender","ArtistBio",
                            "Wiki QID","ULAN","ArtworkNumber","MediumNumber","TopMedium"]
        maxWidth = {"ConstituentID":10,"DisplayName":10,"BeginDate":5,"Gender":5,"ArtistBio":10,
                            "Wiki QID":5,"ULAN":10,"ArtworkNumber":5,"MediumNumber":5,"TopMedium":5}
        printPrettyTable(artistas,keys,fieldNames,maxWidth,sample=n,ultimas=False)

        print("\n\nLas cinco primeras obras ordenadas por fecha de adquisición de",lt.getElement(artistas,1)["DisplayName"],"son: \n")

        keys=["ObjectID","Title","Medium","Date","Dimensions",
                            "DateAcquired","Department","Classification","URL"]
        fieldNames=["ObjectID","Title","Medium","Date","Dimensions",
                            "DateAcquired","Department","Classification","URL"]
        maxWidth = {"ObjectID" : 10, "Title" : 15,"Medium":13,
                            "Date":12,"Dimensions":15,"DateAcquired":11,"Department":10,"Classification":10,"URL":10}

        printPrettyTable(obrasArtista,keys,fieldNames,maxWidth,sample=5,ultimas=False)


    else:
        print("\nNo hay artistas en el rango seleccionado")

def printCapacidadesMapas(catalog):
    print("\n"+"*"*50)
    print("*"*10+"Información mapas y listas"+"*"*10)
    print("-"*40+"\n"+">"*5+"Tamaños listas creados"+"<"*5)
    print("Tamaño de LISTA artworks: ",catalog["artworks"]["size"])

    print("-"*40+"\n"+">"*5+"Capacidades y tamaños de los mapas creados"+"<"*5)

    print("Tamaño de mapa artistas: ",catalog["artists"]["size"])
    print("Capacidad final mapa artistas: ",catalog["artists"]["capacity"])
    #DateAcquiredArt
    print("\nTamaño de mapa fechas de adquisición obras: ",catalog["artworks_index_by_year"]["size"])
    print("Capacidad final mapa fechas de adquisición obras: ",catalog["artworks_index_by_year"]["capacity"])
    
    print("\nTamaño de mapa fechas de nacimiento artistas: ",catalog["Artists_BeginDate"]["size"])
    print("Capacidad final mapa fechas de nacimiento artistas: ",catalog["Artists_BeginDate"]["capacity"])
    #artists_index_name
    print("\nTamaño de mapa nombres artistas: ",catalog["artists_index_name"]["size"])
    print("Capacidad final mapa nombres artistas: ",catalog["artists_index_name"]["capacity"])

    print("\nTamaño de mapa nacionalidades: ",catalog["nationalities"]["size"])
    print("Capacidad final mapa nacionalidades: ",catalog["nationalities"]["capacity"])

    print("\nTamaño de mapa deptos museo: ",catalog["Department"]["size"])
    print("Capacidad final mapa deptos museo: ",catalog["Department"]["capacity"])

    print("-"*40)
    print("\n"+"*"*10+"FIN Información mapas y listas"+"*"*10)
    print("*"*50)
"""
Menu principal
"""
while True:
    printMenu()
    tiempoInicial=time.process_time()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs.isnumeric:
        if int(inputs[0]) == 0:
            tiempoInicial=time.process_time()
            print("\nCargando información de los archivos ....")
            catalog=initCatalog()
            loadData(catalog,nArtists=1948,nArtWork=768)
            print("\n\nSe ha completado la carga de artworks y artistas al catálogo")
            printCapacidadesMapas(catalog)
            # print(catalog["artworks_index_by_initial_year"])
            # print(catalog["artworks_index_by_initial_year"]["table"])

        # Caso cuando no hay datos cargados
        elif catalog==None and int(inputs[0])!=7:
            print("\nPara correr la funciones cargue la información primero.")
        
        elif int(inputs[0])==1:
            tiempoInicial=time.process_time()
            fechaInicial=input("\nIngrese el año inicial (AAAA): ")
            fechaFinal=input("\nIngrese el año final (AAAA): ")
            print("\n..Cargando")
            resultado= controller.listarArtistasCronologicamente(catalog, fechaInicial, fechaFinal)
            printRequerimiento1(resultado)

        elif int(inputs[0]) == 2:
            fechaInicial=input("\nIngrese la fecha inicial (AAAA-MM-DD): ")
            fechaFinal=input("\nIngrese la fecha final (AAAA-MM-DD): ")
            tiempoInicial=time.process_time()
            resultado= controller.listarAdquisicionesCronologicamente(catalog, fechaInicial, fechaFinal)
            # try:
            printRequerimiento2(resultado)
            # except:
            #     print(resultado)

        
        elif int(inputs[0]) == 3:
            tiempoInicial=time.process_time()
            nombre=input("Ingrese el nombre del artista: ")
            resultado= controller.tecnicasObrasPorArtista(catalog,nombre)
            printRequerimiento3(resultado,nombre)


            pass
        elif int(inputs[0]) == 4:

            tiempoInicial=time.process_time()
            print("...Cargando top10 de nacionalidades de acuerdo a sus obras ")
            respuesta=controller.clasificarObrasNacionalidad(catalog)
            printRequerimiento4(respuesta)

        # Opción 0: Salir
        elif int(inputs[0]) == 5: ##Implementarlo de la otra forma xd
            tiempoInicial=time.process_time()
            nombreDepartamento=input("\nIngrese el nombre del departamento: ")
            tiempoInicial=time.process_time()
            respuesta=controller.transportarObrasDespartamento(catalog,nombreDepartamento)
            printRequerimiento5(respuesta,nombreDepartamento)

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
