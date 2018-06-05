#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
import hashlib
import time
import psycopg2
import sys
import binascii



def genera_bd(fname,tabla,algo):
    """
    Genera la base de datos con todos los hashes de cada cadena de un archivo de entrada
    Argumento:
        Nombre del archivo donde se sacan las cadenas en claro (str)
        Nombre de la tabla (str)
    Salida:
        None
    """
    conn = psycopg2.connect("dbname=root user=root password=hola123.,")
    cur = conn.cursor()
    cmd = "select (LOWER(tablename)) from pg_tables where schemaname like 'public' and tablename like LOWER('%s')" % (tabla)
    cur.execute(cmd)
    if cur.fetchone() is None:
        cur.execute("CREATE TABLE %s (id serial PRIMARY KEY, plain varchar%s);" % (tabla, ', "%s" varchar' * len(algo) % tuple(algo)))
	conn.commit()
                cmd = "INSERT INTO %s(plain, %s) VALUES ('%s', %s);" % (tabla, ('"%s",' * len(algo) % tuple(algo))[:-1], p, ("'%s'," * len(mh) % tuple(mh))[:-1])
                cur.execute(cmd)
                i = f.readline()
	conn.commit()
	cur.close()
	conn.close()

def busca_hash(tabla,digest,algo):
    """
    Busca el texto en claro que corresponde al hash de la entrada
    Argumentos:
        Tabla de busqueda (str)
        Cadena del digest en formato hexadecimal (str)
        Algoritmos posibles para el digest (str[])
    Salida:
        Texto en claro correspondiente al hash de entrada (str[])
    """
    plain = []
    disponibles = []
    conn = psycopg2.connect("dbname=root user=root password=hola123.,")
    cur = conn.cursor()
    cmd = "select (column_name) from information_schema.columns where LOWER(table_name) like LOWER('%s')" % (tabla)

    cur.execute(cmd)
    al = cur.fetchone()
    while al:
        disponibles.append(al[0])
        al = cur.fetchone()
    for i in algo:
        if i in disponibles:
                cmd = "select (tablename) from pg_tables where schemaname like 'public' and tablename like '%s'" % (tabla)
	        cur.execute(cmd)
	        if cur.fetchone():
	            cmd = "SELECT plain FROM %s WHERE %s like '%s'" % (tabla,i,digest)
                    cur.execute(cmd)
	            e = cur.fetchone()
	            if e:
	                plain.append((e[0],digest))
    cur.close()
    conn.close()
    return plain
