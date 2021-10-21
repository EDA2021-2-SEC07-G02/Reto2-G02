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


from App.controller import buscarNacionalidad
from DISClib.DataStructures.arraylist import isPresent, newList
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import selectionsort as selection
assert cf
import time
import re

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo. Se crea dos mapas/indices, una de ellos para guardar a los artistas, 
    otra para las obras de arte.
    
    Parámetros:
        
    Retorno:
        catalog: Catalogo inicializado
    """
    catalog = {'artists': None,
               'artworks': None,
               "nationalities":None,
               "Department":None,
               "artists_index_name":None,
               "Artists_BeginDate":None}
    
    # catalog["artists"]=lt.newList("ARRAY_LIST",cpmfunction=compareConsIDArtist)

    catalog["artworks"]=lt.newList("ARRAY_LIST",cmpfunction=compareObjectID)

    #Mapas
    catalog['artworks_index_by_year'] = mp.newMap(1000, #Hay aprox 15k de artistas
                                    maptype='CHAINING', #elegir si chaining o probing
                                    loadfactor=4.0)

    catalog['artists'] = mp.newMap(15000, #Hay aprox 15k de artistas
                                   maptype='CHAINING', #elegir si chaining o probing
                                   loadfactor=4.0,
                                   comparefunction=compareConsIDArtist)

    catalog['artists_index_name'] = mp.newMap(15000,
                                   maptype='CHAINING', #elegir si chaining o probing
                                   loadfactor=4.0) # Utilizado para encontrar rapidamente


    catalog['nationalities'] = mp.newMap(250, 
                                   maptype="CHAINING",
                                   loadfactor=4.0,
                                   comparefunction=compareNationality)
    catalog["Artists_BeginDate"] = mp.newMap(331, #Hay 236 fechas únicas,331 numero primo
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareBeginDate)
    catalog["Department"] = mp.newMap(13, #numero primo +5 espacios extras
                                   maptype='CHAINING',
                                   loadfactor=2.0,
                                   comparefunction=compareDepartment)

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
                "Total_obras":0,
                "ObrasUnicas":0}
    nationality["Nationality"]=pais
    nationality["Artworks"]=lt.newList("ARRAY_LIST")
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
    BeginDate["Artistas"]=lt.newList("ARRAY_LIST")
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
    artist["artwork_index_list"]=lt.newList("ARRAY_LIST",cmpfunction=compareObjectID)
    mp.put(catalog['artists'], artist['ConstituentID'], artist)
    mp.put(catalog['artists_index_name'], artist['DisplayName'], artist['ConstituentID'])

    if len(artist["BeginDate"])>1: #Se ignoran si su fecha de nacimiento es vacía (no se añade al mapa de begindate)
        addBeginDate(catalog,artist)

def addArtwork(catalog, artwork):
    """
    Se agrega la obra entregada por parámetro en la última posición de la lista de obras del catalogo.
    Párametros:
        catalog: catalogo de artistas y obras
        artwork: obra de arte a añadir
    Se añade la obra de arte al mapa de artworks,mediums y nationalities
    """
    lt.addLast(catalog["artworks"],artwork)
       
    index=lt.size(catalog["artworks"])
    addDepartment(catalog,artwork,index)
    addArtworkIndexByYear(catalog,artwork)
    addNationality(catalog,artwork,index) #req nacionalidades 

    for consID in artwork["ConstituentID"].strip("[]").replace(" ","").split(","):
        listaIndices=mp.get(catalog["artists"],consID)["value"]["artwork_index_list"] # Req 3 y 6
        lt.addLast(listaIndices,lt.size(catalog["artworks"])) # Añadimos los indices en nuestro mapa para requerirlos en nuestros requerimientos
    

def addArtworkIndexByYear(catalog,artwork):
    """
    Se agrega el indice de artwork al mapa de años
    Párametros:
        catalog: catalogo de artistas y obras
        artwork: obra de arte a añadir
    """
    year=artwork["DateAcquired"].split("-")[0]
    if year.isnumeric():
        year=int(year)
    else:
        year=0
    if mp.contains(catalog["artworks_index_by_year"],year):
        lt.addLast(mp.get(catalog["artworks_index_by_year"],year)["value"],lt.size(catalog["artworks"]))
    else:
        listaIndicesArtwork=lt.newList("ARRAY_LIST")
        lt.addLast(listaIndicesArtwork,lt.size(catalog["artworks"]))
        mp.put(catalog["artworks_index_by_year"],year,listaIndicesArtwork)  


def addBeginDate(catalog,artist): #req 1 MAPA
    """
    Agregar info a mapa fechas de nacimiento
        Párametros:
        catalog: catalogo de artistas y obras
        artist: artista a añadir
    """
    nacimiento=artist["BeginDate"]
    existYear=mp.contains(catalog["Artists_BeginDate"],nacimiento)
    if existYear:
        entry=mp.get(catalog["Artists_BeginDate"],nacimiento)
        yearMap=me.getValue(entry)
    else:
        yearMap=newBeginDate(nacimiento)
        mp.put(catalog["Artists_BeginDate"],nacimiento,yearMap)
    lt.addLast(yearMap["Artistas"],artist["ConstituentID"]) #Se añade solamente el 'ConstituentID'


    
def addNationality(catalog,artwork,index):
    # nacionalidades
    """
    La función agrega la obra entregada por parámetro al mapa de nacionalidades.
    Párametros:
        catalog: catalogo de artistas y obras
        artwork: obra de arte a añadir
    """
    constituentID=artwork["ConstituentID"][1:-1] #se obtiene el constituentID que relaciona una obra con un artista
    codigoNum=constituentID.split(",")
    nacionalidadesObra=lt.newList("ARRAY_LIST")
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
        if lt.isPresent(nacionalidadesObra,nationality)==0:
            lt.addLast(nacionalidadesObra,nationality)
            nationalityMap["ObrasUnicas"]+=1
            lt.addLast(nationalityMap["Artworks"],index) #Se añade solamente el index
        nationalityMap["Total_obras"]+=1
    nacionalidadesObra=None #Se elimina lista provisional

def addDepartment(catalog,artwork,index):
    """
    Agregar info al mapa de departamentos del MOMA
    """
    departamento=artwork["Department"]
    cualidadesobra=index
    existDepartment=mp.contains(catalog["Department"],departamento)
    if existDepartment:
        entry=mp.get(catalog["Department"],departamento)
        departmentMap=me.getValue(entry)
    
    else:
        departmentMap={"Department":departamento,
                        "Artworks":None}
        departmentMap["Artworks"]=lt.newList("ARRAY_LIST")
        mp.put(catalog["Department"],departamento,departmentMap)
    
    lt.addLast(departmentMap["Artworks"],index) #Se añade solamente el index de la obra de arte


# Funciones de consulta

def listarArtistasCronologicamente(catalog,fechaInicialS,fechaFinalS): # Requerimiento Grupal 1: Función Principal
    """
    Requerimiento 2
    La función retorna los artistas nacidos dentro de un rango de fechas.

    Parámetros: 
        catalog: catalogo con obras y artistas
        fechaInicials: fecha inicial ingresada por el usuario
        fechaFinals: fecha final ingresada por el usuario

    Retorno:
        listaNac: lista con todos los artistas nacidos en este rango de fechas
        contador: total de artistas nacidos en este rango de fechas
        respuestaLista: lista con 6 artistas
    """

    listaNac=lt.newList("ARRAY_LIST") #Se crea una nueva lista
    nacimientoKeys=mp.keySet(catalog["Artists_BeginDate"]) #Todos los keys del mapa de años de nacimiento
    contador=0
    fechaInicial=int(fechaInicialS)
    fechaFinal=int(fechaFinalS)
    for fechaStr in lt.iterator(nacimientoKeys):
        fecha=int(fechaStr)
        if fecha>=fechaInicial and fecha<=fechaFinal:
            lt.addLast(listaNac,fecha)
            cantidadArtistas=mp.get(catalog["Artists_BeginDate"],fechaStr)["value"]["Artistas"]["size"]
            contador+=cantidadArtistas
    selection.sortEdit(listaNac,cmpArtistDate,3,ordenarInicio=True,ordenarFinal=True)
    respuestaLista=None
    respuestaLista=listasRespuesta(listaNac,catalog,"Artists","req1")
    return listaNac,contador,respuestaLista


def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal):  # Requerimiento Grupal 2: Función Principal
    """ 
    La función lista cronológicamente las adquisiciones en una rango de tiempo. Selecciona de un mapa de obras, organizando un número
    de obras cercano a de las obras que se mostrarán.

    Parámetros: 
        catalog: catalogo con obras y artistas
        fechaInicial: fecha inicial ingresada por el usuario
        fechaFinal: fecha final ingresada por el usuario
    Retorno:
        lista3Inicio: lista de alrededor de 6 obras
        contadorPurchase: entero que representa las obras compradas (purchase)dentro
        del rango de fechas 
        numeroAdquisiciones: total de obras en el rango de fechas
        numeroArtistas: suma algebraica de artistas en cada obra 
    """

    contadorPurchase=0
    numeroArtistas=0

    yearInitial=int(fechaInicial.split("-")[0])
    yearFinal=int(fechaFinal.split("-")[0])
    year=yearInitial

    yaTengo3Iniciales=False
    yaTengo3Finales=False
    numeroAdquisiciones=0
    
    inicial=time.strptime(fechaInicial,"%Y-%m-%d")
    final=time.strptime(fechaFinal,"%Y-%m-%d")


    lista3Inicio=lt.newList('ARRAY_LIST')
    lista3Final=lt.newList('ARRAY_LIST')

    while year <= yearFinal:

        if mp.contains(catalog["artworks_index_by_year"],year):
            listaArtworkYearIni=mp.get(catalog["artworks_index_by_year"],year)["value"]
            for index_artwork in lt.iterator(listaArtworkYearIni):

                artw=lt.getElement(catalog["artworks"],index_artwork)
                fecha_obra=time.strptime(artw["DateAcquired"],"%Y-%m-%d")
                if inicial<=fecha_obra and final>=fecha_obra:
                    numeroAdquisiciones+=1
                    res=nombresArtistas(catalog,artw["ConstituentID"])
                    artw["ArtistsNames"]=res[0]
                    numeroArtistas+=res[1]
                    if "purchase" in artw["CreditLine"].lower():
                                contadorPurchase+=1
                    if not yaTengo3Iniciales:
                        lt.addLast(lista3Inicio,artw)
        if not yaTengo3Iniciales:
            if lt.size(lista3Inicio)>3:
                yaTengo3Iniciales=True
        year+=1

    yearContrario=yearFinal
    while (yearContrario >= yearInitial) and not yaTengo3Finales:

        if mp.contains(catalog["artworks_index_by_year"],yearContrario):
            listaArtworkYearIni=mp.get(catalog["artworks_index_by_year"],yearContrario)["value"]
            for index_artwork in lt.iterator(listaArtworkYearIni):

                artw=lt.getElement(catalog["artworks"],index_artwork)
                fecha_obra=time.strptime(artw["DateAcquired"],"%Y-%m-%d")
                if inicial<=fecha_obra and final>=fecha_obra:
                    if not yaTengo3Finales:
                        artw["ArtistsNames"]=nombresArtistas(catalog,artw["ConstituentID"])[0]
                        lt.addLast(lista3Final,artw)
        
        if not yaTengo3Finales:
            if lt.size(lista3Final)>=3:
                yaTengo3Finales=True
        yearContrario-=1
    
    lista3Final=sortList(lista3Final,cmpArtworkByDateAcquired)
    lista3Inicio=sortList(lista3Inicio,cmpArtworkByDateAcquired)

    for elementoFinal in lt.iterator(lista3Final):
        lt.addLast(lista3Inicio,elementoFinal)
    
    return lista3Inicio, contadorPurchase, numeroAdquisiciones, numeroArtistas

def nombresArtistas(catalog,consIDs): # Requerimiento 2, 4 y 5: Función Complementaria
    """
    A partir de una cadena con los ConstituenID de cada obra, retorna una cadena con los nombres de los artistas
    Parámetros: 
        catalog: estructura de datos con el catalogo de artistas y obras
        consIDs: constituenID en la base de datos de obras i.e. [2828,2543,9654]
    Retorno:
        resp[:2]: nombres de los artistas separados por comas
        numero_artistas: numero de artistas contados
    """
    numero_artistas=0
    listaConsID=consIDs.strip("[]").replace(" ","").split(",")
    resp=""
    for consID in listaConsID:
        if(mp.contains(catalog["artists"],consID)):
            numero_artistas+=1
            resp+=mp.get(catalog["artists"],consID)["value"]["DisplayName"]+", "
    return resp[:-2],numero_artistas

def tecnicasObrasPorArtista(catalog,nombre): # Requerimiento Individual 3: Función Principal
    """ 
    Clasifica las obras de un artista por técnica dado un nombre
    Parámetros: 
        catalog: estructura de datos con el catalogo de artistas y obras
        nombre: nombre del artista
        sortType: tipo de ordenamiento a utilizar
    Retorno:
        sortedList: lista de técnicas en donde cada elemento es una lista de obras de cada técnica
        totalObras: número total de obras del artista
    """
    constituentID = mp.get(catalog['artists_index_name'],nombre)["value"] # obtiene el constituentID del mapa
    indicesObras = mp.get(catalog['artists'], constituentID)["value"]["artwork_index_list"] # obtiene una lista con los indices de las obras
    obras=lt.newList()
    tecnicas=lt.newList()
    for indiceObra in lt.iterator(indicesObras): # obtiene las obras a partir de las lista de indices
        lt.addLast(obras,lt.getElement(catalog["artworks"],indiceObra))
    for obraArtista in lt.iterator(obras): # se van añadiendo cada obra a una lista con la obras de cada tecnica alojada a su vez en una lista de tecnicas
            encontro=False
            for tecnica in lt.iterator(tecnicas): # busca si la tecnica existe en la lista de tecnicas
                if obraArtista["Medium"] == lt.getElement(tecnica,0)["Medium"]:
                    lt.addLast(tecnica,obraArtista) # si existe la añade la obra a la técnica
                    encontro=True
            if not encontro: # si no existe
                lt.addLast(tecnicas,lt.newList()) # crea una técnica (lista de obras) en la lista de tecnicas
                lt.addLast(lt.lastElement(tecnicas),obraArtista) # añade la lista de obras de esa tecnica
        # sortedList=sortList(tecnicas,cmpFunctionTecnicasArtista,sortType) # utiliza la función de comparación con orden ascendente
    totalObras=lt.size(obras) # retorna el número total de obras
    tecnicas=sortList(tecnicas,cmpFunctionTecnicasArtista)
    return tecnicas,totalObras,lt.getElement(lt.getElement(tecnicas,0),0)["Medium"]
        

def clasificarObrasNacionalidad(catalog): # Requerimiento Individual 4: Función Principal
    """
    Se crea una lista para guardar las nacionalidades que existan del mapa
    junto con su cantidad de obras. Seguido a esto, la lista se ordena con merge sort.
    
    Parámetros:
        catalog: catalogo de obras y artistas
    Retorno:
        top10: Lista con el top10 de nacionalidades, ordenada de mayor a menor
        keyPrimerlugar: Nombre de la nacionalidad del primer lugar
        nationalitiesQ: lista con todas las nacionalidades y la cantidad total de obras que tienen
        sizeNationalitiesQ: total de nacionalidades en el MOMA
        rtaNElementos: lista 6 elementos con obras del primer lugar
        sizeObrasUnicas: total de obras únicas del primer lugar
    """
    nationalitiesQ=lt.newList("ARRAY_LIST") #Se crea una nueva lista
    nationalityKeys=mp.keySet(catalog["nationalities"]) #Todos los keys del mapa de nacionalidades
    for nationality in lt.iterator(nationalityKeys): 
        infoNationality=mp.get(catalog["nationalities"],nationality)["value"]
        infoAdd={"Nacionalidad":nationality,
                "Total_obras":infoNationality["Total_obras"]}
        lt.addLast(nationalitiesQ,infoAdd)
    selection.sortEdit(nationalitiesQ,cmpNationalitiesSize,10,ordenarInicio=True,ordenarFinal=False) #TOP 10
    keyPrimerlugar=lt.getElement(nationalitiesQ,1)["Nacionalidad"]
    top10=lt.subList(nationalitiesQ,1,10)
    sizeNationalitiesQ=nationalitiesQ["size"]

    #Respuesta con 6 obras
    listaObrasPrimerL=mp.get(catalog["nationalities"],keyPrimerlugar)["value"]
    obrasUnicas=listaObrasPrimerL["Artworks"]
    sizeObrasUnicas=listaObrasPrimerL["ObrasUnicas"]
    rtaNElementos=lt.newList("ARRAY_LIST")
    i=1
    n=0
    recorrer=True
    while recorrer: 
        elemento=lt.getElement(obrasUnicas,i)
        obra=lt.getElement(catalog["artworks"],elemento)
        obra["NombresArtistas"]=nombresArtistas(catalog,obra["ConstituentID"])
        lt.addLast(rtaNElementos,obra)
        n+=1
        if n>6 or n>sizeObrasUnicas:
            recorrer=False
        if n==3:
            i=sizeObrasUnicas
        elif n>3:
            i-=1
        else:
            i+=1
    return top10,keyPrimerlugar,nationalitiesQ,sizeNationalitiesQ,rtaNElementos,sizeObrasUnicas


def transportarObrasDespartamento(catalog,departamento): # Requerimiento Grupal 5: Función Principal
    """
    La función indica el precio total de envío que cuesta transportar un departamento. Entrega también una
    lista que contiene las obras que se van a transportar y el precio de transportar cada obra. Los precios
    se establecen de acuerdo a los requerimientos del proyecto.

    Parámetros: 
        catalog: catalogo con obras y artistas
        departamento: nombre del departamento a transportar
    Retorno:
        precioSortedList: lista de obras organizadas por precio (solamente 5 primeras)
        obrasDepartamento: lista de obras organizadas por fecha de antiguedad (solamente 5 primeras)
        precioTotalEnvio: costo total de transportar las obras
        pesoTotal: peso total de las obras
        cantidadDeObras: cantidad de obras a transportar
        obrasArteDepto: todas las obras de este departamento
    """

    # Constantes
    PRECIO_ENVIO_UNIDAD=72
    PRECIO_ENVIO_FIJO=48
    precioTotalEnvio=0
    pesoTotal=0
    exisDepartamento=mp.contains(catalog["Department"],departamento)
    obrasArteDepto=lt.newList("ARRAY_LIST")
    if exisDepartamento:
        obrasDepartamento=mp.get(catalog["Department"],departamento)["value"]["Artworks"] #
        for index in lt.iterator(obrasDepartamento):
            obra=lt.getElement(catalog["artworks"],index)
            obra["NombresArtistas"]=nombresArtistas(catalog,obra["ConstituentID"])[0]
            lt.addLast(obrasArteDepto,obra)
            altura=obra["Height (cm)"]
            ancho=obra["Width (cm)"]
            peso=obra["Weight (kg)"]
            profundidad=obra["Depth (cm)"]
            precioPorPeso=0
            precioPorM2=0
            precioPorM3=0
            #precioPorPeso=PRECIO_ENVIO_UNIDAD/100
            if peso.isnumeric(): #KG   #se comprueba que peso no sea una cadena vacia 
                precioPorPeso=PRECIO_ENVIO_UNIDAD*(float(peso)/100) #if len(peso)>0 else 0
                pesoTotal+=peso
            if altura!="" and ancho!="" and profundidad!="":
                precioPorM3=PRECIO_ENVIO_UNIDAD*(float(altura)/100)*(float(ancho)/100)*(float(profundidad)/100) #if len(peso)>0 else 0
            if altura!="" and ancho!="":
                precioPorM2=PRECIO_ENVIO_UNIDAD*(float(altura)/100)*(float(ancho)/100) #if len(peso)>0 else 0
            
            precioEnvio=max(precioPorM2,precioPorM3,precioPorPeso)
            if precioEnvio==0:
                precioEnvio=PRECIO_ENVIO_FIJO
            obra["TransCost (USD)"]=round(precioEnvio,4)
            precioTotalEnvio+=precioEnvio
    
    size=obrasArteDepto["size"]
    obrasDeptoCopy=lt.subList(obrasArteDepto,0,size) #se copia la lista 
    precioSorted=lt.subList((selection.sortEdit(obrasDeptoCopy,cmpArtworkByPrice,5)),1,5)
    fechaSorted=lt.subList((selection.sortEdit(obrasArteDepto,cmpArtworkByDate,5)),1,5)#lista ordenada por fecha
    respuestaLPrecio=precioSorted#listasRespuesta(precioSorted,catalog,"",requerimiento="req5",elementosTotal=5)
    respuestaLFecha=fechaSorted#listasRespuesta(fechaSorted,catalog,"",requerimiento="req5",elementosTotal=5)
    return precioTotalEnvio, pesoTotal,respuestaLFecha,respuestaLPrecio,size,obrasArteDepto



def artistasMasProlificos(catalog,fecha_inicio,fecha_final,numero_artistas): # Requerimiento Bono 6: Función Única
    """
    Se entrega una lista de los n artista más prolificos, por número de obras y técnicas utilizadas
    Párametros:
        catalog: catalogo de artistas y obras
        fecha_inicio: rango inicial (AAAA)
        fecha_final: limite superior (AAAA)
        numero_artistas: n artistas que se desean mostrar
    Retorno:
        artistasMasProlificos: lista con los n artitas mas prolificos
        numeroArtistasRango: numero de artistas en el rango de fechas
        listaObrasSort: lista organizada de obras del artista más prolifico
    """
    llavesArtistas=mp.keySet(catalog["artists"])
    llavesArtistas=lt.subList(llavesArtistas,0,lt.size(llavesArtistas)) 
    gruposArtistas=lt.newList("ARRAY_LIST")
    numeroMaximo=0

    primerRecorrido=True
    numeroArtistasRango=1

    while numeroMaximo<numero_artistas:
        listaArtistas=lt.newList("ARRAY_LIST")
        maxObras=-1
        contLlaves=1
        for consID in lt.iterator(llavesArtistas):
            artista=mp.get(catalog["artists"],consID)["value"]
            if fecha_inicio<=int(artista["BeginDate"]) and fecha_final>=int(artista["BeginDate"]):
                if(primerRecorrido):
                    numeroArtistasRango+=1
                numero_obras=lt.size(artista["artwork_index_list"])
                if numero_obras>maxObras:
                    maxObras=numero_obras
                    listaArtistas=lt.newList("ARRAY_LIST")
                    artista["ArtworkNumber"]=numero_obras
                    artista["posicionListaLLaves"]=contLlaves
                    lt.addLast(listaArtistas,artista)
                elif numero_obras==maxObras:
                    artista["ArtworkNumber"]=numero_obras
                    artista["posicionListaLLaves"]=contLlaves
                    lt.addLast(listaArtistas,artista)
            contLlaves+=1

        primerRecorrido=False

            
        cont=lt.size(listaArtistas)
        while cont>=1:
            lt.deleteElement(llavesArtistas,lt.getElement(listaArtistas,cont)["posicionListaLLaves"])
            cont-=1



        numeroMaximo+=lt.size(listaArtistas)
        lt.addLast(gruposArtistas,listaArtistas)

    artistasMasProlificos=lt.newList("ARRAY_LIST")

    for listaArtistasG in lt.iterator(gruposArtistas):
        for artista in lt.iterator(listaArtistasG):
            resultado=tecnicasObrasPorArtista(catalog,artista["DisplayName"])

            cantidadTecnicas=lt.size(resultado[0])
            artista["MediumNumber"]=cantidadTecnicas
            artista["ObrasTopMedium"]=lt.firstElement(resultado[0])
            artista["TopMedium"]=resultado[2]

        listaArtistasSorted=sortList(listaArtistasG,cmpCantMedios)
        for artistaS in lt.iterator(listaArtistasSorted):
            lt.addLast(artistasMasProlificos,artistaS)
        
    
    if lt.size(artistasMasProlificos)>numero_artistas:
        artistasMasProlificos=lt.subList(artistasMasProlificos,1,numero_artistas)

    listaIndicesObras=lt.getElement(artistasMasProlificos,1)["artwork_index_list"]

    obrasArtista=lt.newList("ARRAY_LIST")
    for indexObra in lt.iterator(listaIndicesObras):
        lt.addLast(obrasArtista,lt.getElement(catalog["artworks"],indexObra))
    
    listaObrasSort=sortList(obrasArtista,cmpArtworkByDateAcquired)
    
    return artistasMasProlificos, numeroArtistasRango, listaObrasSort

#Funciones de comparación

def cmpFunctionTecnicasArtista(tecnica1,tecnica2): 
    """ 
    Compara dos técnicas por su cantiadad de obras
    Parámetros: 
        tecnica1: lista de obras de una tecnica
        tecnica2: lista de obras de otra tecnica
    Retorno:
        retorna verdader (True) si la lista tecnica 1 tiene más elementos que la lista de la tecnica 2
    """
    if lt.size(tecnica1)>lt.size(tecnica2): # comparación con orden ascendente
        return True
    else:
        return False

def cmpCantMedios(artista1,artista2): 
    return artista1["MediumNumber"]>artista2["MediumNumber"]


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

def cmpArtworkByDate(obra1,obra2): 
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

def compareConsIDArtist(consIDArtist, entry):
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

def cmpADateAcquired(date1,date2): 
    """"
    cmp en fechas de adquisición
    """
    fecha1=time.strptime(date1,"%Y-%m-%d")
    fecha2=time.strptime(date2,"%Y-%m-%d")
    return fecha1<fecha2

def cmpADateAcquiredObra(artwork1,artwork2): 
    """
    cmp obra[DateAcquired]
    """
    fecha1=time.strptime(artwork1["DateAcquired"],"%Y-%m-%d")
    fecha2=time.strptime(artwork2["DateAcquired"],"%Y-%m-%d")
    return fecha1<fecha2

def cmpArtworkByDateAcquired(artwork1, artwork2): 
    """ 
    Compara las fechas de dos obras de arte
    Parámetros: 
        artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
        artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    Retorno:
        Devuelve verdadero (True) si artwork1 es menor en fecha que artwork2, si tienen la misma 
        fecha retorna falso (False)
    """
    pattern = re.compile("[0-9][0-9][0-9][0-9]-([1][0-2]|[0][1-9])-([3][1]|[0-2][0-9])")
    if pattern.match(artwork1["DateAcquired"]):
        fecha1=time.strptime(artwork1["DateAcquired"],"%Y-%m-%d")
    else:
        fecha1=time.strptime("0001-01-01","%Y-%m-%d")
    if pattern.match(artwork2["DateAcquired"]):
        fecha2=time.strptime(artwork2["DateAcquired"],"%Y-%m-%d")
    else:
        fecha2=time.strptime("0001-01-01","%Y-%m-%d")
    comparacion=fecha1<fecha2
    return comparacion

def compareObjectID(ObjectID, entry): 
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

def compareDepartment(Department, entry):
    """
    Compara dos departamentos del museo.
    Department es un identificador y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if Department == identry:
        return 0
    elif Department > identry:
        return 1
    else:
        return -1


