Earthquake Data Collection Project

A system for automatically collecting, processing, and analyzing earthquake data from the USGS API.

## Quick Start

### Via Docker (recommended)

1. **Initialize Airflow:**
```bash
export AIRFLOW_UID=$(id -u) # for Linux/Mac (optional)
docker-compose up airflow-init
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Access web interfaces:**
- Airflow: http://localhost:8081 (login: `airflow`, password: `airflow`)
- Kafka UI: http://localhost:8080

4. **Activate DAGs:**
- Open Airflow UI
- Enable DAGs: `job1_continuous_ingestion`, `job2_hourly_cleaning`, `job3_daily_analytics`

📖 **Detailed instructions:** See [DOCKER_SETUP.md](DOCKER_SETUP.md)

## Architecture

- **Job 1**: Collect data from USGS API → Kafka (every minute)
- **Job 2**: Read from Kafka → Cleanup → SQLite (every hour)
- **Job 3**: Data analytics → daily_summary (every day)

## Components

- **Apache Kafka** - message queue
- **Apache Airflow** - task orchestration
- **PostgreSQL** - Airflow metadata
- **SQLite** - storage of processed data

## Project Structure

``
. ├── docker-compose.yaml # Docker configuration
├── Dockerfile.airflow # Airflow image
├── requirements.txt # Python dependencies
├── DOCKER_SETUP.md # Detailed instructions
├── airflow/
│ ├── airflow.cfg # Airflow configuration
│ └── dags/ # DAG files
├── src/ # Source code
└── data/ # SQLite database
```

## Useful commands

```bash
# View logs
docker-compose logs -f

# Stop
docker-compose stop

# Complete cleanup
docker-compose down -v
```

## Requirements

- Docker 20.10+
- Docker Compose 1.29+
- 4GB RAM minimum
- 10GB of free space