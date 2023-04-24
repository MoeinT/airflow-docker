from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import XCom
from datetime import datetime

def _t1():
    return 42

def _t2(ti):
    ti.xcom_push(key = "my_value_xcom", value = 50)

with DAG("xcom_dag", start_date = datetime(2023, 4, 24), 
         schedule_interval = '@daily',catchup = False) as dag:
    
    task_1 = PythonOperator(
        task_id = "task_1", 
        python_callable = _t1
    )

    task_2 = PythonOperator(
        task_id = "task_2", 
        python_callable = _t2
    )

    task_1 >> task_2