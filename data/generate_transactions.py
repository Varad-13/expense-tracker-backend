import requests
import random
from datetime import datetime, timedelta
import pytz

# Define card numbers and their respective limits
cards = {
    "1273848272149222": 5000,
    "1273848272149234": 3000,
    "1273848272149235": 7000
}

# Define categories and their respective weights for debit and credit transactions
credit_categories = ["pocket money", "freelancing", "savings", "sharing"]
debit_categories = ["Food", "Travel", "Books", "Stationery", "Electronics"]
debit_weights = [0.3, 0.3, 0.15, 0.1, 0.25]
credit_weights = [0.3, 0.2, 0.1, 0.4]

# Generate synthetic data
data = []
start_date = datetime(2024, 3, 1, 0, 0, 0, tzinfo=pytz.UTC)
end_date = datetime(2024, 3, 31, 0, 0, 0, tzinfo=pytz.UTC)
current_date = start_date

while current_date <= end_date:
    for card_number, limit in cards.items():
        for i in range(0, random.randint(1, 3)):
            credit_debit = "debit" if random.random() < 1 else "credit"  # 80% chance of debit
            amount = random.randint(100, 1000) if credit_debit == "credit" else random.randint(50, 500)
            category = random.choices(debit_categories if credit_debit == "debit" else credit_categories,
                                      weights=debit_weights if credit_debit == "debit" else credit_weights)[0]

            if credit_debit == "debit" and amount > limit:
                amount = limit  # Ensure debit amount does not exceed card limit
            if credit_debit == "credit":
                amount *= 7

            entry = {
                "card_number": card_number,
                "credit_debit": credit_debit,
                "amount": amount,
                "category": category,
                "timestamp": current_date.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Make a POST request to API URL with headers and body
            api_url = "http://35.154.235.185:8000/api/add-transaction/"
            device_id = "faba38ac14dffec8"
            headers = {"DEVICEID": device_id}
            response = requests.post(api_url, headers=headers, json=entry)
            
            # Check if the request was successful
            if response.status_code == 200:
                print("POST request successful")
            else:
                print(f"POST request failed with status code {response.status_code}")

            data.append(entry)

    current_date += timedelta(days=1)
