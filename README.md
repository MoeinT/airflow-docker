# Installing Airflow using Docker
We can use docker compose to deploy airflow on docker containers and get the web UI up & running. In order to do that, we need to fetch the docker-compose file using the below command on PowerShell:

```Invoke-WebRequest -Uri 'https://airflow.apache.org/docs/apache-airflow/2.5.3/docker-compose.yaml' -OutFile 'docker-compose.yaml'```

Use the below command for Linux-based operating system: 

```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.3/docker-compose.yaml'```

**How to initialize the airflow metadata database –** The command ```docker compose up airflow-init``` is used to initialize the Airflow metadata database, which is required for Airflow to run properly.
When you install Airflow using Docker Compose, the ```airflow-init``` service is created to initialize the Airflow database. This service runs a set of commands that create the necessary tables and default user accounts in the database.
Running the ```docker compose up airflow-init``` command will start the "airflow-init" service and execute the commands necessary to create the Airflow metadata database. Once the initialization is complete, the "airflow-init" service will stop automatically.

**Docker-compose up –** After initializing the Airflow metadata database, you can start Airflow itself by running the command ```docker compose up```. The ```.docker-compose```. part is part of the Docker Compose command line tool. Tells Docker Compose to start the services defined in the docker-compose.yml file. This command is useful for starting all the services in a multi-container application, which is the case for airflow. 

**docker ps -** Use this command to get a list of all running containers on the Docker host. 

**docker exec id -** Use this command and the id of one of the containers to interact with the airflow command line interface.

**Interact with the User Interface -** Use the below command to interact with the web user. The below command retrieves the list of available DAGs: ```curl --user "airflow:airflow" "http://localhost:8080/api/v1/dags"```

**Interacting with provides –** Installing Airflow core gives us access to some of the most important operators, such as the Python or Bash operators; however, in cases where we need to interact with other platforms, such as AWS, Databricks or DBT, we will have to install additional operators.  

**Airflow configurations -** Running the bellow command copies the configuration file of airflow from the scheduler container into the host machine. Once we have this file, we can modify the configuration settings in Airflow. 

```docker cp materials_airflow-scheduler_1:/opt/airflow/airflow.cfg .```

The configuration file contains information such as how and on which systems tasks should be executed, or the level of parallelism.

**NOTE -** The environment variables in the docker-compose.yaml file overwrite the parameters in the configuration file; so, in order to change certain configurations, like the type of executor, we'll have to modify the docker compose file.


# Airflow architecture
Airflow is an open-source platform to programmatically author, schedule and monitor data engineering workflows. Airflow however, is not a data streaming, nor a data processing/transformation framework. So, you won’t be able to schedule your workflow on a micro-batch basis; on the other hand, you won’t be able to transform your data, like Spark, inside your Airflow operators. If you do so, you might end up with memory overflow errors. Instead, Airflow is used to trigger and orchestrate the tools you use to process and transform your data. Here's a high-level architecture: 

### Scheduler 
The scheduler is responsible for triggering the workflows as well as submitting tasks to the executors 

### Executor
Executors handle running of tasks. In most cases, they push the tasks to the workers to be run; so, they're responsible in how and on which system the tasks should be run. There are two types of executors: local & remote executors. Local executors run the tasks locally inside the scheduler’s process, on the other hand, remote executors run the tasks remotely, i.e., within a kubernetes cluster, usually with a use of a pool of executors. Here's different executor types: 

[**Sequential executors -**](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/sequential.html) Default executor when we install Airflow; with this it is not possible to run tasks in parallel. They'll always run in sequence.  

[**Local executors -**](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/local.html) Local executors allow you to run multiple tasks at the same time, but on a single machine. This is not ideal for scaling up, as it only allows you to scale vertically, and not horizontally. 

[**Celery executors -**](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/local.html) It allows you to scale up the execution of tasks by providing multiple workers. The celery executor provides an additional component to the architecture, called Queue; it's composed of a backend to store the state of each workder, and a broker to push the tasks in the right order. The queue could be Redis, or RabbitMQ, which will have to be installed. This is the default executor specified in the ```docker-compose.yaml``` file. We can see that an environment variable has been set for the metadata database, one for the backend, and one for the broker.

