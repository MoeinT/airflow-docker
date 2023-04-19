from datetime import datetime

from airflow import DAG, Dataset
from airflow.decorators import task

my_file = Dataset("/tmp/my_file.txt")

with DAG(
    dag_id = "consumer", 
    schedule = [my_file], 
    start_date = datetime(2023, 4, 19), 
    catchup = False) as dag:
    
    @task()
    def read_dataset(): 
        with open(my_file.uri, mode="r") as f: 
            print(f.read())
    
    read_dataset()