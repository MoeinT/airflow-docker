from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import XCom
from datetime import datetime

def _t1(ti):
    ti.xcom_push(key = "MyValueToShare", value = 50)

def conditionally_execute(ti):
    condition = ti.xcom_pull(key = "MyValueToShare", task_ids='task_1')
    if condition >= 40:
        return 'task_a'
    else:
        return 'task_b'

with DAG("xcom_dag", start_date = datetime(2023, 4, 24), 
         schedule_interval = '@daily',catchup = False) as dag:
    
    task_1 = PythonOperator(
        task_id = "task_1", 
        python_callable = _t1
    )

    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=conditionally_execute,
        provide_context=True,
         dag=dag
    )

    task_a = BashOperator(
        task_id='task_a',
        bash_command='sleep 5'
    )

    task_b = BashOperator(
        task_id='task_b',
        bash_command='sleep 5'
    )

    task_c = BashOperator(
        task_id='task_c',
        bash_command='sleep 5', 
        trigger_rule = "none_failed"
    )

    task_1 >> branch_task >> [task_a, task_b] >> task_c