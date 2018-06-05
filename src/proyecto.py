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
headers = {'user-agent': "UNAMCERT-botv1"}

def archivos(url,puerto,texto):
	f1 = open(url+'_'+puerto+'.txt','w')
	f1.write(texto)
	f1.close()
	curl='curl https://api.hackertarget.com/reverseiplookup/?q='+url
	curl=commands.getoutput(curl)
	print(url)
	print(curl)
	if curl.find("No DNS") < 0:
		print(curl)


def peticiones(url):
	nmap='nmap '+ url +' -p 80 | grep -i "80"'
	nmap=commands.getoutput(nmap)
	if nmap.find("open") >=0:
		try:
			req = requests.get("http://"+url,headers,verify=False)
			if req.status_code==200:
				archivos(url,str(80),str(req.text))
#				print(url)
#				print(req.text)
#				print("abierto puerto 80 y activo")
		except:
			print("No hay servicio HTTP")
	nmap='nmap '+ url +' -p 443 | grep -i "443"'
	nmap=commands.getoutput(nmap)
	if nmap.find("open") >=0:
		try:
			req = requests.get("https://"+url,headers,verify=False)
			if req.status_code==200:
				archivos(url,str(443),str(req.text))
#				print(url)
#				print(req.text)
#				print("abierto puerto 443 y activo")
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
				ping=commands.getoutput(ping)
#				print(url)
#				if len(ping) !=0:
				if ping.find("alive") >= 0:
#					print(url + "rango bueno")
#					print("1111111111111111111111111111111111111111")
#					print(ping)
					peticiones(url)

	

def inicial():
	t=[j for j in range(1,81)]
	print(t[0])
	for j in range(1,81):
		t[j-1]=threading.Thread(target=ping_funcion,args=(j,))
		t[j-1].start()





inicial()



