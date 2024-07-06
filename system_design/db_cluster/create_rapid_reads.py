import requests
import concurrent.futures
import time
import random

API_URL = "http://localhost:5000/records"

# Function to make a GET request to the API
def get_record(record_id):
    response = requests.get(f"{API_URL}/{record_id}")
    if response.status_code == 200:
        pass
        # print(f"Record {record_id} fetched successfully.")
    else:
        print(f"Failed to fetch record {record_id}. Status code: {response.status_code}")

def main():
    num_requests = 10000000000000  # Number of requests to make
    record_id = random.randint(1, 100000)  # ID of the record to read
    start_time = time.time()

    # Use ThreadPoolExecutor to make concurrent GET requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(get_record, record_id) for _ in range(num_requests)]
        concurrent.futures.wait(futures)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Made {num_requests} requests in {duration:.2f} seconds")

if __name__ == "__main__":
    main()
