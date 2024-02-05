
class ExemplarDB:    
    def __init__(self, name, monitor_schema, execute_schema, adaptation_options_schema):
        self.name = name
        self.monitor_schema = monitor_schema
        self.execute_schema = execute_schema
        self.adaptation_options_schema = adaptation_options_schema