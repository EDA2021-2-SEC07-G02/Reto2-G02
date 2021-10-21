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
 """

import config as cf
import model
import csv
import time
#from tqdm import tqdm,trange

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo 

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog,nArtists=6656,nArtWork=15008): #10 pct parámetros

    """
    Carga los artistas y obras al catalogo
    """
    muestra="small"
    #print("*************PRUEBAS CON MUESTRA TAMAÑO "+muestra+" *********")
    loadArtists(catalog,nArtists,muestra)
    loadArtworks(catalog,nArtWork,muestra)


def loadArtists(catalog,nArtists=6656,muestra="small"):

    """
    Carga los artistas en una lista dado un nombre de archivo
    """
    artistsFilename = cf.data_dir + 'MoMA\\Artists-utf8-' +muestra+ '.csv'
    inputFile= csv.DictReader(open(artistsFilename, encoding='utf-8'))
    #bar =tqdm(desc="..Carga artistas: ",total=nArtists)
    start_time = time.process_time()
    for artist in inputFile:
        model.addArtist(catalog, artist)
     #   update_iter=1
     #   bar.update(update_iter)
    stop_time = time.process_time()
    print("Tiempo mapas artists (constituent ID),(BeginDate)",contarTiempo(start_time,stop_time)[1]) #MOD LAB!

def loadArtworks(catalog,nArtWork=15008,muestra="small"):
    """
    Carga las obras en una lista dado un nombre de archivo
    """
    artworksFilename = cf.data_dir + 'MoMA\\Artworks-utf8-' +muestra+ '.csv'
    inputFile= csv.DictReader(open(artworksFilename, encoding='utf-8'))
    #bar =tqdm(desc="..Carga Artworks: ",total=nArtWork)
    start_time = time.process_time()
    for artwork in inputFile:
        model.addArtwork(catalog, artwork)
     #   update_iter=1
     #   bar.update(update_iter)
    stop_time = time.process_time()
    print("Tiempo mapas obras de arte (objectid),(medios),(nacionalidad)",contarTiempo(start_time,stop_time)[1]) #MOD LAB!

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal):
    """
    Retorna a los artistas ordenados cronologicamente de acuerdo a un rango de fechas
    Además del total de artistas en ese rango de fechas
    """
    return model.listarArtistasCronologicamente(catalog,fechaInicial,fechaFinal)

def listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal):
    """
    Retorna a los artistas ordenados cronologicamente de acuerdo a un rango de fechas
    Además del total de artistas en ese rango de fechas
    """
    return model.listarAdquisicionesCronologicamente(catalog,fechaInicial,fechaFinal)

def tecnicasObrasPorArtista(catalog, nombre):
    """
    Retorna las técnicas usadas en obras de acuerdo a un artista en específico, junto al total de obras del
    artista y su técnica más usada y su listado de obras
    """
    return model.tecnicasObrasPorArtista(catalog,nombre)

# TODO: ELiminar, esto era de lab antiguo
# def obrasMasAntiguas(catalog,medio,n):
#     return model.obrasMasAntiguas(catalog,medio,n)

def clasificarObrasNacionalidad(catalog):
    return model.clasificarObrasNacionalidad(catalog)

def buscarNacionalidad(catalog,nacionalidad):
    return model.buscarNacionalidad(catalog,nacionalidad)

def transportarObrasDespartamento(catalog,departamento):
    return model.transportarObrasDespartamento(catalog,departamento)

def artistasMasProlificos(catalog,fecha_inicio,fecha_final,n):
    return model.artistasMasProlificos(catalog,fecha_inicio,fecha_final,n)

def contarTiempo(start_time,stop_time):
    return model.contarTiempo(start_time,stop_time)

def limpiarVar(dato):
    """
    Llama a la función limpiarvar
    """
    return model.limpiarVar(dato)