**Executor dashboard -** When working with Celery, we can also take advantage of [**flower**](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/flower.html), which is a web based tool for monitoring and administrating the clusters. Use the following command to get it up & running: ```docker-compose --profile flower up -d```. Once that's up & running, load the page on [http://localhost:5555/](http://localhost:5555/). When running your DAG, depending on the number of tasks being executed, the flower dashboard allows you to monitor their status.

**Creating a queue -** There is a default queue associated with every worker; meaning that all tasks that are pushed to that default queue will be run under those workders; however, under the worker task in the yaml file, we can use the following command to attach a workder with a queue: ```celery worker -q <queue_name>```; so, every task that is pushed to that queue will be run only and only by that worker. This allows us to add more flexibility in how & on which worker certain tasks should be executed. In order to push a task to a given queue, specify it using the ```queue``` parameter in the operator.

### Web Server
A flask-based user interface that is used to inspect, trigger and debug DAGs and tasks. 

### Folder of DAG files
The folder of DAGs is read by the scheduler, the executor and any worker that it might have.

### Metadata Database
Used by the scheduler, executor and the web server to store state. This is compatible with SQL Alchemy, such as Postgresql, MySQL, SQL Server, Oracle and so on. All components of the Airflow architecture are connected to the metadata database, so it allows communications between all components of Airflow.

### Queue
In case of remote executors, once the scheduler has identified which tasks to trigger, it’ll submit them to the executors and the executors push them to the Tasks Queue in the right order to be executed. Most executors will use other components to communicate with their workers, such as a task queue, but we can still think of executors and their workers as a single logical component in airflow overall.


# What is an operator?
An operator is a Python class that encapsulates logic to perform a unit of task. Operators are the building blocks of Airflow DAGS, and contain the logic on how the tasks need to be implemented. In Airflow, each task is defined by instantiating an operator. All operators inherit from the BaseOperator class that contains the logic on how an operator should be executed. There are three kinds of operators on a high lever: 

**Execute –** A kind of operator that executes an action; i.e., a PythonOperator that operates a Python function, or a BashOperator that executes a bash script.

**Transfer operators –** They’re in charge of transferring data between point A to point B. 

***Sensors –*** They allow you to only run a task in case a condition is set to true. This operator is useful in creating an event-driven application. 

Here are a few other examples of Airflow operators: 

***KubernetesPodOperator –***  Executes a task defined as a Docker image in a Kubernetes Pod.

***SnowflakeOperator –*** Executes a query against a Snowflake database.

***HttpSensor –*** This is an example of a sensor operator; it executes an HTTP GET statement and returns false for 404 Not Found, or response check failures. So, every 30 seconds it creates this request and checks if there’s an api available. This task checks whether a web service or a REST API is available within an endpoint before running a task in the DAG. If the result of this operator is true, the next task will be run. 

***SimpleHttpOperator –*** The SimpleHttpOperator is an operator in Apache Airflow that allows you to make HTTP requests to a web server. It can be used to retrieve data, send data, or trigger an action on a remote server. Read doc here.

# Single-node and multi-node architectures
In Apache Airflow, the single-node architecture refers to the setup where all the Airflow components, including the web server, scheduler, metadata database, and workers, are installed and run on a single machine. In this setup, Airflow can only scale vertically by adding more resources to the single machine.

On the other hand, the multi-node architecture refers to a setup where each component of Airflow runs on a separate machine, allowing Airflow to scale horizontally by adding more machines. In this setup, the webserver, scheduler, metadata database, and workers are each deployed to separate nodes or clusters, enabling Airflow to handle larger workflows and higher workloads.

The multi-node architecture can also provide benefits such as increased fault tolerance and better resource utilization. However, it can be more complex to set up and manage than the single-node architecture, which is often used for small-scale deployments or for testing and development purposes.

# How it works under the hood 

1: We create a DAG and store it in the DAG folder. Once the DAG has been stored in the DAG folder, the scheduler parses the folder to detect new available DAGs. The scheduler parses the DAG folder every 5 minutes to detect if there’s any new DAG. If a modification occurs on a DAG, the scheduler applies the changes once every 30 seconds. 

2: The scheduler then runs the DAG and creates a DagRun object with the state “Running” and identifies tasks to be executed creating a TaskInstance object with a state “Known”. 

