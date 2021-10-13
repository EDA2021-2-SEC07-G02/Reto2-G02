"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import newList
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import selectionsort as selection
assert cf
import time

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(mapLab='CHAINING',FactorCarga=4.0):
    # TODO: Documentación return
    """
    Inicializa el catálogo. Se crea dos mapas/indices, una de ellos para guardar a los artistas, 
    otra para las obras de arte.
    
    Parámetros:
        
    Retorno:
        catalog: Catalogo inicializado
    """
    catalog = {'artists': None,
               'artworks': None,
               'mediums':None,
               "nationalities":None}
    
    # catalog["artists"]=lt.newList("ARRAY_LIST",cpmfunction=compareConsIDArtist)
    # catalog["artworks"]=lt.newList("ARRAY_LIST",cpmfunction=compareObjectID)
    #Mapas
    catalog['artists'] = mp.newMap(15000, #Hay aprox 15k de artistas
                                   maptype='CHAINING', #elegir si chaining o probing
                                   loadfactor=4.0,
                                   comparefunction=compareConsIDArtist)

    ##!!!! Creo que no es necesario hacer mapa de artworks
    catalog['artworks'] = mp.newMap(150000, #Hay 138150 obras de arte 
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareObjectID)
    catalog['mediums'] = mp.newMap(1000,
                                   maptype=mapLab,
                                   loadfactor=FactorCarga,
                                   comparefunction=compareMedium)
    catalog['nationalities'] = mp.newMap(300, #hay 232 nacionalidades
                                   maptype=mapLab,
                                   loadfactor=FactorCarga,
                                   comparefunction=compareNationality)
    catalog["Artists_BeginDate"] = mp.newMap(2000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareBeginDate)
    return catalog

def NewNationalityArt(pais):
    """
    Esta funcion crea la estructura de artworks asociados
    a una nacionalidad.
        Parámetros: 
        pais: nacionalidad
    Retorno:
        nacionality: diccionario de la nacionalidad
    """
    nationality={"Nationality":"",
                "Artworks": None,
                "Total_obras":0}
    nationality["Nationality"]=pais
    nationality["Artworks"]=lt.newList()
    return nationality

def newBeginDate(nacimiento):
    """
    Esta funcion crea la estructura de años nacimientos asociados
    a artistas.
        Parámetros: 
        nacimiento: año de nacimiento. Fórmato YYYY
    Retorno:
        nacimiento: diccionario de año nacimiento
    """
    BeginDate={"FechaNacimiento":"",
                "Artistas":None}
    BeginDate["FechaNacimiento"]=int(nacimiento)
    BeginDate["Artistas"]=lt.newList()
    return BeginDate


# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    """
    Se agrega el artista entregado por parámetro en la última posición de la lista de artistas del catalogo.
    Párametros:
        catalog: catalogo de artistas y obras
        artist: artista a añadir
    
    Se añade el artista en mapa 
    """
    mp.put(catalog['artists'], artist['ConstituentID'], artist)
    if len(artist["BeginDate"])==4: #Se ignoran si su fecha de nacimiento es vacía (no se añade al mapa de begindate)
        addBeginDate(catalog,artist)

def addBeginDate(catalog,artist): #req 1 MAPA
    nacimiento=artist["BeginDate"]
    existYear=mp.contains(catalog["Artists_BeginDate"],nacimiento)
    if existYear:
        entry=mp.get(catalog["Artists_BeginDate"],nacimiento)
        yearMap=me.getValue(entry)
    else:
        yearMap=newBeginDate(nacimiento)
        mp.put(catalog["Artists_BeginDate"],nacimiento,yearMap)
    lt.addLast(yearMap["Artistas"],artist["ConstituentID"]) #Se añade solamente el 'ConstituentID'



def addArtwork(catalog, artwork):
    """
    Se agrega la obra entregada por parámetro en la última posición de la lista de obras del catalogo.
    Párametros:
        catalog: catalogo de artistas y obras
        artwork: obra de arte a añadir
    Se añade la obra de arte al mapa de artworks,mediums y nationalities
    """
    mp.put(catalog['artworks'], artwork['ObjectID'], artwork)
    medium =artwork['Medium']  # Se obtienen el medium

    if mp.contains(catalog["mediums"],medium):
        lt.addLast(mp.get(catalog["mediums"],medium)['value'],artwork)
    else:
        lista_inicial=lt.newList()
        lt.addLast(lista_inicial,artwork)
        mp.put(catalog["mediums"],medium,lista_inicial)
    addNationality(catalog,artwork) #req nacionalidades
    
def addNationality(catalog,artwork):
    # nacionalidades
    """
    La función agrega la obra entregada por parámetro al mapa de nacionalidades.
    Párametros:
        catalog: catalogo de artistas y obras
        artwork: obra de arte a añadir
    """
    constituentID=artwork["ConstituentID"][1:-1] #se obtiene el constituentID que relaciona una obra con un artista
    codigoNum=constituentID.split(",")
    objectID=artwork["ObjectID"]
    for ID in codigoNum:
        conID=ID.strip() #se eliminan los espacios en blanco
        existArtist=mp.contains(catalog["artists"],conID)
        nationality="Unknown"
        if existArtist: #se comprueba si el artista existe, de lo contario la nacionalidad queda como "Unknown"
            artist=mp.get(catalog["artists"],conID) #artista con ese ConstituentID
            nationality=me.getValue(artist)["Nationality"] #nacionalidad del artista
            if nationality=="Nationality unknown" or nationality=="":
                nationality="Unknown"

        existNationality=mp.contains(catalog["nationalities"],nationality) #se comprueba si existe esta nacionalidad en el map
        if existNationality:
            entry=mp.get(catalog["nationalities"],nationality)
            nationalityMap=me.getValue(entry)
        else:
            nationalityMap=NewNationalityArt(nationality)
            mp.put(catalog["nationalities"],nationality,nationalityMap)
        lt.addLast(nationalityMap["Artworks"],objectID) #Se añade solamente el objectID, preguntar si es necesario añadir toda la obra de arte
        nationalityMap["Total_obras"]+=1

# Funciones para creacion de datos

# Funciones de consulta

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal):
    listaNac=lt.newList("ARRAY_LIST") #Se crea una nueva lista
    nacimientoKeys=mp.keySet(catalog["Artists_BeginDate"]) #Todos los keys del mapa de años de nacimiento
    contador=0
    for fechaStr in lt.iterator(nacimientoKeys):
        fecha=int(fechaStr)
        if fecha>=fechaInicial and fecha<=fechaFinal:
            lt.addLast(listaNac,fecha)
            cantidadArtistas=mp.get(catalog["Artists_BeginDate"],fechaStr)["value"]["Artistas"]["size"]
            contador+=cantidadArtistas
    print("\nLista de nacimientos sin ordenar\n",listaNac)
    #ms.sort(listaNac,cmpArtistDate)
    print("\nSelection editado! solamente los 10 primeros y últimos lugares \n")
    selection.sortEdit(listaNac,cmpArtistDate,10)
    print(listaNac)
    return listaNac,contador

def obrasMasAntiguas(catalog,medio,n):
    res=""
    if mp.contains(catalog["mediums"],medio):
        lista_a_ordenar=mp.get(catalog["mediums"],medio)['value']
        lista_ordenada=ms.sort(lista_a_ordenar,cmpArtworkByDate)
        cont=1
        for obra in lt.iterator(lista_ordenada):
            res+=str(cont)+". Obra: "+obra["Title"]+"\n"
            res+="Fecha Obra: "+obra["Date"]+"\n\n"
            cont+=1
            if cont>n:
                break
    return res

def clasificarObrasNacionalidad(catalog):
    """
    Se crea una lista para guardar las nacionalidades que existan del mapa
    junto con su cantidad de obras. Seguido a esto, la lista se ordena con merge sort.
    
    Parámetros:
        catalog: catalogo de obras y artistas
    Retorno:
        top10: Lista con el top10 de nacionalidades, ordenada de mayor a menor
        keyPrimerlugar: Nombre de la nacionalidad del primer lugar
    """
    nationalitiesQ=lt.newList("ARRAY_LIST") #Se crea una nueva lista
    nationalityKeys=mp.keySet(catalog["nationalities"]) #Todos los keys del mapa de nacionalidades
    for nationality in lt.iterator(nationalityKeys): 
        infoNationality=mp.get(catalog["nationalities"],nationality)["value"]
        infoAdd={"Nacionalidad":nationality,
                "Total_obras":infoNationality["Total_obras"]}
        lt.addLast(nationalitiesQ,infoAdd)
    #ms.sort(nationalitiesQ,cmpNationalitiesSize)
    selection.sortEdit(nationalitiesQ,cmpNationalitiesSize,10,ordenarInicio=True,ordenarFinal=False)
    keyPrimerlugar=lt.getElement(nationalitiesQ,1)["Nacionalidad"]
    top10=lt.subList(nationalitiesQ,1,10)
    return top10,keyPrimerlugar,nationalitiesQ #nationalitiesQ solamente para lab6, borrar después 

def buscarNacionalidad(catalog,nacionalidad): #Edit laboratorio 6
    obrasNacionalidad=""
    existNationality=mp.contains(catalog["nationalities"],nacionalidad)
    if existNationality:
        obras=mp.get(catalog["nationalities"],nacionalidad)
        cantidadobras=me.getValue(obras)["Total_obras"]
        obrasNacionalidad=str(cantidadobras)
    else:
        obrasNacionalidad="La nacionalidad no existe"
    return obrasNacionalidad

def contarTiempo(start_time,stop_time):
    # start_time = time.process_time()
    # stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    respuestaTexto="el tiempo (mseg) es: "+str(elapsed_time_mseg)
    return elapsed_time_mseg,respuestaTexto
# 
# Funciones utilizadas para comparar elementos dentro de una lista/mapa

# def compareConsIDArtistLT(catalog, ConsIDArtist):  #Función comparación al crear una array_list
#     """
    
