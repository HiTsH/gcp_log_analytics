# System Architecture

## Components

1. **Data Generation**

   - Python script generates synthetic log data
   - Outputs to GCS in CSV format

2. **Data Processing**

   - Apache Beam pipeline running on Dataflow
   - Key transformations:
     - Filter non-200 status codes
     - Aggregate bytes by user
   - Output to BigQuery

3. **Monitoring**
   - Pub/Sub for event notifications
   - Email alerts for:
     - Job start (with ETA)
     - Job completion
     - Failures

## Scalability Features

- Dataflow autoscaling
- Partitioned BigQuery tables
- Batch processing for large datasets
