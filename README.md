# Running airflow on a Docker container
Follow this tutorial for more details. 
We can use docker compose to deploy airflow on docker containers and get the web UI up & running. In order to do that, we need to fetch the docker-compose file using the below command on PowerShell:

```Invoke-WebRequest -Uri 'https://airflow.apache.org/docs/apache-airflow/2.5.3/docker-compose.yaml' -OutFile 'docker-compose.yaml'```

**How to initialize the airflow metadata database –** The command ```docker compose up airflow-init``` is used to initialize the Airflow metadata database, which is required for Airflow to run properly.
When you install Airflow using Docker Compose, the ```airflow-init``` service is created to initialize the Airflow database. This service runs a set of commands that create the necessary tables and default user accounts in the database.
Running the ```docker compose up airflow-init``` command will start the "airflow-init" service and execute the commands necessary to create the Airflow metadata database. Once the initialization is complete, the "airflow-init" service will stop automatically.

**Docker-compose up –** After initializing the Airflow metadata database, you can start Airflow itself by running the command ```docker compose up```. The ```.docker-compose```. part is part of the Docker Compose command line tool. Tells Docker Compose to start the services defined in the docker-compose.yml file. This command is useful for starting all the services in a multi-container application, which is the case for airflow. 
**```.docker ps``` -** Use this command to get a list of all running containers on the Docker host. 
**```docker exec id``` -** Use this command and the id of one of the containers to interact with the airflow command line interface.
**Use the below command to interact with the web user –**  curl --user "airflow:airflow" "http://localhost:8080/api/v1/dags"

**Interacting with provides –** Installing Airflow core gives us access to some of the most important operators, such as the Python or Bash operators; however, in cases where we need to interact with other platforms, such as AWS, Databricks or DBT, we will have to install additional operators.  


# Airflow architecture
Airflow is an open-source platform to programmatically author, schedule and monitor data engineering workflows. Airflow however, is not a data streaming, nor a data processing/transformation framework. So, you won’t be able to schedule your workflow on a micro-batch basis; on the other hand, you won’t be able to transform your data, like Spark, inside your Airflow operators. If you do so, you might end up with memory overflow errors. Instead, Airflow is used to trigger and orchestrate the tools you use to process and transform your data

# What is an operator?
An operator is a Python class that encapsulates logic to perform a unit of task. Operators are the building blocks of Airflow DAGS, and contain the logic on how the tasks need to be implemented. In Airflow, each task is defined by instantiating an operator. All operators inherit from the BaseOperator class that contains the logic on how an operator should be executed. There are three kinds of operators on a high lever: 
***Execute –*** A kind of operator that executes an action; i.e., a PythonOperator that operates a Python function, or a BashOperator that executes a bash script.
Transfer operators – They’re in charge of transferring data between point A to point B. 
***Sensors –*** They allow you to only run a task in case a condition is set to true. This operator is useful in creating an event-driven application. 

Here are a few other examples of Airflow operators: 
***KubernetesPodOperator –***  Executes a task defined as a Docker image in a Kubernetes Pod.
***SnowflakeOperator –*** Executes a query against a Snowflake database.
***HttpSensor –*** This is an example of a sensor operator; it executes an HTTP GET statement and returns false for 404 Not Found, or response check failures. So, every 30 seconds it creates this request and checks if there’s an api available. This task checks whether a web service or a REST API is available within an endpoint before running a task in the DAG. If the result of this operator is true, the next task will be run. 
***SimpleHttpOperator  –*** The SimpleHttpOperator is an operator in Apache Airflow that allows you to make HTTP requests to a web server. It can be used to retrieve data, send data, or trigger an action on a remote server. Read doc here.

# Airflow Architectures 
In Apache Airflow, the single-node architecture refers to the setup where all the Airflow components, including the web server, scheduler, metadata database, and workers, are installed and run on a single machine. In this setup, Airflow can only scale vertically by adding more resources to the single machine.

On the other hand, the multi-node architecture refers to a setup where each component of Airflow runs on a separate machine, allowing Airflow to scale horizontally by adding more machines. In this setup, the webserver, scheduler, metadata database, and workers are each deployed to separate nodes or clusters, enabling Airflow to handle larger workflows and higher workloads.

The multi-node architecture can also provide benefits such as increased fault tolerance and better resource utilization. However, it can be more complex to set up and manage than the single-node architecture, which is often used for small-scale deployments or for testing and development purposes.

# How it works under the hood 

1: We create a DAG and store it in the DAG folder. Once the DAG has been stored in the DAG folder, the scheduler parses the folder to detect new available DAGs. The scheduler parses the DAG folder every 5 minutes to detect if there’s any new DAG. If a modification occurs on a DAG, the scheduler applies the changes once every 30 seconds. 

2: The scheduler then runs the DAG and creates a DagRun object with the state “Running” and identifies tasks to be executed creating a TaskInstance object with a state “Known”. 

3: Once the tasks have been identified, the scheduler submits the Task Instances to the executor with the state “Queued”.

4: Once the tasks have been submitted to the queue, the executor pushes them to the workers to be run with task instances having the state “Running”. 

5: Once all the tasks have been successfully run by the workers, the DagRun object will have the state “Succeeded”, if not, it’ll have the state “Failed”.  If the tasks are not yet run, the DagRun object will have the state “Queued”.  


# Test Airflow 

Run this command to have access to the container where the scheduler runs: ```docker exec -it <name_of_the_scheduler> /bin/bash```

Inside that container environment, we will have access to the Airflow CLI; i.e., we can use the ```airflow version``` command to get the version of the airflow currently running in a docker container. 

Run the following command to test a specific task: ```airflow tasks test <DAG_name> <Task_name> <Date_in_the_past>```

# Best Practices 

Do not include too many activities in one operator; i.e., if we’re cleaning our data first, and processing it next, we should not be putting both of them into one task, otherwise if there’s an error in the second task, the first one will have to run as well, which is not efficient. Make sure your tasks are well separated. 

When working with operators like PostgresOperator, it’s best practice to create a sql directory under the dag folder and include all your SQL codes there. We can then refer to those locations in our codes using the PostgresOperator. Read on the best practices when working with PostgresOperator.  

