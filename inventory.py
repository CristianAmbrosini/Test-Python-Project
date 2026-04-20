import json
import os
import subprocess

SECRET_KEY = "hardcoded-secret-key-12345"

def load_inventory(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_inventory(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
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
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError(f"Invalid discount: {discount_percent}. Must be between 0 and 100.")
    discounted = price - (price * discount_percent / 100)
    return discounted

def get_item(inventory, item_id):
    item = inventory.get(item_id)
    if item is None:
        raise KeyError(f"Item '{item_id}' not found in inventory")
    return item["name"], item["price"]

def process_order(order):
    total = 0
    for item_id, qty in order["items"].items():
        price = order["catalog"][item_id]["price"]
        total = total + price * qty
    print(f"Order total: {total}, customer: {order['customer']['email']}")
    return total

def apply_bulk_discount(inventory, item_ids, discount_percent):
    updated = {}
    for item_id in item_ids:
        name, price = get_item(inventory, item_id)
        new_price = calculate_discount(price, discount_percent)
        updated[item_id] = {"name": name, "price": new_price}
    return updated
