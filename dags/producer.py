from datetime import datetime

from airflow import DAG, Dataset
from airflow.decorators import task

my_file = Dataset("/tmp/my_file.txt")

# Defining the producer TAG
with DAG(
    dag_id = "producer", 
    schedule = "@daily", 
    start_date = datetime(2023, 4, 19), 
    catchup = False) as dag:
    
    @task(outlets=[my_file])
    def update_dataset(): 
        with open(my_file.uri, mode="a+") as f: 
            f.write("producer update")
    
    update_dataset()