#from UPISAS.example_strategy import ExampleStrategy
from UPISAS.exemplar import Exemplar
from UPISAS.exemplars.ews import EWS
import signal
import sys


# def signal_handler(sig, frame):
#     print('You pressed Ctrl+C!')
#     exemplar.stop()
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)
if __name__ == '__main__':
    
    exemplar = EWS(auto_start=True)
    exemplar.start_run()
#