3: Once the tasks have been identified, the scheduler submits the Task Instances to the executor with the state “Queued”.

4: Once the tasks have been submitted to the queue, the executor pushes them to the workers to be run with task instances having the state “Running”. 

5: Once all the tasks have been successfully run by the workers, the DagRun object will have the state “Succeeded”, if not, it’ll have the state “Failed”.  If the tasks are not yet run, the DagRun object will have the state “Queued”.  

# What are hooks? 

Airflow uses hooks to provide a unified interface for connecting to various external systems, including databases, cloud services, and other APIs. By using hooks, you can abstract away the details of connecting to these systems and focus on writing the logic for your tasks. For example, a **PostgresHook** hook is a type of hook that provides a Python interface to interact with a PostgreSQL database. It allows you to connect to a PostgreSQL database, execute SQL queries, and retrieve data from the database.


# Test Airflow tasks

Run this command to have access to the container where the scheduler runs: ```docker exec -it <name_of_the_scheduler> /bin/bash```

Inside that container environment, we will have access to the Airflow CLI; i.e., we can use the ```airflow version``` command to get the version of the airflow currently running in a docker container. 

Run the following command to test a specific task: ```airflow tasks test <dag_name> <task_name> <Date_in_the_past>``` 

Another scenario would be when we'd like to debug certain tasks; we might have to access the docker container on which that task is running. For example, if there's a task that gathers certain data and another task that stores it in a CSV file, we can access that file by accessing the docker container in which the worker node is running. Use the following command to do that ```docker exec -it <name_of_the_workder_node> /bash/bin```.

Furthermore, if we have defined a postgres db and would like to access and run sql commands on it, we can access it using the above method. Once inside the database container, run psql -Uairflow and start running sql commands. 

# Airflow task groups

