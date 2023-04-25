from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base_hook import BaseHook
from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):
    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(conn_id)

        conn_config = {}

        if conn.host:
            hosts = conn.host.split(",")
        
        if conn.port:
            conn_config["port"] = int(conn.port)
        
        if conn.login: 
            conn_config["http_auth"] = (conn.login, conn.password)

        es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

# Return information about the ElasticSearch object
    def info(self):
        return self.es.info()

# Override the index attribute
    def set_index(self, index):
        self.index = index

# Adding an index in the document
    def add_doc(self, index, doc_type, doc): 
        result = self.es.index(index=index, doc_type=doc_type, doc=doc)
        return result