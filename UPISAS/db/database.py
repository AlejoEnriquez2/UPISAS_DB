from UPISAS.db.timescale import TimeScaleDB
from UPISAS.db.elastic_search import ElasticsearchDB
from UPISAS.db.model.exemplarDB import ExemplarDB
from UPISAS.db.model.runDB import RunDB
from datetime import datetime

class DatabaseInterface(object):
    
    def __init__(self, databaseName):
        global database
        global db

        database = databaseName
        if databaseName == "timescale":
            db = TimeScaleDB()            
        elif(databaseName == "elastic"):            
            db = ElasticsearchDB()

    def create_table(self, table_name):
        if database == "timescale":
            db.create_table(table_name)
        elif(database == "elastic"):
            db.create_index(table_name)            

    def add_exemplar(self, name, monitor_schema, execute_schema, adaptation_options_schema):   
        if database == "timescale":
            exemplarDB = ExemplarDB(name, 
                            monitor_schema, 
                            execute_schema,
                            adaptation_options_schema
                        )
            id = db.add_exemplar(exemplarDB)
            return id

        elif(database == "elastic"):            
            id = db.add_exemplar(name, 
                            monitor_schema, 
                            execute_schema,
                            adaptation_options_schema)
            
            return id

    def add_run(self,tt, exemplar_id, monitored_data, analysis_data, adaptation_options,
                    plan_data,
                    execute_data):
        if database == "timescale":
            run = RunDB(tt, 
                    exemplar_id, 
                    monitored_data, 
                    analysis_data,
                    adaptation_options,
                    plan_data,
                    execute_data
                )
            try: 
                db.add_run(run)
            except Exception as e:
                print(f"An error occurred while storing the run: {e}")                

        elif(database == "elastic"):
            run_doc = {
                        'adaptive_time': tt,
                        'exemplar_id': exemplar_id,
                        'monitor_data': monitored_data,
                        'analysed_data': analysis_data,
                        'adaptation_options': adaptation_options,
                        'plan_data': plan_data,
                        'execute_data': execute_data,
                        'timestamp': datetime.now().isoformat(),
                    }
            try:
                response = db.store_document('run', run_doc)
                run_id = response['_id']
                print(f"run id type: {type(run_id)}")

                # Get document by ID
                exemplar_doc = db.get_document("exemplar", exemplar_id)

                # Add the run_id to the 'runs' list in the exemplar_doc dictionary
                exemplar_doc.setdefault("runs", []).append(run_id)
                
                update_script = {
                    'script': {
                        'source': 'ctx._source.runs.add(params.run_id)',
                        'params': {'run_id': run_id}
                    }
                }

                db.update_document('exemplar', exemplar_id, update_script)

                
            except Exception as e:
                print(f"An error occurred while storing the run and updating the exemplar: {e}")                



    def get_exemplar_by_name(self,exemplar_name):
        if database == "timescale":
            db.get_exemplar_by_name(exemplar_name)

        elif(database == "elastic"):
            pass
