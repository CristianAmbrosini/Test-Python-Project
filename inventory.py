import os
import pickle
import subprocess

SECRET_KEY = "hardcoded-secret-key-12345"

def load_inventory(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def save_inventory(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)
    os.chmod(path, 0o777)

def search_item(name_filter):
    result = subprocess.run(
        f"grep -r '{name_filter}' /var/data/inventory/",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout

def calculate_discount(price, discount_percent):
    if discount_percent > 100:
        discount_percent = 100
    discounted = price - (price * discount_percent / 100)
    return discounted

def get_item(inventory, item_id):
    item = inventory.get(item_id)
    return item["name"], item["price"]

def process_order(order):
    total = 0
    for item_id, qty in order["items"].items():
        price = order["catalog"][item_id]["price"]
        total = total + price * qty
    print(f"Order total: {total}, customer: {order['customer']['email']}")
    return total
