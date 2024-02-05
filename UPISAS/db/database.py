from UPISAS.db.timescale import TimeScaleDB
import psycopg2

class DatabaseInterface(object):
    
    def __init__(self, databaseName):
        global database
        global db

        database = databaseName
        if databaseName == "timescale":
            db = TimeScaleDB()            
        elif(databaseName == "elastic"):
            pass

    def create_table(self, table_name):
        if database == "timescale":
            db.create_table(table_name)
        elif(database == "elastic"):
            
            pass

    def add_exemplar(self,exemplar):
        if database == "timescale":
            db.add_exemplar(exemplar)

        elif(database == "elastic"):
            pass

    def add_run(self,run):
        if database == "timescale":
            db.add_run(run)

        elif(database == "elastic"):
            pass

    def get_exemplar_by_name(self,exemplar_name):
        if database == "timescale":
            db.get_exemplar_by_name(exemplar_name)

        elif(database == "elastic"):
            pass
