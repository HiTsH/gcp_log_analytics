import uuid
import random
import datetime
import csv
from google.cloud import storage

def generate_logs(num_records=10000000, batch_size=100000):
    """Generate 1TB of sample log data in batches"""
    client = storage.Client()
    bucket = client.get_bucket('your-data-lake-bucket')
    
    for batch_num in range(num_records // batch_size):
        blob = bucket.blob(f'logs/raw/logs_batch_{batch_num}.csv')
        
        with blob.open('w') as f:
            writer = csv.writer(f)
            writer.writerow(['log_id', 'user_id', 'status_code', 'timestamp', 'bytes_sent'])
            
            for _ in range(batch_size):
                writer.writerow([
                    str(uuid.uuid4()),
                    random.randint(1, 10000),
                    random.choice([200, 404, 500]),
                    datetime.datetime.now().isoformat(),
                    random.randint(1, 10000)
                ])

if __name__ == "__main__":
    generate_logs()
