import sys
sys.path.append("/home/alejo/Documents/SAS/code/UPISAS")
import psycopg2
from UPISAS.db.model.runDB import RunDB
import json
from datetime import datetime

class TimeScaleDB():
    def __init__(self, host='localhost', port=5432, user="admin", password="admin", dbname="dbname"):
        self.conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        self.cur = self.conn.cursor()

    def create_table(self, table_name):
        exemplar_query = """
            CREATE TABLE IF NOT EXISTS exemplar (
            id SERIAL PRIMARY KEY,
            name TEXT,
            monitor_schema json,
            execute_schema json,
            adaptation_options_schema json          
        );
        """
        run_query = """
            CREATE TABLE IF NOT EXISTS run (
            run_id SERIAL PRIMARY KEY,
            run_time NUMERIC(10,10) NOT NULL,
            time TIMESTAMPTZ NOT NULL,
            exemplar_id INTEGER,
            monitor_data json,
            analysed_data json,
            adaptation_options json,
            plan_data json,
            execute_data json,
            FOREIGN KEY (exemplar_id) REFERENCES exemplar (id)
        );
        """

        if table_name == "exemplar":
            self.cur.execute(exemplar_query)
            self.conn.commit()
        elif table_name == "run": 
            self.cur.execute(run_query)    
            self.conn.commit()
        
        #hypertable_query = "SELECT create_hypertable('run', by_range('time'));"
        #self.cur.execute(hypertable_query)
        #self.conn.commit()

    def add_exemplar(self, content):        
        # Check if the exemplar already exists
        # Make name primary key or unique
        self.cur.execute("SELECT id FROM exemplar WHERE name = %s", (json.dumps(content.name),))
        result = self.cur.fetchone()

        # If the exemplar does not exist, insert it
        if result is None:
            self.cur.execute(f"INSERT INTO exemplar (name, monitor_schema, execute_schema, adaptation_options_schema) VALUES (%s, %s, %s, %s)", (json.dumps(content.name), json.dumps(content.monitor_schema), json.dumps(content.execute_schema), json.dumps(content.adaptation_options_schema)))
            self.conn.commit()
            self.cur.execute("SELECT id FROM exemplar WHERE name = %s", (json.dumps(content.name),))
            result = self.cur.fetchone()
        
        # Return status code 
        return result
    
    def add_run(self, content: RunDB):     
        self.cur.execute(f"INSERT INTO run (time, run_time, exemplar_id, monitor_data, analysed_data, adaptation_options, plan_data, execute_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (datetime.now().isoformat(), content.run_time, content.exemplar_id, json.dumps(content.monitor_data), json.dumps(content.analysed_data), json.dumps(content.adaptation_options), json.dumps(content.plan_data), json.dumps(content.execute_data)))
        self.conn.commit()

        # Return status code 
        return content

    def get_exemplar_by_name(self, exemplar_name):
        # Query
        print(exemplar_name)
        self.cur.execute("SELECT id FROM exemplar WHERE name like %s", (json.dumps(exemplar_name.name),))
        result = self.cur.fetchone()
        print(result)
        exemplar_id = None

        # Check if it exists already
        if result is not None:
            exemplar_id = result[0]      
            
        return exemplar_id
    