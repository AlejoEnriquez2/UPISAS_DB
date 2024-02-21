from UPISAS.exemplar import Exemplar
from UPISAS.exemplars.swim import SWIM
from UPISAS.strategies.swim_strategy import SwimStrategy
from UPISAS.database.test_elastic_search import ElasticsearchDB
# from UPISAS.database import database
import signal
import time
import sys
from datetime import datetime
import uuid


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exemplar.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if _name_ == '_main_':
    # Instantiate the ElasticsearchDB
    db = ElasticsearchDB()
    ##db = database.create_database('elastic')

    # Create the indexes if they don't exist
    db.create_index('exemplar')
    db.create_index('run')

    try:
        exemplar = SWIM(auto_start=True)
        exemplar.start_run()
        time.sleep(5)
        print('swim started')
        strategy = SwimStrategy(exemplar)

        strategy.get_monitor_schema()
        strategy.get_adaptation_options_schema()
        strategy.get_execute_schema()
        time.sleep(5)
        strategy.get_adaptation_options()
        print('Get adaptation options...done')

        # Get the class name in lowercase
        exemplar_name = exemplar._class.name_.lower()

        # Check if the Exemplar document already exists
        ### 
        try:
            # look for the Exemplar document in the database if not create a new exemplar id
            exemplar_id = db.get_exemplar_id(exemplar_name)
            exemplar_doc = db.get_document('exemplar', exemplar_id)
            
        except:
            # If not, create a new Exemplar document
            exemplar_doc = {
                'name': exemplar_name,
                'monitor_schema': strategy.knowledge.monitor_schema,
                'execute_schema': strategy.knowledge.execute_schema,
                'adaptation_options_schema': strategy.knowledge.adaptation_options_schema,
                'runs': []
            }
            response = db.store_document('exemplar', exemplar_doc)
            exemplar_id = response['_id']
        
        ####
        
        execute_data = {"server_number": 2, "dimmer_factor": 0.5}
        print(f"Exemplar document found: {exemplar_doc}")
        for i in range(2):
            try:
                time.sleep(5)
                adaptive_time_start = time.time()
                strategy.monitor()
                if strategy.analyze():
                    if strategy.plan():
                        strategy.execute(execute_data)
                        adaptive_time_end = time.time()
                        

                        # Save the Run document
                        run_doc = {
                            'adaptive_time': adaptive_time_end - adaptive_time_start,
                            'exemplar_id': exemplar_id,
                            'monitor_data': strategy.knowledge.monitored_data,
                            'analysed_data': strategy.knowledge.analysis_data,
                            'adaptation_options': strategy.knowledge.adaptation_options,
                            'plan_data': strategy.knowledge.plan_data,
                            'execute_data': execute_data,
                            'timestamp': datetime.now().isoformat(),
                        }

                        # Update the Exemplar document with the new run but make sure it stores both the run and the exemplar
                        try:
                            response = db.store_document('run', run_doc)
                            run_id = response['_id']
                            print(f"run id type: {type(run_id)}")

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
                            continue


            except KeyboardInterrupt:
                print("Keyboard interrupt received. Stopping the program.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    exemplar.stop_container()