#!/usr/bin/python
#UNAM-CERT
import requests
import re
import sys


def analiza_cuerpo(url):
    """
    Analiza las cabeceras recibidas del metodo HEAD al servidor
    Argumentos:
        url (str) : La URL del servidor
        sesion (session) : objeto session
    Salida:
        cms (str) : El CMS utilizado por la pagina
        correos (str)[] : Lista de correos encontrados en la pagina
    """
 
    try:
        respuesta = requests.get(url)
    except Exception as e:
        print e
    try:
        dfmnt = re.findall('((((hacked by|hacked)|hacked-by)|hack)|owned)',respuesta.content,re.I)
        if len(dfmnt) > 0:
            return 1
        else:
            return 0
    except Exception as e:
        print 'No se encontro nada en el cuerpo de la pagina'

print analiza_cuerpo('https://www.unam.mx')


print analiza_cuerpo('https://codepen.io/cr4shcod3/pen/ZKGoVz')
