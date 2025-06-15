# data_generator.py
import csv
import time
import random
from datetime import datetime

file_path = "realtime_data.csv"

# Header
with open(file_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'value'])

# Generate data
while True:
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        now = datetime.utcnow().isoformat()
        value = round(random.uniform(20.0, 10000.0), 2)
        writer.writerow([now, value])
    time.sleep(2)
