#!/usr/bin/python
import requests
import urllib2
import smtplib
import socket
import os, os.path as path
import sys
import commands
import threading
import time
import pyping
import psycopg2
import re

dvr=['sony','camera','camara','dvr','axis','axiscommunications','panasonic','mobotix','milestone','jvc','vivotek','y-cam','qnap','arecont','iqeye','pelco','veracity','videotec','fujinon','powerdsine','securityspy']

printer=['printer','impresora','hp laserjet','canon','inkjet','black and white','scanner','xerox','samsung printer','pixma','phaser','versalink','ricoh','cartucho','tinta']

cms=['drupal','joomla','wordpress','magneto','blogger','shopify','bitrix','typo3','squerespace','prestashop']

iis=['IIS','IIS Windows Server']

itwork=['It Works','it works','It works','it Works']

def inserta_bd_dominio(curl,url,texto):
	if "132.247." in url:
		ip="247"
	else:
		ip="248"
	conn = psycopg2.connect("dbname=monitoreo user=root password=hola123")
	cur = conn.cursor()
	cmd = "INSERT INTO dominio(nombre,ip,segmento) VALUES ('%s','%s','132.%s.0.0/24') RETURNING idDominio;" % (curl,url,ip)
	cur.execute(cmd)
	for a in cur.fetchone():
		var=a
	conn.commit()
	cur.close()
	conn.close()
	servicios(url,texto,str(var))

def inserta_db_archivo(nombre,ubicacion,fecha,md5):
	conn = psycopg2.connect("dbname=monitoreo user=root password=hola123")
	cur = conn.cursor()
	cmd = "INSERT INTO archivo(nombre,ubicacion,md5,fechaCre) VALUES ('%s','%s','%s','%s');" % (nombre,ubicacion,md5,fecha)
	cur.execute(cmd)
	conn.commit()
	cur.close()
	conn.close()

def inserta_db_serdom(a,idDominio):
	conn = psycopg2.connect("dbname=monitoreo user=root password=hola123")
	cur = conn.cursor()
	cmd = "INSERT INTO domser(idDominio,idServicio) VALUES (%s,%s);" % (idDominio,a)
	cur.execute(cmd)
	conn.commit()
	cur.close()
	conn.close()


def inserta_db_servicios(nombre,cms,idDominio):
	conn = psycopg2.connect("dbname=monitoreo user=root password=hola123")
	cur = conn.cursor()
	cmd = "INSERT INTO servicio(nombre,cms) VALUES ('%s','%s') RETURNING idServicio;" % (nombre,cms)
	cur.execute(cmd)
	for a in cur.fetchone():
		var=a
	conn.commit()
	cur.close()
	conn.close()
	inserta_db_serdom(var,idDominio)

def servicios(url,texto,idDominio):
	var1=re.findall('<meta name=\"generator\" content=\".*\"',texto)
	cont = 0
	cms2="null"
	if var1!=[]:
		cms2=var1[0].split(">")[0].split("\"")[3]
	if cont == 0:
		for a in dvr:
			if texto.find(a) >= 0:
				inserta_db_servicios("dvr",cms2,idDominio)
				cont = 1
				break
	if cont == 0:
		for a in printer:
			if texto.find(a) >= 0:
				inserta_db_servicios("printer",cms2,idDominio)
				cont = 1
				break
	if cont == 0:
		for a in cms:
			if texto.find(a) >= 0:
				inserta_db_servicios("cms",cms2,idDominio)
				cont = 1
				break
	if cont == 0:
		for a in iis:
			if texto.find(a) >= 0:
				inserta_db_servicios("iis",cms2,idDominio)
				cont = 1
				break
	if cont == 0:
		for a in itwork:
			if texto.find(a) >= 0:
				inserta_db_servicios("it work",cms2,idDominio)
				cont = 1
				break
	if cont == 0:
		inserta_db_servicios("web",cms2,idDominio)

def subdominios(url,puerto):
	fecha='date | cut -d" " -f2,4,5,7'
	fecha=commands.getoutput(fecha)
	fecha=fecha.replace(' ','_')
	try:
		url2="https://www.ip-address.org/reverse-lookup/reverse-ip.php"
		parametros = {'s':url}
		r = requests.post(url2,parametros)
		a=re.findall('[href]*="[htps]*://[a-zA-Z\.0-9]*.unam.mx',r.content)
		if a :
			for b in a:
				dominio=b.split("//")[1]
				peticiones(url,dominio,puerto,fecha,dominio)
		elif len(a)==0:
			peticiones(url,fecha,puerto,fecha,url)
	except:
		print("Verifica tu conexion")

def archivos(url,puerto,texto,nombre,fecha):
	directorio='mkdir '+url
	commands.getoutput(directorio)
	archivo='./'+url+'/'+nombre+'_'+puerto+'.txt'
	f1 = open(archivo,'w+')
	f1.write(texto)
	f1.close()	
	md5='md5sum '+'./'+url+'/'+nombre+'_'+puerto+'.txt'
	md5=commands.getoutput(md5)
	inserta_db_archivo(nombre,url,fecha,md5.split(" ")[0])

def peticiones(url,nombre,puerto,fecha,busqueda):
	try:
		req = 'curl -A "UNAMCERT-botv1" http://'+busqueda+' -k -s'
		codigo = 'curl -A "UNAMCERT-botv1" http://'+busqueda+' -k -I -s'
		req=commands.getoutput(req)
		codigo=commands.getoutput(codigo)
		if codigo.find("200") >=0:
			if req:
				inserta_bd_dominio(busqueda,url,req)
				archivos(url,str(80),req,nombre,fecha)
		req2 = 'curl -A "UNAMCERT-botv1" https://'+busqueda+' -k -s'
		codigo2 = 'curl -A "UNAMCERT-botv1" https://'+busqueda+' -k -I -s'
		req2=commands.getoutput(req2)
		codigo2=commands.getoutput(codigo2)
		if codigo2.find("200") >=0:
			if req2:
				inserta_bd_dominio(busqueda,url,req)
				archivos(url,str(443),req2,nombre,fecha)
	except:
		print("No hay servicio HTTP o HTTPS")



def ping_funcion(j):
	for i in range(248,249):
		for m in range(0,5):
			val=j+60*m
			if val > 255:
				break
			for k in range(1,256):
				url="132."+str(i)+"."+str(val)+"."+str(k)
				nmap='nmap -f '+url+' -p 80,443 --open'
				nmap=commands.getoutput(nmap)
				if nmap.find("80/tcp") >= 0:
					subdominios(url,80)
				if nmap.find("443/tcp") >=0:
					subdominios(url,443)

	

def inicial():
	t=[j for j in range(1,61)]
	print(t[0])
	for j in range(1,61):
		t[j-1]=threading.Thread(target=ping_funcion,args=(j,))
		t[j-1].start()


inicial()





