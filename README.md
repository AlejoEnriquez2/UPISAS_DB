# UPISAS
Unified Python interface for self-adaptive system exemplars.

### Prerequisites 
Tested with Python 3.9.12

### Installation
In a terminal, navigate to the parent folder of the project and issue:
```
pip install -r requirements.txt
```
### Run unit tests
In a terminal, navigate to the parent folder of the project and issue:
```
python -m UPISAS.tests.upisas.test_exemplar
python -m UPISAS.tests.upisas.test_strategy
python -m UPISAS.tests.swim.test_swim_interface
```
### Database
Execute the docker compose file, inside the folde db_dockers/
```
docker compose up -d
```

Then follow the instructions on the manual to select the database you want to use, and how to use the dashboard 

### Run
In a terminal, navigate to the parent folder of the project and issue:
```
python run.py
```





