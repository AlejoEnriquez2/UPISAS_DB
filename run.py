from UPISAS.exemplar import Exemplar
from UPISAS.exemplars.swim import SWIM
from UPISAS.db.model.runDB import RunDB
from UPISAS.db.model.exemplarDB import ExemplarDB
from UPISAS.strategies.swim_strategy import SwimStrategy
from UPISAS.db.database import DatabaseInterface
import time
from datetime import datetime

if __name__ == '__main__':
    # Select the database intended to use 'timescale' or 'elastic'
    db = DatabaseInterface("timescale")
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
    exemplarDB = ExemplarDB(exemplar_name, 
                            strategy.knowledge.monitor_schema, 
                            strategy.knowledge.execute_schema,
                            strategy.knowledge.adaptation_options_schema
                        )
    db.add_exemplar(exemplarDB)
    
    exemplar_id = db.get_exemplar_by_name(exemplarDB)

    flag = True   
    while flag:    
        execute_data = {"server_number": 2, "dimmer_factor": 0.5}
        time.sleep(5)
        t1 = time.time()
        strategy.monitor()
        if strategy.analyze():
            if strategy.plan():
                strategy.execute(execute_data)
                t2 = time.time() 
                tt = t2-t1                
                runDB = RunDB(tt, 
                                exemplar_id, 
                                strategy.knowledge.monitored_data, 
                                strategy.knowledge.analysis_data,
                                strategy.knowledge.adaptation_options,
                                strategy.knowledge.plan_data,
                                execute_data
                            )
                db.add_run(runDB)
        flag = True

        