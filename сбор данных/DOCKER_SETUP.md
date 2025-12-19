# Instructions for running the project via Docker

## Project Description

The project is a system for collecting and processing earthquake data from the USGS API using:
- Apache Kafka for transferring data between components
- Apache Airflow for task orchestration (DAG)
- SQLite for storing processed data
- PostgreSQL for Airflow metadata

## Architecture

1. Job 1 (Ingestion): Collect earthquake data from the USGS API and send it to Kafka
2. Job 2 (Cleaning & Storage): Read data from Kafka, clean it, and store it in SQLite
3. Job 3 (Analytics): Daily analytics on the collected data

## Requirements

- Docker version 20.10 or later
- Docker Compose version 1.29 or later
- Minimum 4GB of free RAM
- Minimum 10GB of free disk space

## Project Structure

```
.
├── docker-compose.yaml # Configuration of all services
├── Dockerfile.airflow # Dockerfile for Airflow
├── requirements.txt # Python dependencies
├── airflow/
│ ├── airflow.cfg # Airflow configuration
│ └── dags/ # DAG files
│ ├── job1_ingestion_dag.py
│ ├── job2_clean_store_dag.py
│ └── job3_daily_summary_dag.py
├── src/ # Source code
│ ├── job1_producer.py
│ ├── job2_consumer.py
│ ├── job3_analytics.py
│ └── db_utils.py
└── data/ # SQLite database (created automatically)
└── app.db
```

## Step-by-step instructions for launching

### Step 1: Preparing the environment

1. Make sure Docker and Docker Compose are installed:
```bash
docker --version
docker-compose --version
```

2. Change to the project directory:
```bash
cd /Users/symbatbayanbayeva/Downloads/сбор\ data
```

### Step 2: Initializing Airflow

Before the first Before launching, you must initialize the Airflow database:

```bash
# Set the UID for the Airflow user (recommended for Linux/Mac)
export AIRFLOW_UID=$(id -u)

# Initialize the database (creates the user and tables)
docker-compose up airflow-init
```

This command will create:
- The default user (airflow/airflow)
- The necessary tables in PostgreSQL
- The directory structure for logs

**Note:** The AIRFLOW_UID variable is optional on macOS/Windows, but is recommended for Linux.

### Step 3: Start all services

Start all services with one command:

```bash
docker-compose up -d
```

**Note:** If you see a version warning or the error "project name must not be empty," this is normal—the project name is explicitly set in `docker-compose.yaml` as `earthquake-data-pipeline`.

This command will start the following services:
- **Zookeeper** (port 2181)
- **Kafka** (ports 9092, 29092)
- **Kafka UI** (port 8080) - web interface for managing Kafka
- **PostgreSQL** (internal port) - database for Airflow
- **Airflow Webserver** (port 8081) - Airflow web interface
- **Airflow Scheduler** - task scheduler

### Step 4: Checking service status

Check that all containers are running:

```bash
docker-compose ps
```

All services should be in the "Up" or "healthy" status.

### Step 5: Accessing Web Interfaces

#### Airflow Web UI
- URL: http://localhost:8081
- Login: `airflow`
- Password: `airflow` (default, can be changed via environment variables)

#### Kafka UI
- URL: http://localhost:8080
- Viewing Kafka topics, messages, and configuration

### Step 6: Activating DAGs

1. Open the Airflow Web UI: http://localhost:8081
2. Find the DAGs:
- `job1_continuous_ingestion` - data collection every minute
- `job2_hourly_cleaning` - cleaning and storing every hour
- `job3_daily_analytics` - analytics once a day
3. Enable the DAGs by toggling the switch to the left of their names

### Step 7: Monitoring Execution

- **Airflow Logs**: View task logs directly in the web UI
- **Container Logs**:
```bash
docker-compose logs -f airflow-scheduler
docker-compose logs -f airflow-webserver
```
- **Kafka Topics**: Inspect messages in the Kafka UI

## Useful Commands

### View Logs

```bash
# All Logs
docker-compose logs -f

# Service-Specific Logs
docker-compose logs -f airflow-scheduler
docker-compose logs -f kafka
docker-compose logs -f postgres
```

### Stop Services

```bash
# Stop without deleting data
docker-compose stop

# Stop with container deletion (data is preserved)
docker-compose down

# Complete cleanup (removes ALL data, including databases)
docker-compose down -v
```

