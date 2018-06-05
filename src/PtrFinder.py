#!/usr/bin/python
#import dns
import socket


#x = list( map( lambda x: x[4][0], socket.getaddrinfo('www.example.com',22)))
for i in socket.getaddrinfo('www.example.com',22):
	print i


with open('ips.1','r') as ips:
    ip = ips.readline()[:-1]
    print ip
    try:
        info = socket.gethostbyaddr('127.0.0.1')
        print info
    except Exception as e:
        print e

#for i in hosts
