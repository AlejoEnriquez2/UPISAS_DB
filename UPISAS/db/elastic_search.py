from elasticsearch import Elasticsearch
from datetime import datetime, timedelta


class ElasticsearchDB():
    #certificate verification is disabled
    def __init__(self, host='localhost', port=9200, scheme='http'):
        self.es = Elasticsearch(hosts=f"{scheme}://{host}:{port}", verify_certs=False)
    
    def create_index(self, index_name):
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)

    def add_exemplar(self, exemplar_name, monitor_schema, execute_schema, adaptation_options_schema):
        # Get the class name in lowercase
        exemplar_name = exemplar_name.lower()

        # Check if the Exemplar document already exists
        exemplar_id = self.get_exemplar_id(exemplar_name)

        # If not, create a new Exemplar document
        if not exemplar_id:
            exemplar_doc = {
                'name': exemplar_name,
                'monitor_schema': monitor_schema,
                'execute_schema': execute_schema,
                'adaptation_options_schema': adaptation_options_schema,
                'runs': []
            }
            response = self.store_document('exemplar', exemplar_doc)
            exemplar_id = response['_id']

        return exemplar_id

    def store_document(self, index_name, document):
        return self.es.index(index=index_name, body=document)
    
    def delete_indices(self, indices):
        return self.es.options(ignore_status=[400,404]).indices.delete(index=indices)

    def get_exemplar_id(self, exemplar_name):
        # Search for an Exemplar with the same name
        body = {
            "query": {
                "match": {
                    "name": exemplar_name
                }
            }
        }
        response = self.es.search(index='exemplar', body=body)

        # Default exemplar_id to None
        exemplar_id = None

        # If an Exemplar with the same name exists, retrieve its ID
        if response['hits']['total']['value'] > 0:
            exemplar_id = response['hits']['hits'][0]['_id']
        # else:
        #     # If not, create a new Exemplar and generate a new ID
        #     exemplar_id = str(uuid.uuid4())
        return exemplar_id

    def get_document(self, index_name, doc_id):
        return self.es.get(index=index_name, id=doc_id)
    
    def update_document(self, index_name, doc_id, update_script):
        return self.es.update(index=index_name, id=doc_id, body=update_script)
  
    # Get a run document from the particular hour
    def get_runs_by_exemplar(self, exemplar_id, start_time=None, end_time=None):
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "exemplar_id": exemplar_id
                            }
                        }
                    ]
                }
            }
        }

        if start_time and end_time:
            body['query']['bool']['must'].append({
                "range" : {
                    "timestamp" : {
                        "gte" : start_time,
                        "lt" :  end_time
                    }
                }
            })

        return self.es.search(index='run', body=body)

    def exists(self, exemplar_name, doc_id):
        return self.es.exists(index=exemplar_name, id=doc_id)