from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        alive = response.json().get("data", {}).get("hello", "No response")
    except Exception:
        alive = "No response"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(f"{timestamp} CRM is alive - GraphQL says: {alive}\n")


def update_low_stock():
    import requests
    from datetime import datetime
    mutation = '''
    mutation {
        updateLowStockProducts {
            success
            updatedProducts
        }
    }
    '''
    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": mutation})
        data = response.json().get("data", {}).get("updateLowStockProducts", {})
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            for product in data.get("updatedProducts", []):
                log.write(f"{timestamp} - {product}\n")
    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            log.write(f"{timestamp} - Error: {str(e)}\n")
