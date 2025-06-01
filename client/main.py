import time
import requests
import os

def get_charge_category(description: str):
    url = os.getenv('API_CHARGE_CLASSIFICATION')
    payload = {"description": description}

    connection_status = False
    retry_limit = 10
    retry = 0
    while not connection_status and retry <= retry_limit:
        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                print(f"Charge Category: {data['label']}")
                connection_status = True
            else:
                print(f"Error: {response.status_code} - {response.json().get('detail')}")
                connection_status = True
        except requests.exceptions.ConnectionError:
            print("Server not ready, retrying...")
            retry += 1
            time.sleep(2)
    
    if not connection_status:
        print("Failed to connect to the server after multiple attempts.")

if __name__ == "__main__":
  while True:
    user_input = input("Enter a charge description (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    get_charge_category(user_input)
   
