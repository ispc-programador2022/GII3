"""
CARRERA: TECNICATURA SUPERIOR DE CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
PROYECTO INTEGRADOR 1
GRUPO: GII3
PROYECTO ALFA
PROFESORA: SILVIA PEROTTI
PROFESOR: HÉCTOR PRADO
COHORTE: 2022

WEBSCRAPING CATALOGO DE NETFLIX
Integrantes del Grupo:
-- Galeano, Gerardo Agustín
-- Guzmán Ma. Lilen
-- Ingaramo Ma. Eugenia

"""


import requests #resuelve peticiones al servidor
from bs4 import BeautifulSoup #se importa libreria beautifilsoup
import pandas as pd #genera data Frame con los datos que se recolectan

urlInicial='https://www.filmaffinity.com/ar/cat_new_netflix.html' #url en la que trabajamos
page = requests.get(urlInicial)#se descarga el contenido de la pagina
soup=BeautifulSoup(page.text,'lxml')#se genera el texto plano de la respuesta recibida



def linkTodasPginas(pageLink):#funcion que consigue el link de todas las paginas de la web filmaffinity
    lista=[]#lista donde se almacenan los link de todas las paginas de la web filmaffinity
    for i in range(1, 2):#genero una lista con los LINK DE CADA PAGINA (para pruebas solo los link de la 1 primer pagina
                        # dado que el poder de máquina donde corremos el scrap es limitado)
      b=str(i)#paso int a string
      lista.append(pageLink+b)#concateno rootLink con i para generar el string "https://www.filmaffinity.com/ar/category.php?id=new_netflix&page="+i
                            # con la direccion https y lo agrego a la lista

    return lista


def linkTodasPeliculas(listaPaginas):#de cada pagina  de listaPaginas se obtienen los link de las peliculas y series y se agregan a listaPeliculas
    listaPeliculas=[]# en esta lista se  agrega el link de todas las peliculas y series
    for i in listaPaginas:#de cada pagina obtengo los link
        page = requests.get(i)  # descarga el contenido de la página actual
        soup = BeautifulSoup(page.text, 'lxml')  # genera el texto plano de la respuesta recibida
        listaLink = soup.find_all('div', class_="movie-title")  # se obtiene la lista de link de las películas y más información
        linkPeliculas=[x.find('a').get('href')for x in listaLink]#de listaLink se obtiene lista con todos los link de las peliculas
                                                                # y series que hay en la página actual

        contador=0
        for j in linkPeliculas:#de la lista obtenida al recorrer la pagina actual se extrae cada link y agrega a listaPeliculas
                                #que tiene el link de todas las peliculas y series de todas las paginas de la web
            listaPeliculas.append(linkPeliculas[contador])
            contador=contador+1
    return listaPeliculas#retorna una lista con los link de peliculas y series de todas las paginas de filmaffinity


def obtenerDatos(linkPeliculas):#obtiene una lista con el titulo, anio, país, director y genero de cada pelicula
                                #de la pagina filmaffinity.com

    listaDatos=list()#se guardan los datos de todas las películas y series

    for i in linkPeliculas:#se recorre la lista que contiene el link de todas las peliculas y series de filmaffinity.com
                           #para obtener titulo, anio, país, director y genero.

        lista = list()#lista para almacenar los datos de la pelicula o serie actual
        page = requests.get(i)  # descarga el contenido de la página actual
        soup = BeautifulSoup(page.text, 'lxml')  # genero el texto plano de la respuesta que recibida
        box=soup.find('dl',class_='movie-info')

        lista.append(obtenerTitulos(box))#obtiene titulo
        lista.append(obtenerAnio(box))#obtiene año
        lista.append(obtenerPais(box))#obtiene país
        lista.append(obtenerDirector(box))#obtiene director
        lista.append(obtenerGenero(box))#obtiene titulo
        listaDatos.append(lista)#a listaDatos que almacena los datos de todas las peliculas y series de filmaffinity.com
                                # se inserta 'lista' que contiene los datos de la pelicula actual

    return listaDatos#contiene los datos de todas las películas y series


def obtenerTitulos(box): # se obtiene titulo de la película o serie
    titulo = box.find('dd') # se obtiene título
    if titulo==None:#si no hay título cargado en filmaffinity.com
        titulo="Sin Datos"
    else:
        titulo=titulo.get_text().strip()  # se convierte el título a texto y se le quitan los espacios

    return titulo


def obtenerAnio(box):# se obtiene año
    anio = box.find('dd', itemprop='datePublished')  # se obtiene año
    if anio==None:#si no hay año cargado en filmaffinity.com
        anio="Sin Datos"
    else:
        anio=anio.get_text()#se convierte el año a texto

    return anio


def obtenerPais(box): # se obtiene pais
    pais = box.find('img').get('alt')  # se obtiene pais
    if pais==None:#si no hay pais cargado en filmaffinity.com
        pais=="Sin Datos"

    return pais


def obtenerDirector(box): # se obtiene el director
    director = box.find('span', itemprop='name')
    if director == None:#si no hay director cargado en filmaffinity.com
        director = "Sin Datos"
    else:
        director = director.get_text()#se convierte director a texto
    return director


def obtenerGenero(box):#obtengo genero
    genero=box.find('span',itemprop='genre')
    genero=genero.find('a')#se obtiene el genero
    if genero==None:#si no hay genero cargado en filmaffinity.com
        genero="Sin Datos"
    else:
        genero=genero.get_text()#se convierte el genero a texto

    return genero


pageLink="https://www.filmaffinity.com/ar/category.php?id=new_netflix&page="#link utilizado para generar el link de todas las paginas de filmaffinity.com
listaPaginas=linkTodasPginas(pageLink)#se obtiene el link de todas las paginas
linkPeliculas=linkTodasPeliculas(listaPaginas)#se obtiene el link de todas las peliculas y series

catalogo=obtenerDatos(linkPeliculas)#se obtienen los datos de todas las películas y series de filmaffinity.com

dfCatalogo=pd.DataFrame(catalogo,columns=['Titulo','Anio','Pais','Director','Genero'])#con la libreria panda se genera el
                                                                                        #dataframe

dfCatalogo.to_csv('grupoGII3_webScrapingNetflix.csv',encoding='utf-8')#se genera el csv



