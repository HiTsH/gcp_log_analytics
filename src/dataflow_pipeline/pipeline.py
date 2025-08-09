import os
from dotenv import load_dotenv

import apache_beam as beam
from transforms import FilterErrors, AggregateByUser
import json
import logging
from datetime import datetime


class LogNotifications(beam.DoFn):
    def process(self, element):
        from google.cloud import pubsub_v1
        
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path('your-project', 'dataflow-alerts')
        
        # Job start notification
        start_message = {
            'job_id': 'log-processing-job',
            'severity': 'INFO',
            'estimated_time': 120,  # 2 hours estimate
            'timestamp': datetime.now().isoformat()
        }
        publisher.publish(topic_path, json.dumps(start_message).encode('utf-8'))
        
        yield element
        
        # Job end notification
        end_message = {
            'job_id': 'log-processing-job',
            'severity': 'INFO',
            'processed_records': element[1],  # Count from aggregation
            'timestamp': datetime.now().isoformat()
        }
        publisher.publish(topic_path, json.dumps(end_message).encode('utf-8'))

def run_pipeline():
    load_dotenv()
    options = beam.options.pipeline_options.PipelineOptions(
        project=os.getenv('GCP_PROJECT_ID'),
        region=os.getenv('GCP_REGION'),
        temp_location=f'gs://{os.getenv("GCS_BUCKET_NAME")}/temp',
        staging_location=f'gs://{os.getenv("GCS_BUCKET_NAME")}/staging',
        setup_file='./setup.py'
    )
    
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadFromGCS' >> beam.io.ReadFromText('gs://your-data-lake-bucket/logs/raw/*.csv')
         | 'ParseCSV' >> beam.Map(lambda x: x.split(','))
         | 'FilterErrors' >> FilterErrors()
         | 'AggregateByUser' >> AggregateByUser()
         | 'SendNotifications' >> beam.ParDo(LogNotifications())
         | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
             table='your-project:server_logs.user_metrics',
             schema='user_id:INTEGER,total_bytes:INTEGER',
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
         )
        )

if __name__ == "__main__":
    run_pipeline()