### Restart services

```bash
# Restart all services
docker-compose restart

# Restart a specific service
docker-compose restart airflow-scheduler
```

### Execute commands inside a container

```bash
# Enter an Airflow container
docker-compose exec airflow-webserver bash

# Execute an Airflow command
docker-compose exec airflow-webserver airflow dags list
docker-compose exec airflow-webserver airflow tasks list job1_continuous_ingestion
```
### Check the database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U airflow -d airflow

# Check the SQLite database
docker-compose exec airflow-webserver sqlite3 /opt/airflow/data/app.db "SELECT COUNT(*) FROM events;"
```

## Configuring the DAG Schedule

The schedule can be changed in the DAG files:

- **job1_ingestion_dag.py**: `schedule=timedelta(minutes=1)` - every minute
- **job2_clean_store_dag.py**: `schedule='@hourly'` - every hour
- **job3_daily_summary_dag.py**: `schedule='@daily'` - every day

After making changes, restart the scheduler:
```bash
docker-compose restart airflow-scheduler
```

## Troubleshooting

### Problem: Containers don't start

**Solution:**
1. Check the logs: `docker-compose logs`
2. Make sure the following ports are not in use:
- 8080 (Kafka UI)
- 8081 (Airflow)
- 9092 (Kafka)
- 2181 (Zookeeper)

### Problem: DAG not visible in Airflow

**Solution:**
1. Check the syntax of your DAG files:
```bash
docker-compose exec airflow-webserver python /opt/airflow/dags/job1_ingestion_dag.py
```
2. Check the scheduler logs:
```bash
docker-compose logs airflow-scheduler | grep ERROR
```

### Problem: Errors connecting to Kafka

**Solution:**
1. Make sure Kafka is running: `docker-compose ps kafka`
2. Check that Kafka is ready:
```bash
docker-compose exec kafka kafka-topics --bootstrap-server localhost:29092 --list
```

### Problem: Database not being created

**Solution:**
1. Check permissions on the `data/` directory:
```bash
chmod 777 data/
```
2. Check the consumer logs:
```bash
docker-compose logs airflow-scheduler | grep consumer
```

### Problem: Out of memory

**Solution:**
1. Increase Docker's memory limit (in Docker Desktop settings)
2. Stop unneeded containers: `docker ps` and `docker stop <container_id>`

## Cleanup and reset

### Complete project cleanup

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove images (optional)
docker rmi $(docker images -q)

# Clean up unused resources
docker system prune -a
```

### Reset only the Airflow database

```bash
# Stop services
docker-compose down

# Remove PostgreSQL volume
docker volume rm data-collection_postgres-db-volume

# Reinitialize
export AIRFLOW_UID=$(id -u) # for Linux/Mac
docker-compose up airflow-init
docker-compose up -d
```

### Reset application data only

```bash
# Delete the SQLite database
rm data/app.db

# Restart services
docker-compose restart
```

## Environment Variables

You can configure the project via environment variables in `docker-compose.yaml`:

- `KAFKA_BOOTSTRAP_SERVERS` - Kafka address (default: `kafka:29092`)
- `AIRFLOW_UID` - Airflow user UID (default: 50000)

## Performance

To improve performance:

1. **Increase Docker resources**: In Docker Desktop, configure CPU and Memory
2. **Configure Kafka**: Increase KAFKA_HEAP_OPTS in docker-compose.yaml
3. **Optimize Airflow**: Configure parallelism in airflow.cfg

## Security

⚠️ **Important for production:**

1. Change default passwords:
- PostgreSQL: in docker-compose.yaml
- Airflow: via web interface or environment variables

2. Configure Fernet Key:
```bash
export AIRFLOW__CORE__FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

3. Use HTTPS for web interfaces

4. Restrict port access through a firewall

## Additional Information

- **Airflow Documentation**: https://airflow.apache.org/docs/
- **Kafka Documentation**: https://kafka.apache.org/documentation/
- **USGS API**: https://earthquake.usgs.gov/earthquakes/feed/v1.0/

## Support

If you encounter problems:
1. Check the logs: `docker-compose logs`
2. Check the status of the containers: `docker-compose ps`
3. Ensure all dependencies are installed
4. Check the Docker and Docker Compose versions