from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import XCom
from datetime import datetime

def _t1(ti):
    ti.xcom_push(key = "MyValueToShare", value = 50)

def _t2(ti):
    print(f"Pulled value: {ti.xcom_pull(key = 'MyValueToShare', task_ids = 'task_1')}")

with DAG("xcom_dag", start_date = datetime(2023, 4, 24), 
         schedule_interval = '@daily',catchup = False) as dag:
    
    task_1 = PythonOperator(
        task_id = "task_1", 
        python_callable = _t1
    )

    task_2 = PythonOperator(
        task_id = "task_2", 
        python_callable = _t2, 
        provide_context=True
    )

    task_1 >> task_2