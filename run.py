from UPISAS.exemplar import Exemplar
from UPISAS.exemplars.swim import SWIM
from UPISAS.db.model.runDB import RunDB
from UPISAS.db.model.exemplarDB import ExemplarDB
from UPISAS.strategies.swim_strategy import SwimStrategy
from UPISAS.db.database import DatabaseInterface
import time
from datetime import datetime
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exemplar.stop_container()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    # Select the database intended to use 'timescale' or 'elastic'
    db = DatabaseInterface("timescale")
    # db = DatabaseInterface("elastic")
    
    # Create tables of the database, for Elastic they are called index
    db.create_table("exemplar")
    db.create_table("run")
    
    exemplar = SWIM(auto_start=True)

    exemplar.start_run()
    time.sleep(5)
    strategy = SwimStrategy(exemplar)
    
    strategy.get_monitor_schema()
    strategy.get_execute_schema()
    strategy.get_adaptation_options_schema()
    strategy.get_adaptation_options()
    
    time.sleep(5)                
    exemplar_name = exemplar.__class__.__name__.lower()    
    exemplar_id = db.add_exemplar(exemplar_name, 
                            strategy.knowledge.monitor_schema, 
                            strategy.knowledge.execute_schema,
                            strategy.knowledge.adaptation_options_schema)
        
    
    # Execute data parameters, to be obtained with the trained model, 
    # now using dummy data
    execute_data = {"server_number": 2, "dimmer_factor": 0.5}
    flag = True
    while flag:    
        time.sleep(5)
        t1 = time.time()
        strategy.monitor()
        if strategy.analyze():
            if strategy.plan():
                strategy.execute(execute_data)
                t2 = time.time() 
                tt = t2-t1                                
                db.add_run(tt, 
                    exemplar_id, 
                    strategy.knowledge.monitored_data, 
                    strategy.knowledge.analysis_data,
                    strategy.knowledge.adaptation_options,
                    strategy.knowledge.plan_data,
                    execute_data)
        
        # Change here to false if you just want to execute one run
        flag = True

        