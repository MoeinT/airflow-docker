import json
from airflow import DAG
from datetime import datetime
from pandas import json_normalize

from airflow.decorators import dag, task
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.python import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Function to process the ingest users
def _process_user(ti) -> None:
    """
    Function to process the extracted data from HTTP and store it in a CSV file
    """
    user = ti.xcom_pull(task_ids = "extract_user")
    user = user['results'][0]

    processed_user = json_normalize({
        'firstname': user['name']['first'], 
        'lastname': user['name']['first'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user["email"], 
        'age': user["registered"]['age'],
        "registrationdate": user["registered"]["date"]
        })
    
    processed_user.to_csv("/tmp/processed_user.csv", index=None, header=False)


def _store_user():
    """
    Function to copy the user data from CSV into postgresql
    """
    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(sql="""
      COPY users FROM STDIN WITH CSV DELIMITER ','
        """, 
    filename="/tmp/processed_user.csv")


# Define the user_processing DAG
with DAG("user_processing", start_date = datetime(2023, 4, 17), 
         schedule_interval = '@daily',catchup = False) as dag:
    
    # Create table with a given schema
    create_user_table = PostgresOperator(
        task_id="create_user_table", 
        postgres_conn_id="postgres",
        sql="sql/schema.sql",
    )

    # Check for an api 
    is_api_available = HttpSensor(
        task_id = "is_api_available", 
        http_conn_id = "user_api",
        endpoint = "api/"
        )

    # Extract users 
    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        method='GET',
        http_conn_id='user_api',
        endpoint='/api',
        headers={"Content-Type": "application/json"},
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    # Process Users
    process_user = PythonOperator(
        task_id='process_user',
        python_callable=_process_user
    )

    store_user = PythonOperator(
        task_id = "store_user", 
        python_callable = _store_user
    )

    create_user_table >> is_api_available >> extract_user >> process_user >> store_user