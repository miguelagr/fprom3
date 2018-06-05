#!/usr/bin/python
import os
import requests
import hashlib
import socket
#import plotly

i=0
#hosts=['https://www.unam.mx','https://sadfsda.asdfsadf.as.com','https://ingenieria.unam.mx']
hosts=[]
for host in hosts:
    try:
        req = requests.get(host)
#    ar = open('index.html','w',encoding='utf-8')
        ar = open('base/%i.html'%i,'r')
        hb = hashlib.new("md5")
        hb.update(ar.read())
        ar.close()
        h = hashlib.new("md5")
        h.update(req.content)
        if hb.hexdigest() != h.hexdigest():
            ar = open('base/%i.html'%i,'r')
            ar.write(req.content)
            ar.close()
            print h.hexdigest()
            print "El contenido cambio"
        else:
            print "nada"
#        print req.text.encode('ascii','ignore')
#    ar.write(unicode(req.text,'utf-8').encode('ascii'))
#        ar.write(req.text.encode('ascii','ignore'))

    except Exception as e:
        ar = open('base/%i.html'%i,'w')
#        print req.text.encode('ascii','ignore')
#    ar.write(unicode(req.text,'utf-8').encode('ascii'))
        ar.write("recurso no disponible")
        ar.close()
    i = i + 1


def get_hosts(b1=None,b2=None,b3=None,b4=None):
    ars = locals()
    ip = ''
    for i in ars:
        if not ars[i]:
            ars[i]=range(256)
    for j in ars['b1']:
        for i in ars['b2']:
            for k in ars['b3']:
                for l in ars['b4']:
                    ip = '%s.%s.%s.%s'%(j,i,k,l)
                    yield ip


def Scan(ip,f):
    try:
        print '\n'
        sock = socket.create_connection((ip,80),timeout=0.1)
#        sock.settimeout(None)
        sock.close()
        f.write("%s\n"%ip)
        print 'yes'
        print ip
    except Exception as e:
        print e
        print ip

a = get_hosts(b1=['132'],b2=['248'],b3=['10'])#,b4=['15'])

f = open("ips.5","w")
for i in a:
    Scan(i,f)
f.close() 
#try:
#    sock = socket.create_connection(('132.247.70.15',80),timeout=1)
#    sock.settimeout(None)
#    sock.close()
#except Exception as e:
#    print e
#
# https://websitesetup.org/popular-cms/
