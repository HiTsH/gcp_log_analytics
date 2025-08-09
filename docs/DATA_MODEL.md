# Data Modeling Approach

## OLTP (Source Data)

```csv
log_id,user_id,status_code,timestamp,bytes_sent
```

## OLAP (Target Schema)

### Fact Table

```sql
CREATE TABLE server_logs.user_metrics (
  user_id INT64,
  total_bytes INT64,
  date DATE
) PARTITION BY date;
```

### Dimension Tables

```sql
CREATE TABLE server_logs.users (
  user_id INT64,
  user_name STRING,
  account_type STRING
);
```

### Transformation Logic

1- Filter to only successful (200) requests
2- Sum bytes_sent by user_id
3- Enrich with dimension data (future enhancement)

### **Makefile**

```makefile
.PHONY: all deploy test clean

all: test deploy

deploy:
	cd infra && terraform apply -auto-approve -var="project_id=${GCP_PROJECT}"

generate-data:
	python src/data_generator/generate_logs.py

run-pipeline:
	python src/dataflow_pipeline/pipeline.py

start-monitoring:
	python src/monitoring/alerts.py

test:
	python -m pytest tests/

clean:
	cd infra && terraform destroy -auto-approve -var="project_id=${GCP_PROJECT}"
```
