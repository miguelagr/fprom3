CREATE USER root WITH ENCRYPTED PASSWORD 'hola123';
ALTER USER root WITH SUPERUSER;
CREATE DATABASE monitoreo WITH OWNER root;

CREATE USER user1 WITH ENCRYPTED PASSWORD 'hola123';
CREATE USER user2 WITH ENCRYPTED PASSWORD 'hola123';

\c monitoreo

CREATE TABLE historico(
		idHis SERIAL PRIMARY KEY,
		cambioCo CHAR(1),
		numDetec INT,
		nuevosit CHAR(1),
		elimsit  CHAR(1),
		fecha    TIMESTAMP
);



CREATE TABLE archivo(
		idArchivo SERIAL PRIMARY KEY,
		nombre VARCHAR(30) NOT NULL,
		ubicacion VARCHAR(50) NOT NULL,
		md5 VARCHAR(100) NOT NULL,
		fechaCre TIMESTAMP NOT NULL
);



CREATE TABLE dominio(
		idDominio SERIAL PRIMARY KEY,
		nombre VARCHAR(30),
		ip VARCHAR(15) NOT NULL,
		segmento VARCHAR(20) 
);


CREATE TABLE servicio(
		idServicio SERIAL PRIMARY KEY,
		nombre VARCHAR(30) NOT NULL,
		cms VARCHAR(20)
);

CREATE TABLE DomSer(
		idDominio INT REFERENCES dominio(idDominio),
		idServicio INT REFERENCES servicio(idServicio)		
);


CREATE TABLE top(
		idTop SERIAL PRIMARY KEY,
		idDominio INT REFERENCES dominio(idDominio) NOT NULL
);


CREATE TABLE ArDomHis(
		idArchivo INT REFERENCES archivo(idArchivo),
		idDominio INT REFERENCES dominio(idDominio),
		idHis INT REFERENCES historico(idHis),
		ultimaMod TIMESTAMP,

		CONSTRAINT PKliDomCam PRIMARY KEY(idArchivo, idDominio, idHis, ultimaMod)
);
