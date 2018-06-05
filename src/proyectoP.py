#!/usr/bin/python
import requests
import urllib2
import smtplib
import socket
import os
import sys
import commands
import threading
import time
import pyping
import psycopg2
import re
#import pg
headers = {'user-agent': "UNAMCERT-botv1"}

def servicios(url,texto):
	var1=re.findall('<meta name=\"generator\" content=\".*\"',texto)
	if var1!=[]:
		print(var1[0].split(">")[0].split("\""[3]))



def inserta_bd_dominio(curl,url):
	conn = psycopg2.connect("dbname=monitoreo user=root password=hola123")
	cur = conn.cursor()
	if "132.247." in url:
		ip="247"
	else:
		ip="248"
	if curl=="no":
		cmd = "INSERT INTO dominio(nombre,ip,segmento) VALUES ('%s','%s','132.%s.0.0/24');" % ("null",url,ip)
	else:
		cmd = "INSERT INTO dominio(nombre,ip,segmento) VALUES ('%s','%s','132.%s.0.0/24');" % (curl,url,ip)
	cur.execute(cmd)
	conn.commit()
	cur.close()
	conn.close()

def subdominios(url):
	print(url)
	fecha='date'
	fecha=commands.getoutput(fecha)
	curl='curl https://api.hackertarget.com/reverseiplookup/?q='+url+' -s'
	curl=commands.getoutput(curl)
#	print(url)
#	print(curl)
#	print(fecha)
	if "132.247." in url:
		print("247")
	else:
		print("248")
	if curl.find("No DNS") < 0 and len(curl) > 0:
		for x in curl.split("\n"):
			print(x)
			peticiones(url,x)
#			f1 = open(url+'/'+x+'.txt','w')
#			f1.write(texto)
#			f1.close()
			inserta_bd_dominio(curl,url)
	elif len(curl) == 0:
		peticiones(url,fecha)
#		f1 = open(url+'/'+fecha+'.txt','w')
#		f1.write(texto)
#		f1.close()
		inserta_bd_dominio("no",url)
#	servicios(url,texto)

def archivos(url,puerto,texto,nombre):
	print(url)
	directorio='mkdir '+url
	commands.getoutput(directorio)
	f1 = open(url+'/'+nombre+'.txt','w')
	f1.write(texto)
	f1.close()

def peticiones(url,nombre):
	nmap='nmap '+ url +' -p 80 | grep -i "80"'
	nmap=commands.getoutput(nmap)
	if nmap.find("open") >=0:
		try:
			req = requests.get("http://"+url,headers,verify=False)
			if req.status_code==200:
				archivos(url,str(80),req.text,nombre)
		except:
			print("No hay servicio HTTP")
	nmap='nmap '+ url +' -p 443 | grep -i "443"'
	nmap=commands.getoutput(nmap)
	if nmap.find("open") >=0:
		try:
			req = requests.get("https://"+url,headers,verify=False)
			if req.status_code==200:
				archivos(url,str(443),req.text,nombre)
		except:
			print("No hay servicio HTTPS")



def ping_funcion(j):
	for i in range(247,249):
		for m in range(0,4):
			val=j+80*m
			if val > 255:
				break
			for k in range(1,256):
				url="132."+str(i)+"."+str(val)+"."+str(k)
#				ping='ping '+url+ ' -i .05 -w 100 -c 1 -l 10 | grep -i "ttl"'
				ping='fping '+url+ ' -t100'
		#		print(url)
				ping=commands.getoutput(ping)
#				if len(ping) !=0:
				if ping.find("alive") >= 0:
				#	print("asdasdasd")
					subdominios(url)
				#print(url)

	

def inicial():
	t=[j for j in range(1,81)]
	print(t[0])
	for j in range(1,81):
		t[j-1]=threading.Thread(target=ping_funcion,args=(j,))
		t[j-1].start()

#k=0;
#while k<2
#	time.sleep(1)
#	k=k+1
#a=urlparse.urlparse("132.148.10.143")
#b=a.hostname.split(".")[0]
inicial()





