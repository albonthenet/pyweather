#!/usr/bin/python

#Interactions with the database
#SQLite integrated with python
import random
import sys
import os
import sqlite3 as dbapi

#DB file name
dbfname = "garden.db"
#Connector object for db handling
bd = None
#DB object
c = None

def connect_db(bd):
    try:
        bd = dbapi.connect(dbfname)
        c = bd.cursor()
        return c
    except dbapi.Error, e:
        print "Error when opening the db connector"
        print "Error %s:" % e.args[0]
        sys.exit(1)

def check_db_existence():
    if os.path.isfile(dbfname):
        print "OK: DB file %s exists" % dbfname
    else:
        try:
            print "ERR: DB %s does not exist" % dbfname
            print "INFO: Creating db: %s" % dbfname
            bd = dbapi.connect(dbfname)
            #As db is new we initialize it
            create_plants_table()
            bd.close()
        except dbapi.Error, e:
            print "Error when opening the db file"
            print "Error %s:" % e.args[0]
            sys.exit(1)

def insert_plant(plant_data):
    #Check that all the fields are completed
    #IMPROVE: check that they contain the matching data .. integer,string,etc
    if (len(plant_data)!=8):
        print "Some required fields in the plant data are empty"
        #Error
        return 1

    bd = dbapi.connect(dbfname)
    c = bd.cursor()
    try:
        #c.execute("INSERT INTO plants VALUES(5555,'rosa','rosa salon',1,'26122014',26,1,0)")
        
        c.execute("INSERT INTO plants(\
        identif,name,description,automan,last_water,humidity,active,drytrigger) \
        VALUES(?,?,?,?,?,?,?,?)",(plant_data[0],plant_data[1],plant_data[2],\
        plant_data[3],plant_data[4],plant_data[5],plant_data[6],plant_data[7]))
        idef = c.lastrowid
        print('Last row id: %d' % idef)
        bd.commit()
    except dbapi.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

#If db does not exist we need to create the table layout for plants
def create_plants_table():
    bd = dbapi.connect(dbfname)
    c = bd.cursor()
    print "hola"
    try:
        c.execute("""create table if not exists plants(
        identif TEXT,
        name TEXT,
        description TEXT,
        automan INTEGER,
        last_water TEXT,
        humidity INTEGER,
        active INTEGER,
        drytrigger INTEGER)""")
    except dbapi.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

def update_plant(idef, plant_data):
    #the argument plant_data provides new info
    bd = dbapi.connect(dbfname)
    c = bd.cursor()
    #For the moment this is a quick dirty function
    #
    if len(plant_data)>0:
        if plant_data[1] != None:
            c.execute("UPDATE plants SET name = ? WHERE identif = ?",\
            (plant_data[1], idef))
        if plant_data[2] != None:
            c.execute("UPDATE plants SET description = ? WHERE identif = ?",\
            (plant_data[2], idef))
        if plant_data[3] != None:
            c.execute("UPDATE plants SET automan = ? WHERE identif = ?",\
            (plant_data[3], idef))
        if plant_data[4] != None:
            c.execute("UPDATE plants SET last_water = ? WHERE identif = ?",\
            (plant_data[4], idef))
        if plant_data[5] != None:
            c.execute("UPDATE plants SET humidity = ? WHERE identif = ?",\
            (plant_data[5], idef))
        if plant_data[6] != None:
            c.execute("UPDATE plants SET active = ? WHERE identif = ?",\
            (plant_data[6], idef))
        if plant_data[7] != None:
            c.execute("UPDATE plants SET drytrigger = ? WHERE identif = ?",\
            (plant_data[7], idef))
        bd.commit()
        print "INFO: Plant profile updated"
    else:
        print "INFO: Nothing to update"
        return 0

def delete_plant(idef):
    bd = dbapi.connect(dbfname)
    c = bd.cursor()
    try:
        c.execute("DELETE FROM plants WHERE identif = ?", (idef,))
        bd.commit()
    except dbapi.Error, e:
        print "Error %s:" % e.args[0]
        return 1
    finally:
        if c:
            c.close()


def show_all_db():
    bd = dbapi.connect(dbfname)
    c = bd.cursor()
    c.execute("SELECT * FROM plants")
    rows = c.fetchall()
    for row in rows:
        print row

def show_plant_info(idef):
    bd = dbapi.connect(dbfname)
    c = bd.cursor()
    try:
        c.execute("SELECT * FROM plants WHERE identif=?", (idef,))
        row = c.fetchone()
        print row
    except dbapi.Error, e:
        print "Error %s:" % e.args[0]
        return 1
    finally:
        if c:
            c.close()


#########################
#   Auxliar functions   #
#########################

def gen_id():
    rand_id = str(random.getrandbits(128))
    return rand_id

check_db_existence()
create_plants_table()

plant_info = (gen_id(),'petunia','petunia bano',None,'26122014',26,1,0)
insert_plant(plant_info)
print "La planta info es: %s"
#show_plant_info('205696501110482921615022265575476797946')
show_all_db()
plant_info_upd =('48779389555133777804475226311630968899','rosemary','olor',\
None,'26122014',26,1,0)
print "y la updateada es.."
update_plant('48779389555133777804475226311630968899',plant_info_upd)
show_all_db()
print "y ahora borramos..."
delete_plant('2056965082921615022265575476797946')
show_all_db()
