import tasadorbot2 as tb
import math
import pymysql as mysql
import math
from math import radians, sin, cos, acos, asin,pi,sqrt
from datetime import datetime, timedelta, date
past = datetime.now() - timedelta(days=90)
past=datetime.date(past)
yesterday = datetime.now() - timedelta(days=3)
yesterday=datetime.date(yesterday)
import googleMapApi as gm
import propManager as pm
import sys
import sendMailTasacion as sm



def actualizarActividad():

    sql = "UPDATE pedidos SET activo=0 WHERE activo=1"

    mariadb_connection = mysql.connect(user='root', password='sergei', host='127.0.0.1', database='railstest')
    cur = mariadb_connection.cursor()
    cur.execute(sql)
    mariadb_connection.commit()
    mariadb_connection.close()

def actualizarMail():

    sql = "UPDATE pedidos SET mail='0' WHERE mail='sergei@bullestate.cl'"

    mariadb_connection = mysql.connect(user='root', password='sergei', host='127.0.0.1', database='railstest')
    cur = mariadb_connection.cursor()
    cur.execute(sql)
    mariadb_connection.commit()
    mariadb_connection.close()

def tasacion():
    mariadb_connection = mysql.connect(user='root', password='sergei', host='127.0.0.1', database='railstest')
    cur = mariadb_connection.cursor()
    sql = "SELECT operacion,tipo,sup_util,superficie,dorms,bano,estacionamiento,direccion,comuna,nombre,mail,region,piso,anio,constr,terreno,privado FROM pedidos WHERE activo=1"
    cur.execute(sql)
    tasacion=cur.fetchall()
    return tasacion
tasacion=tasacion()
actualizarMail()
tasacion=tasacion[0]
direccion = tasacion[7]
strminmet="Superficie Útil"
strmaxmet="Superficie Total"
strpiezas="Dormitorios"
minmet=tasacion[2]
maxmet=tasacion[3]
piezas=tasacion[4]
estacionamientos=tasacion[6]


if tasacion[14] is not None:

    minmet=tasacion[14]

    maxmet=tasacion[15]

    strminmet="Superficie Construida"
    strmaxmet="Superficie Terreno"
    estacionamientos=1
if tasacion[4] is None:
    piezas=tasacion[16]
    strpiezas="privados"

lat,lon = gm.getCoordsWithAdress(direccion)

precio,nivel,nrcomp,links=tb.calcularTasacion(tasacion[0],tasacion[1],float(lat),float(lon),float(minmet),float(maxmet),int(piezas),int(tasacion[5]),int(estacionamientos))


actualizarActividad()


sm.sendMail(tasacion,precio,nivel,nrcomp,minmet,maxmet,piezas,strminmet,strmaxmet,strpiezas)




