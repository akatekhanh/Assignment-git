import os
from pathlib import Path
import csv
from dotenv import load_dotenv
load_dotenv()

DATA_PATH = os.getenv('DATA_PATH')

def save_csv_file(header, data, filename):
    data_dir = Path(DATA_PATH)
    if not data_dir.is_dir():
        os.mkdir(DATA_PATH)
    
    path = os.path.join(DATA_PATH, filename)
    with open(path, 'w', newline='\n') as file:
        # Create CSV file
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(header)

        # Write the data
        writer.writerows(data)

