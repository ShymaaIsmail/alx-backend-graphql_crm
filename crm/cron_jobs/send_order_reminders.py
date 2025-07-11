import requests
from datetime import datetime, timedelta

query = '''
{
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
''' % (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

response = requests.post(
    "http://localhost:8000/graphql",
    json={"query": query}
)
orders = response.json().get("data", {}).get("orders", [])

log_path = "/tmp/order_reminders_log.txt"
with open(log_path, "a") as log:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for order in orders:
        log.write(f"{timestamp} - Order ID: {order['id']}, Email: {order['customer']['email']}\n")
print("Order reminders processed!")