It is possible to use TaskGroups in Airflow to organize tasks in a DAG. If there are multiple tasks that follow the same logic, it is possible to devide them into a child DAG and declare it inside the parent DAG. It helps to logically sepearete certain tasks to avoid ending up with a large DAG containing a high number of tasks. See more details [here](https://docs.astronomer.io/learn/task-groups). 

# Communications between tasks 

We can use [Xcom](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html) to communicate between tasks in Airflow. Xcom is a mechanism to let tasks talk to each other; many operators auto-push their results into an Xcom key callled *return_value*, i.e., the PythonOperator. 

**Pushing data to Xcom -** In order to push a result with a specific key name, we need to use the Xcom_push method; for this, we need to pass the ti (task instance) into the function. Use this syntax to push data with a given key & value to Xcom: ```ti.xcom_push(key = "key", value = "value")```. 

**Pulling data from Xcom -** Use the following code to pull data from Xcom: ```ti.xcom_pull(key = 'MyValueToShare', task_ids = 'task_1')```. Notice that you have to provide the id of the task that's pushing the data to Xcom. Also, make sure the ```provide_context``` argument is set to true for the tasks that pulling data from Xcom.

# Conditional executions 

In Airflow, the BranchPythonOperator is used to create a conditional workflow, where the decision to execute a specific task or a set of tasks is based on the result of a Python function. In this method, we need to define a function that returns the task ID of the next task to be executed based on the condition. The tasks that are returned in the function should be defined within the DAG. Make sure to import the BranchPythonOperator package using ```from airflow.operators.python_operator import BranchPythonOperator```.

# Trigger rules

The default workflow behaviour is to trigger tasks only if all the upstream tasks have completed successfully. All operators have a ```trigger_rule``` argument that determines the rule for which the task should be triggered. The default value for that argument is ```all_success```. There are 9 other trigger rules. See the documentation [here](https://airflow.apache.org/docs/apache-airflow/1.10.3/concepts.html?highlight=trigger%20rule). 

# Airflow Plugins

Plugins in Airflow are extensions that allow you to add new functionalities or customize certain features of Airflow to suit your specific needs. Airflow has a modular architecture that allows you to create plugins to add new operators, sensors, hooks, or even entire subsystems.

For example, if you need to interact with a specific API, you can create a custom operator that encapsulates the logic to interact with that API, and then add it to Airflow using a plugin. Or, if you need to customize the behavior of the scheduler, you can create a plugin that overrides the default scheduler implementation.

To create a plugin, you need to define a Python module that contains the code for your plugin. The module should be placed in the plugins directory of your Airflow installation. You can then register your plugin with Airflow by creating an instance of the ```AirflowPlugin``` class and defining the hooks, operators, sensors, or other components that your plugin provides.

# Running ElasticSearch within the Airflow environment 

It is an open-source, full-text search and analytics engine that allows you to store, search, and analyze large volumes of data quickly and in real-time. Elasticsearch can be useful in Airflow for various purposes: 

**Logging -** Airflow generates a lot of logs, and Elasticsearch can be used to store and analyze these logs. By sending Airflow logs to Elasticsearch, you can centralize your log data and make it easier to search and analyze. This can help you identify issues and troubleshoot problems more quickly.

**Monitoring -** Elasticsearch can be used to monitor the health and performance of your Airflow infrastructure. By collecting and analyzing metrics, events, and logs, you can identify performance bottlenecks, detect anomalies, and proactively address issues before they become critical.

**Search -** Airflow provides a web interface for managing workflows and tasks. Elasticsearch can be used to power the search functionality in the web interface, making it easier to find the workflows and tasks you need.

**Analytics -**: Elasticsearch can be used to analyze Airflow metadata, such as task durations, task dependencies, and workflow execution times. By analyzing this data, you can identify patterns, optimize your workflows, and improve your overall Airflow performance.

Add the elastic search service in the docker compose yaml file and run the following command to install the elasticSearch container: ```docker-compose -f .\docker-compose-es.yaml up -d```

# Creating a Plugin for ElasticSearch

The goal is to be able to interact with ElasticSearch, which is an external tool to Airflow. For this we need to create a custom hook; here are the steps: 
- Create a connection of type ```elastic``` on the Airflow UI (connection type: HTTP, host: elastic, port: 9200)
- In order to be able to interact with ElasticSearch, we need to create a hook, a service that allows us to encapsulate the logic required to interact with an external service.
- Create a hook/elastic subfolder under the plugin folder. Create a new .py file under which you can define a custom hook for ElasticSearch. 
- Once the ElasticSearch class has been created, you need to register it by defining another class that inherits from ```AirflowPlugin```. You then add the following line of code to add the CustomHook to the plugin system manager: ```hooks = [<name_of_your_hook>]```.

**BaseHook -** In order to implement step 1, we need to define a class that inherits from the ```BaseHook``` class. See more details in the code under the plugins folder.  

**Connection -** When we create a connection in the Airflow UI, a row gets created within the connection table of Airflow's metadata database. This table has certain columns that we can access by calling the ```self.get_connection(conn_id)``` method of the ```BaseHook``` class in Python. We can then access values of those columns by using the dot notation, i.e., ```hosts = conn.host```. 

**Index -** The ```index``` method of the ```elasticsearch.Elasticsearch``` object sends a request to Elasticsearch to index the provided document in the specified index. The request is executed over the HTTP protocol and the Elasticsearch server processes it to store the document in its index.

# Best Practices

Do not include too many activities in one operator; i.e., if we’re cleaning our data first, and processing it next, we should not be putting both of them into one task, otherwise if there’s an error in the second task, the first one will have to run as well, which is not efficient. Make sure your tasks are well separated. 

When working with operators like PostgresOperator, it’s best practice to create a sql directory under the dag folder and include all your SQL codes there. We can then refer to those locations in our codes using the PostgresOperator. Read on the best practices when working with PostgresOperator.  

When defining a task in a DAG, we need to make sure it produce the same outcome on every re-run; i.e., avoid using **INSERT** statements in a task. 

For communicating between tasks in a DAG, use XCom for small messages; XCom contains the required information that needs to be shared between tasks and is stored in the Airflow meta database; for parsing larger data between tasks, however, a good way is to use a remote storage such as S3/HDFS. For example, if we have a task that stores processed data in S3 that task can push the S3 path for the output data in Xcom, and the downstream tasks can pull the path from XCom and use it to read the data.

You should avoid writing the top level code which is not necessary to create Operators and build DAG relations between them. This will have negative impact in performance when the Airflow scheduler parses the top-level code

# References 
[Architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html) 

[Running Airflow on Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user)

[Airflow Operators](https://docs.astronomer.io/learn/what-is-an-operator?tab=traditional#example-implementation)

[Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/2.1.4/best-practices.html)
