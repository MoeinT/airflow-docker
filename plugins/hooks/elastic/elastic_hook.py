from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base_hook import BaseHook
from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):
    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = self.get_connection(conn_id)

        self.conn_config = {}

        if self.conn.host:
            hosts = self.conn.host.split(",")
        
        if self.conn.port:
            self.conn_config["port"] = int(self.conn.port)
        
        if self.conn.login: 
            self.conn_config["http_auth"] = (self.conn.login, self.conn.password)

        self.es = Elasticsearch(hosts, **self.conn_config)
        self.index = self.conn.schema

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


# Add ElasticHook to the plugin system manager
class AirflowElasticPlugin(AirflowPlugin):
    name = "elastic"
    hooks = [ElasticHook]