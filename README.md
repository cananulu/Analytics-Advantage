# Customer Insights Dashboard

An interactive analytics dashboard for a direct mail catalog company, built for MBA coursework.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data (500 customers)
python3 generate_sample_data.py

# 3. Build the dashboard
python3 generate_dashboard.py

# 4. Open dashboard/index.html in your browser
```

## Using Your Own Data

Replace `data/customers.csv` with your own CSV file. The file must contain these columns:

| Column | Description | Example |
|---|---|---|
| `customer_id` | Unique identifier | CUST-0001 |
| `gender` | Male / Female | Female |
| `age` | Customer age | 34 |
| `state` | US state | California |
| `region` | Geographic region | West |
| `income_bracket` | Income range | $50K-$75K |
| `acquisition_channel` | How they were acquired | Direct Mail |
| `product_category` | Primary product purchased | Apparel |
| `order_amount` | Most recent order value ($) | 89.50 |
| `num_orders` | Total orders placed | 3 |
| `first_order_date` | Date of first order | 2023-06-15 |
| `last_order_date` | Date of most recent order | 2025-01-10 |
| `lifetime_value` | Total customer spend ($) | 267.80 |
| `loyalty_member` | Loyalty program member? | Yes / No |
| `satisfaction_score` | 1-5 satisfaction rating | 4 |

Then re-run the dashboard generator:

```bash
python3 generate_dashboard.py
```

You can also pass a custom path:

```bash
python3 generate_dashboard.py path/to/your_data.csv
```

## Project Structure

```
Analytics-Advantage/
├── data/
│   └── customers.csv          # Customer dataset (sample or your own)
├── dashboard/
│   └── index.html             # Generated interactive dashboard
├── generate_sample_data.py    # Creates sample CSV with 500 customers
├── generate_dashboard.py      # Reads CSV and generates the HTML dashboard
├── requirements.txt           # Python dependencies
└── README.md
```

## Dashboard Features

- **8 KPI cards**: Total customers, revenue, avg order value, avg lifetime value, satisfaction score, loyalty rate, avg orders per customer, repeat purchase rate
- **14 interactive charts** covering:
  - Demographics (age, gender, region, top states)
  - Behavioral data (income, acquisition channel, product category, satisfaction)
  - Cross-analysis (revenue by region, LTV by channel, AOV by product, orders by age, LTV by income, satisfaction by loyalty status)
- **6 managerial insight boxes** with actionable recommendations
- Fully responsive — works on desktop, tablet, and mobile
- No server needed — just open the HTML file in a browser
