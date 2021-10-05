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

def loadData(catalog):

    """
    Carga los artistas y obras al catalogo
    """
    loadArtists(catalog)
    loadArtworks(catalog)

def loadArtists(catalog):

    """
    Carga los artistas en una lista dado un nombre de archivo
    """
    artistsFilename = cf.data_dir + 'MoMA\\Artists-utf8-small.csv'
    inputFile= csv.DictReader(open(artistsFilename, encoding='utf-8'))
    for artist in inputFile:
        model.addArtist(catalog, artist)

def loadArtworks(catalog):
    """
    Carga las obras en una lista dado un nombre de archivo
    """
    artworksFilename = cf.data_dir + 'MoMA\\Artworks-utf8-small.csv'
    inputFile= csv.DictReader(open(artworksFilename, encoding='utf-8'))
    for artwork in inputFile:
        model.addArtwork(catalog, artwork)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def obrasMasAntiguas(catalog,medio,n):
    return model.obrasMasAntiguas(catalog,medio,n)

def clasificarObrasNacionalidad(catalog):
    return model.clasificarObrasNacionalidad(catalog)