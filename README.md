### About project:

This is a service for monitoring OS metrics and writing it in to database.
Can work with any database supported by SQLAlchemy.
Use kafka as message broker.

##### Supported metrics:
 - `cpu_metrics` - CPU utilisation, percentage
 - `mem_metrics` - Memory utilisation, percentage
 - `disk_metrics` - Disk usage, percentage

Each metrics also contains:
 - local time on machine, when metrics was collected
 - time, when metrics was wrote to database
 - hostname of machine, where metrics was collected

##### Quick start:

`git clone https://github.com/LinnTroll/aiven-metrics-hw.git`

`cd aiven-metrics-hw`

Edit `.env` file:
you need to fill connection parameters for connecting to kafka and database.

`docker-compose up --scale client=3`

This command should start 3 containers, that send their metrics to kafka topic.
And one container, that read data form this topic and write it to database.
