from airflow import DAG
from airflow.operators.bash import BashOperator
from groups.download_tasks import download_files
from groups.transform_tasks import transform_files

from datetime import datetime

with DAG('group_dag', start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:
    
    downloads = download_files()
 
    checkfiles = BashOperator(
        task_id='checkfiles',
        bash_command='sleep 5'
    )

    transforms = transform_files()

    downloads >> checkfiles >> transforms
 
 