def cmpArtworkByPrice(obra1,obra2): 
    """
    Función de comparación por el costo de transporte de artworks.
    Parámetros:
        obra1: primera obra, contiene el valor "TransCost (USD)"
        obra2: segunda obra, contiene el valor "TransCost (USD)"
    Retorno:
        True si la obra1 tiene un costo en USD mayor que la obra2
    """
    return obra1["TransCost (USD)"]>obra2["TransCost (USD)"] # orden descendentes



def compareBeginDate(Date, entry): 
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

def cmpArtistDate(fecha1,fecha2):  
    """
    Compara la fecha de nacimiento
        Devuelve verdadero (True) si fecha1 es menor en fecha que fecha2, de lo contrario (False)
    """
    return fecha1<fecha2

def cmpArtistaDateRespues(artist1,artist2):
    """
    Cmp para ordenar los artistas de la lista pequeña de respuesta del req 1
    """
    return artist1["BeginDate"]<artist2["BeginDate"]
# Funciones de ordenamiento 

def sortList(lista,cmpFunction,sortType=3):
    """
    ####### FUNCIÓN MODIFICADA PARA HACER PRUEBAS #####
    Función de ordenamiento que se usará en distintos requerimientos dependiendo
    del ordenamiento deseado
    Parámetros: 
        lista: lista que se ordenara
        cmpFunction: función de comparación
        sortType: tipo de ordenamiento (1)Insertion - (2)Selection - (3)Merge - (4)Quick
    Retorno:
        lista ordenada por insertion
    """
    if sortType == 1:
        sorted_list= selection.sort(lista,cmpFunction) 
    elif sortType == 2:
        sorted_list= sa.sort(lista,cmpFunction)
    elif sortType == 3:
        sorted_list= ms.sort(lista,cmpFunction)
    else:
        sorted_list= ms.sort(lista,cmpFunction)
    return sorted_list

