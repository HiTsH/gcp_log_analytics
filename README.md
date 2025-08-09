# 1TB Log Analytics Pipeline

## Overview

Production-grade data pipeline processing 1TB of server logs on GCP.

## Features

- Scalable Dataflow processing
- BigQuery data warehouse
- Email notifications
- Terraform infrastructure

## Setup

1. Set environment variables:

   ```bash
   export GCP_PROJECT=your-project-id
   ```

2. Deploy infrastructure:

   ```bash
   make deploy
   ```

3. Generate test data:

   ```bash
    make generate-data
   ```

4. Run pipeline:

   ```sql
   make run-pipeline
   ```

## Monitoring

1. Start the alert listener

   ```sql
   make start-monitoring
   ```

## CI/CD

### Github Actions Workflow

- Linting
- Terraform Validation
- Automated deployment