#     """
#     if (ConsIDArtist == catalog['Nationality']):
#         return 0
#     else:
#         return -1

# def compareObjectID(catalog, ObjectID):  #Función comparación al crear una array_list
#     """
    
#     """
#     if (ObjectID == catalog['artworks']):
#         return 0
#     else:
#         return -1

def compareMedium(mediumName, entry):
    """
    Compara dos ConstituentID de artistas, consIDArtist es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (mediumName == identry):
        return 0
    elif (mediumName > mediumName):
        return 1
    else:
        return -1

def cmpArtworkByDate(obra1,obra2): # Requerimiento Grupal 5: Función Comparación Ordenamiento
    """
    Función de comparación por fechas de artworks.
    Si alguna de las dos fechas es vacía se toma como valor de referencia el
    entero 2022. Esto se hace con el objetivo de dejar las fechas vacías de 
    últimas al ordenar.
    Parámetros:
        obra1: primera obra, contiene el valor "Date"
        obra2: segunda obra, contiene el valor "Date"
    Retorno:
        True si la obra1 tiene una fecha menor que la fecha2.
        False en el caso contrario.
    """
    fecha1=2022 #año actual +1
    fecha2=2022 
    if len(obra1["Date"])>0:
        fecha1=int(obra1["Date"])
    if len(obra2["Date"])>0:
        fecha2=int(obra2["Date"]) 
    return fecha1<fecha2

def compareConsIDArtist(consIDArtist, entry): #MAPA
    """
    Compara dos ConstituentID de artistas, consIDArtist es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(consIDArtist) == int(identry)):
        return 0
    elif (int(consIDArtist) > int(identry)):
        return 1
    else:
        return -1

def compareObjectID(ObjectID, entry): #MAPA
    """
    Compara dos ObjectID de artworks, ObjectID es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(ObjectID) == int(identry)):
        return 0
    elif (int(ObjectID) > int(identry)):
        return 1
    else:
        return -1

def compareNationality(Nationality, entry):
    """
    Compara dos Nacionalidades de los artistas correspondientes a un artwork, 
    Nacionalidades es un identificador y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if Nationality == identry:
        return 0
    elif Nationality > identry:
        return 1
    else:
        return -1
def compareBeginDate(Date, entry): #MAPA
    """
    Compara dos ObjectID de artworks, ObjectID es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(Date) == int(identry)):
        return 0
    elif (int(Date) > int(identry)):
        return 1
    else:
        return -1
def cmpNationalitiesSize(nacionalidad1,nacionalidad2):
    """
    Función de comparación por cantidad de artworks por nacionalidad.
    """
    return nacionalidad1["Total_obras"]>nacionalidad2["Total_obras"]

def cmpArtistDate(fecha1,fecha2):  # Requerimiento Grupal 1: Función Comparación Ordenamiento
    """
    Compara la fecha de nacimiento
        Devuelve verdadero (True) si fecha1 es menor en fecha que fecha2, de lo contrario (False)
    """
    return fecha1<fecha2
# Funciones de ordenamiento