# Funciones complementarias

def listasRespuesta(lista,catalog,seccionCatalogo,requerimiento,elementosTotal=6,ordenarSoloInicio=True): ##Borrar después xd o modificar xd
    """
    FUNCIÓN COMPLEMENTARIA REQ 1
    La función buscará los n primeros y últimos elementos de una lista,
    los cuales se guardarán en una nueva array list que será usadada para
    mostrar resultados al usuario en el view.
    Parámetros:
        lista
        catalog
        elementosTotal=6
        seccionCatalogo: artists o artworks #'artists',
                                            'artworks' 
        requerimiento: se agregará info a los elementos dependiendo del requerimiento
    """
    listaRespuesta=lt.newList("ARRAY_LIST")
    n=0
    pos=1
    recorrer=True
    mitad=elementosTotal//2
    precioTransporte=0
    while recorrer:
        elemento=lt.getElement(lista,pos)
        artistasLista=mp.get(catalog["Artists_BeginDate"],str(elemento))["value"]["Artistas"]
        for artista in lt.iterator(artistasLista):
            if pos==0:
                pos=lista["size"]

            if n==mitad and pos==1: #Para no quedarse solamente en el primer año en caso de que tenga muchos artistas
                #print("NO MORE",artista,n)
                break
            elif n>=elementosTotal:
                #print("NO MORE END",artista,n)
                recorrer=False
                break
            else:
                artista=mp.get(catalog["artists"],artista)["value"]
                lt.addLast(listaRespuesta,artista)
                n+=1

        if n>elementosTotal or n>lista["size"]:
            recorrer=False
        if n<mitad:
            pos+=1
        elif n==mitad:
            pos=lista["size"]
        else:
            pos-=1
    selection.sortEdit(listaRespuesta,cmpArtistaDateRespues,3,ordenarInicio=False,ordenarFinal=True)
    return listaRespuesta


def contarTiempo(start_time,stop_time): # TODO: Esto también creo que debe ir en el controlador
    
    elapsed_time_mseg = (stop_time - start_time)*1000
    respuestaTexto="el tiempo (mseg) es: "+str(elapsed_time_mseg)
    return elapsed_time_mseg,respuestaTexto

def limpiarVar(dato):
    """
    Esta función limpia cualquier tipo de dato que tenga como párametro de entrada.
    Se utilizará cuando el programa este ejecutando datos provisionales que no necesiten
    ser guardados, esto con el objetivo de optimizar el uso de memoria ram.
    Parámetros:
        dato: Dato de cualquier tipo (str, listas, entre otros)
    Retorno:
        dato: Dato en None
    """
    dato=None
    return dato

