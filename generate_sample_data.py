"""
Generate a sample customer dataset for a direct mail catalog company.
Run this script to create 'data/customers.csv' with realistic sample data.

You can replace data/customers.csv with your own file — just keep the same
column names (or update generate_dashboard.py to match your columns).
"""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)

NUM_CUSTOMERS = 500

REGIONS = {
    "Northeast": ["New York", "Massachusetts", "Pennsylvania", "Connecticut", "New Jersey"],
    "Southeast": ["Florida", "Georgia", "North Carolina", "Virginia", "Tennessee"],
    "Midwest": ["Illinois", "Ohio", "Michigan", "Minnesota", "Indiana"],
    "Southwest": ["Texas", "Arizona", "New Mexico", "Oklahoma", "Colorado"],
    "West": ["California", "Washington", "Oregon", "Nevada", "Utah"],
}

CHANNELS = ["Direct Mail", "Email", "Web", "Phone", "Referral"]
PRODUCT_CATEGORIES = ["Apparel", "Home & Garden", "Electronics", "Kitchen", "Outdoor", "Books & Media"]
GENDERS = ["Male", "Female"]

def random_date(start_year=2023, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    rand_days = random.randint(0, delta.days)
    return (start + timedelta(days=rand_days)).strftime("%Y-%m-%d")

def generate_customers(n):
    rows = []
    for i in range(1, n + 1):
        region = random.choice(list(REGIONS.keys()))
        state = random.choice(REGIONS[region])
        gender = random.choice(GENDERS)
        age = random.randint(22, 75)
        income_bracket = random.choices(
            ["Under $30K", "$30K-$50K", "$50K-$75K", "$75K-$100K", "$100K-$150K", "Over $150K"],
            weights=[5, 15, 25, 25, 20, 10],
        )[0]
        channel = random.choices(CHANNELS, weights=[30, 25, 20, 15, 10])[0]
        product = random.choices(
            PRODUCT_CATEGORIES,
            weights=[25, 20, 15, 18, 12, 10],
        )[0]

        # Order value correlates loosely with income
        income_multiplier = {
            "Under $30K": 0.6, "$30K-$50K": 0.8, "$50K-$75K": 1.0,
            "$75K-$100K": 1.2, "$100K-$150K": 1.5, "Over $150K": 2.0,
        }
        base_order = random.uniform(15, 200)
        order_amount = round(base_order * income_multiplier[income_bracket], 2)

        num_orders = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            weights=[25, 20, 15, 12, 10, 7, 5, 3, 2, 1],
        )[0]

        first_order_date = random_date(2023, 2024)
        last_order_date = random_date(2024, 2025) if num_orders > 1 else first_order_date

        lifetime_value = round(order_amount * num_orders * random.uniform(0.8, 1.2), 2)

        loyalty_member = random.choices(["Yes", "No"], weights=[35, 65])[0]

        satisfaction = random.choices(
            [1, 2, 3, 4, 5],
            weights=[3, 7, 20, 40, 30],
        )[0]

        rows.append({
            "customer_id": f"CUST-{i:04d}",
            "gender": gender,
            "age": age,
            "state": state,
            "region": region,
            "income_bracket": income_bracket,
            "acquisition_channel": channel,
            "product_category": product,
            "order_amount": order_amount,
            "num_orders": num_orders,
            "first_order_date": first_order_date,
            "last_order_date": last_order_date,
            "lifetime_value": lifetime_value,
            "loyalty_member": loyalty_member,
            "satisfaction_score": satisfaction,
        })
    return rows

def main():
    os.makedirs("data", exist_ok=True)
    customers = generate_customers(NUM_CUSTOMERS)
    filepath = os.path.join("data", "customers.csv")
    fieldnames = list(customers[0].keys())
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customers)
    print(f"Generated {len(customers)} customer records -> {filepath}")

if __name__ == "__main__":
    main()
