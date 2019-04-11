import requests                 #Llibreria que permet fer peticions HTTP, FTP,...
from lxml import html           #Permet treballar amb documents XML
from bs4 import BeautifulSoup   #Llibreria per analitzar i extreure dades de documents HTML
import pandas as pd     #Paquet per utilizar dataframe
import numpy as np      #Paquet que afegeix una biblioteca de funcions matemàtiques a alt nivell
import csv              #Llibreria per treballar amb arxius .csv

#Emmagatzemem a l'objecte soup el contingut de la web
url = "https://pokemon.fandom.com/es/wiki/Lista_de_Pok%C3%A9mon"
urlsub="https://pokemon.fandom.com"
r=requests.get(url)
soup=BeautifulSoup(r.content,"lxml")

#Obtenim el títol de la web
title = soup.title.string
title=title.split('|')[0]
title=[title]

#Volem obtenir una taula amb tots el Pokémon de cada generació.
#Seleccionarem les dades més representatives:
#id,nom,tipus1,tipus2,generació, descripcio
#Les dades de descripció les agafarem de les subpàgines de cada item

#1.Seleccionem els títols de cada generació
titles=[]
h2s = soup.findAll('h2')
for i in h2s:
    links = i.findAll('a')
    for a in links:
        titles.append(a['title'])
titles.pop()    #Esborrem l'últim element de la llista     

#2.Seleccionem l'id (td dins de cada h2)
trs=soup.findAll('tr')

#Esborrem els 'tr' que no necessitem, i emmagatzemem les seves posicions
#en una llista "indexremove"
indexremove= [0,1,2,3,4,156,157,158,159,260,261,262,263,399,400,401,402,510,
              511,512,513,670,671,672,673,746,747,748,749,836,837,838,839,
              840,841]
for i in sorted(indexremove, reverse=True): 
    del trs[i]

#Comencem a recollir els atributs
ids=[]
noms=[]
tipus1=[]
tipus2=[]
links2=[]
descripcions=[]
comptador=0
generacio=[]
objectes=[]
print("Carregant...")
for i in trs:
        datos=i.findAll('a')
        noms.append(datos[0]['title'])       #Obtenim l'atribut nom
        tipus1.append(datos[1]['title'])     #Obtenim l'atribut tipus1   
        try:
                if(len(datos)>2):
                        tipus2.append(datos[2]['title'])        #Obtenim l'atribut tipus2
                else:
                        tipus2.append(" - ")
        except KeyError:
                tipus2.append(" - ")
        
        #Per motius d'eficiència, es decideix obtenir únicament l'atribut de descripció
        #per a la primera generació de Pokémon, ja que s'ha comprovat que en total el
        #programa trigaria entre 3 i 4 minuts en executar-se.
        
        if (comptador<=150):        
                urldesc=datos[0]['href']
                r2=requests.get(urlsub+urldesc)
                soup2=BeautifulSoup(r2.content,"lxml")
                
                data = soup2.findAll('div',attrs={'class':'mw-content-ltr mw-content-text'})
                for div in data:
                        findp = div.findAll('p')
                        ids.append((findp[0].text)[1:].replace('\n',""))    #Obtenim l'atribut id
                        descripcions.append(findp[2].text)             #Obtenim l'atribut descripcio
                        generacio.append(titles[0])
        else:
                idstr=str(comptador+1)
                ids.append(idstr)
                descripcions.append(" - ")
                n=int(ids[comptador])
                if (n>=151 and n<=251):
                        generacio.append(titles[1])
                elif (n>=252 and n<=386):
                        generacio.append(titles[2])     
                elif (n>=387 and n<=493):
                        generacio.append(titles[3])
                elif (n>=494 and n<=649):
                        generacio.append(titles[4])
                elif (n>=650 and n<=721):
                        generacio.append(titles[5])
                else:
                        generacio.append(titles[6])
        
        comptador=comptador+1        
        objectes.append((ids[comptador-1],noms[comptador-1],tipus1[comptador-1],tipus2[comptador-1],generacio[comptador-1],descripcions[comptador-1]))          
   
        
#3.Les dades de descripció les agafarem de les subpàgines de cada item
pokemon_atributs_coleccio=pd.DataFrame(objectes) #Creem el Dataframe
pokemon_atributs_coleccio.rename(columns={0:'Id',1:'Nombre',2:'Tipo 1',3:'Tipo 2',4:'Generación',5:'Descripción'},inplace=True)
pokemon_atributs_coleccio.to_csv("Llista_Pokemon.csv",index=False,encoding='utf-8')