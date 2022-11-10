import requests #resuelve peticiones al servidor
import bs4 #
from bs4 import BeautifulSoup #
from urllib.parse import urljoin #para parsear los url
import pandas as pd #genera data Frame con los datos que se recolectan

urlInicial='https://www.filmaffinity.com/ar/cat_new_netflix.html' #url en la que vamos a trabajar
page = requests.get(urlInicial)#descargo el contenido de la pagina

soup=BeautifulSoup(page.text,'lxml')#genero el texto plano de la respuesta que recibi



def linkTodasPginas(pageLink):#consigo el link de todas las paginas de la web filmaffinity
    lista=[]
    for i in range(1, 2):#genero una lista con los LINK DE CADA PAGINA (para pruebas solo los link de las 3 primeras paginas para que no se trabe la pc)
      b=str(i)#paso int a string
      lista.append(pageLink+b)#concateno rootLink con i para generar el string con la direccion https y lo agrego a la lista
    return lista

def linkTodasPeliculas(listaPaginas):#de cada pagina obtengo los link de las peliculas y los agrego a listaPeliculas
    listaPeliculas=[]# en esta lista agrego el link de todas las peliculas
    for i in listaPaginas:#de cada pagina obtengo los link
        page = requests.get(i)  # descargo el contenido de la pagina actual
        soup = BeautifulSoup(page.text, 'lxml')  # genero el texto plano de la respuesta que recibi
        listaLink = soup.find_all('div', class_="movie-title")  # lista de link  de las peliculas y mas informacion
        linkPeliculas=[x.find('a').get('href')for x in listaLink]#lista con los link de las peliculas que hay en la pagina actual

        contador=0
        for j in linkPeliculas:#de la lista obtenida al recorrer la pagina actual extraigo cada link y lo agrego a listaPeliculas
                                #que tiene el link de todas las peliculas de todas las paginas de la web
            listaPeliculas.append(linkPeliculas[contador])
            contador=contador+1
    return listaPeliculas#retorno una lista con los link de peliculas de todas las paginas de filmaffinity
def obtenerDatos(linkPeliculas):#obtener una lista con los titulos de las peliculas
    #diccionarioNetflix = {}
    titulos=list()
    anios=list()
    paises=list()
    directores=list()
    generos=list()

    listaTodos=list()
    diccionarioN=[]
    for i in linkPeliculas:
        lista = list()
        page = requests.get(i)  # descargo el contenido de la pagina actual
        soup = BeautifulSoup(page.text, 'lxml')  # genero el texto plano de la respuesta que recibi
        box=soup.find('dl',class_='movie-info')

        lista.append(obtenerTitulos(box))
        lista.append(obtenerAnio(box))
        lista.append(obtenerPais(box))
        lista.append(obtenerDirector(box))
        lista.append(obtenerGenero(box))
        listaTodos.append(lista)
        """titulos.append(obtenerTitulos(box))
        anios.append(obtenerAnio(box))
        paises.append(obtenerPais(box))
        directores.append(obtenerDirector(box))
        generos.append(obtenerGenero(box))"""
        """diccionarioNetflix['Titulo']=obtenerTitulos(box)#obtengo titulo
        diccionarioNetflix['Anio']=obtenerAnio(box)#obtengo el año
        diccionarioNetflix['Pais']=obtenerPais(box)#obtengo el pais
        diccionarioNetflix['Director']=obtenerDirector(box)#obtengo el director
        diccionarioNetflix['Genero']=obtenerGenero(box)#obtengo el genero
        diccionarioN.append(diccionarioNetflix)"""
    #diccionarioNetflix={'Titulo':titulos,'Anio':anios,'Pais':paises,'Director':directores,'Genero':generos}
    return listaTodos#diccionarioNetflix

def obtenerTitulos(box): # se obtiene titulo
    titulo = box.find('dd') # se obtiene titulo
    if titulo==None:#si no hay titulo cargado
        titulo="Sin Datos"
    else:
        titulo=titulo.get_text().strip()  # se convierte el titulo a texto y se le quitan los espacios

    return titulo
def obtenerAnio(box):# se obtiene año
    anio = box.find('dd', itemprop='datePublished')  # se obtiene año
    if anio==None:#si no hay año cargado
        anio="Sin Datos"
    else:
        anio=anio.get_text()#se convierte el año a texto

    return anio
def obtenerPais(box): # se obtiene pais
    pais = box.find('img').get('alt')  # se obtiene pais
    if pais==None:#si no hay pais cargado
        pais=="Sin Datos"

    return pais
def obtenerDirector(box): # se obtiene el director
    director = box.find('span', itemprop='name')
    if director == None:#si no hay director cargado
        director = "Sin Datos"
    else:
        director = director.get_text()#se convierte director a texto
    return director
def obtenerGenero(box):#obtengo genero
    genero=box.find('span',itemprop='genre')
    genero=genero.find('a')
    if genero==None:#si no hay genero cargado
        genero="Sin Datos"
    else:
        genero=genero.get_text()#se convierte el genero a texto

    return genero
pageLink="https://www.filmaffinity.com/ar/category.php?id=new_netflix&page="#link utilizado para generar el link de todas las paginas de filmaffinity
listaPaginas=linkTodasPginas(pageLink)#obtengo el link de todas las paginas
linkPeliculas=linkTodasPeliculas(listaPaginas)#obtengo el link de todas las peliculas

diccionario=obtenerDatos(linkPeliculas)
#rint(diccionario)
dfCatalogo=pd.DataFrame(diccionario,columns=['Titulo','Anio','Pais','Director','Genero'])
#print(dfCatalogo)
dfCatalogo.to_csv('webScrapingNetflix.csv')


