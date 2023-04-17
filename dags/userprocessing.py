from airflow import DAG
import json
from datetime import datetime
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.http_sensor import HttpSensor

# Provide a unique name/id for your DAG: user_processing
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

    extract_user = SimpleHttpOperator(
    task_id='extract_user',
    method='GET',
    http_conn_id='user_api',
    endpoint='/api',
    headers={"Content-Type": "application/json"},
    response_filter=lambda response: json.loads(response.text),
    log_response=True,
)