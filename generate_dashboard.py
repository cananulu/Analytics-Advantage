"""
Customer Insights Dashboard Generator
======================================
Reads data/customers.csv and produces dashboard/index.html — a fully
self-contained, interactive dashboard (no server required).

Usage:
    python3 generate_dashboard.py                   # uses data/customers.csv
    python3 generate_dashboard.py path/to/file.csv  # uses a custom CSV

The CSV must contain these columns (case-sensitive):
    customer_id, gender, age, state, region, income_bracket,
    acquisition_channel, product_category, order_amount, num_orders,
    first_order_date, last_order_date, lifetime_value, loyalty_member,
    satisfaction_score
"""

import json
import os
import sys

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------

csv_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "customers.csv")
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found. Run generate_sample_data.py first.")
    sys.exit(1)

df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows from {csv_path}")

# ---------------------------------------------------------------------------
# 2. Compute summary statistics (JSON payloads for the HTML/JS dashboard)
# ---------------------------------------------------------------------------

def safe_json(obj):
    """Serialize, handling numpy/pandas types."""
    return json.dumps(obj, default=str)

# KPIs
total_customers = int(len(df))
total_revenue = float(df["order_amount"].sum())
avg_order_value = float(df["order_amount"].mean())
avg_lifetime_value = float(df["lifetime_value"].mean())
avg_satisfaction = float(df["satisfaction_score"].mean())
loyalty_rate = float((df["loyalty_member"] == "Yes").mean() * 100)
avg_orders = float(df["num_orders"].mean())
repeat_rate = float((df["num_orders"] > 1).mean() * 100)

kpis = {
    "total_customers": total_customers,
    "total_revenue": round(total_revenue, 2),
    "avg_order_value": round(avg_order_value, 2),
    "avg_lifetime_value": round(avg_lifetime_value, 2),
    "avg_satisfaction": round(avg_satisfaction, 2),
    "loyalty_rate": round(loyalty_rate, 1),
    "avg_orders": round(avg_orders, 2),
    "repeat_rate": round(repeat_rate, 1),
}

# Distributions
age_bins = [18, 25, 35, 45, 55, 65, 100]
age_labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)

age_dist = df["age_group"].value_counts().sort_index()
age_data = {"labels": age_dist.index.tolist(), "values": age_dist.values.tolist()}

gender_dist = df["gender"].value_counts()
gender_data = {"labels": gender_dist.index.tolist(), "values": gender_dist.values.tolist()}

region_dist = df["region"].value_counts()
region_data = {"labels": region_dist.index.tolist(), "values": region_dist.values.tolist()}

income_order = ["Under $30K", "$30K-$50K", "$50K-$75K", "$75K-$100K", "$100K-$150K", "Over $150K"]
income_dist = df["income_bracket"].value_counts().reindex(income_order, fill_value=0)
income_data = {"labels": income_dist.index.tolist(), "values": income_dist.values.tolist()}

channel_dist = df["acquisition_channel"].value_counts()
channel_data = {"labels": channel_dist.index.tolist(), "values": channel_dist.values.tolist()}

product_dist = df["product_category"].value_counts()
product_data = {"labels": product_dist.index.tolist(), "values": product_dist.values.tolist()}

satisfaction_dist = df["satisfaction_score"].value_counts().sort_index()
satisfaction_data = {"labels": [str(s) for s in satisfaction_dist.index.tolist()], "values": satisfaction_dist.values.tolist()}

loyalty_dist = df["loyalty_member"].value_counts()
loyalty_data = {"labels": loyalty_dist.index.tolist(), "values": loyalty_dist.values.tolist()}

# Cross-tabs for deeper insights
revenue_by_region = df.groupby("region")["order_amount"].sum().round(2)
revenue_by_region_data = {"labels": revenue_by_region.index.tolist(), "values": revenue_by_region.values.tolist()}

ltv_by_channel = df.groupby("acquisition_channel")["lifetime_value"].mean().round(2)
ltv_by_channel_data = {"labels": ltv_by_channel.index.tolist(), "values": ltv_by_channel.values.tolist()}

avg_order_by_product = df.groupby("product_category")["order_amount"].mean().round(2)
avg_order_by_product_data = {"labels": avg_order_by_product.index.tolist(), "values": avg_order_by_product.values.tolist()}

satisfaction_by_loyalty = df.groupby("loyalty_member")["satisfaction_score"].mean().round(2)
satisfaction_by_loyalty_data = {"labels": satisfaction_by_loyalty.index.tolist(), "values": satisfaction_by_loyalty.values.tolist()}

orders_by_age = df.groupby("age_group")["num_orders"].mean().round(2)
orders_by_age_data = {"labels": orders_by_age.index.tolist(), "values": orders_by_age.values.tolist()}

revenue_by_income = df.groupby("income_bracket")["lifetime_value"].mean().reindex(income_order).round(2)
revenue_by_income_data = {"labels": revenue_by_income.index.tolist(), "values": revenue_by_income.values.tolist()}

# Top states by customer count
top_states = df["state"].value_counts().head(10)
top_states_data = {"labels": top_states.index.tolist(), "values": top_states.values.tolist()}

# ---------------------------------------------------------------------------
# 3. Generate the HTML dashboard
# ---------------------------------------------------------------------------

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Customer Insights Dashboard — Direct Mail Catalog Company</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --primary: #1e3a5f;
    --accent: #2e86de;
    --light-bg: #f0f4f8;
    --card-bg: #ffffff;
    --text: #2d3436;
    --muted: #636e72;
    --border: #dfe6e9;
    --green: #00b894;
    --orange: #fdcb6e;
    --red: #d63031;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--light-bg);
    color: var(--text);
    line-height: 1.6;
  }}
  header {{
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: #fff;
    padding: 28px 32px;
    text-align: center;
  }}
  header h1 {{ font-size: 1.8rem; font-weight: 700; }}
  header p {{ opacity: 0.85; margin-top: 4px; font-size: 0.95rem; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}

  /* KPI cards */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
  }}
  .kpi-card {{
    background: var(--card-bg);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-top: 4px solid var(--accent);
  }}
  .kpi-card .value {{ font-size: 1.7rem; font-weight: 700; color: var(--primary); }}
  .kpi-card .label {{ font-size: 0.82rem; color: var(--muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* Chart grid */
  .chart-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
    gap: 20px;
    margin-bottom: 28px;
  }}
  .chart-card {{
    background: var(--card-bg);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }}
  .chart-card h3 {{
    font-size: 1rem;
    margin-bottom: 12px;
    color: var(--primary);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }}
  canvas {{ width: 100% !important; }}

  /* Insight boxes */
  .insights-section {{ margin-top: 12px; }}
  .insights-section h2 {{
    font-size: 1.25rem; color: var(--primary); margin-bottom: 16px;
    border-left: 4px solid var(--accent); padding-left: 12px;
  }}
  .insight-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }}
  .insight-box {{
    background: var(--card-bg);
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-left: 4px solid var(--green);
  }}
  .insight-box h4 {{ font-size: 0.95rem; color: var(--primary); margin-bottom: 6px; }}
  .insight-box p {{ font-size: 0.88rem; color: var(--muted); }}

  footer {{
    text-align: center;
    padding: 20px;
    color: var(--muted);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }}
  @media (max-width: 500px) {{
    .chart-grid {{ grid-template-columns: 1fr; }}
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
  }}
</style>
</head>
<body>

<header>
  <h1>Customer Insights Dashboard</h1>
  <p>Direct Mail Catalog Company &mdash; {total_customers} customers analyzed</p>
</header>

<div class="container">

<!-- KPI Cards -->
<div class="kpi-grid">
  <div class="kpi-card"><div class="value">{total_customers:,}</div><div class="label">Total Customers</div></div>
  <div class="kpi-card"><div class="value">${total_revenue:,.0f}</div><div class="label">Total Revenue</div></div>
  <div class="kpi-card"><div class="value">${avg_order_value:,.2f}</div><div class="label">Avg Order Value</div></div>
  <div class="kpi-card"><div class="value">${avg_lifetime_value:,.2f}</div><div class="label">Avg Lifetime Value</div></div>
  <div class="kpi-card"><div class="value">{avg_satisfaction:.2f}/5</div><div class="label">Avg Satisfaction</div></div>
  <div class="kpi-card"><div class="value">{loyalty_rate:.1f}%</div><div class="label">Loyalty Members</div></div>
  <div class="kpi-card"><div class="value">{avg_orders:.1f}</div><div class="label">Avg Orders/Customer</div></div>
  <div class="kpi-card"><div class="value">{repeat_rate:.1f}%</div><div class="label">Repeat Purchase Rate</div></div>
</div>

<!-- Charts Row 1: Demographics -->
<div class="chart-grid">
  <div class="chart-card"><h3>Customers by Age Group</h3><canvas id="ageChart"></canvas></div>
  <div class="chart-card"><h3>Customers by Gender</h3><canvas id="genderChart"></canvas></div>
  <div class="chart-card"><h3>Customers by Region</h3><canvas id="regionChart"></canvas></div>
  <div class="chart-card"><h3>Top 10 States by Customer Count</h3><canvas id="stateChart"></canvas></div>
</div>

<!-- Charts Row 2: Behavioral -->
<div class="chart-grid">
  <div class="chart-card"><h3>Income Distribution</h3><canvas id="incomeChart"></canvas></div>
  <div class="chart-card"><h3>Acquisition Channel Mix</h3><canvas id="channelChart"></canvas></div>
  <div class="chart-card"><h3>Product Category Breakdown</h3><canvas id="productChart"></canvas></div>
  <div class="chart-card"><h3>Satisfaction Score Distribution</h3><canvas id="satChart"></canvas></div>
</div>

<!-- Charts Row 3: Cross-analysis -->
<div class="chart-grid">
  <div class="chart-card"><h3>Total Revenue by Region</h3><canvas id="revRegionChart"></canvas></div>
  <div class="chart-card"><h3>Avg Lifetime Value by Acquisition Channel</h3><canvas id="ltvChannelChart"></canvas></div>
  <div class="chart-card"><h3>Avg Order Value by Product Category</h3><canvas id="aovProductChart"></canvas></div>
  <div class="chart-card"><h3>Avg Orders by Age Group</h3><canvas id="orderAgeChart"></canvas></div>
  <div class="chart-card"><h3>Avg Lifetime Value by Income Bracket</h3><canvas id="ltvIncomeChart"></canvas></div>
  <div class="chart-card"><h3>Avg Satisfaction: Loyalty vs Non-Loyalty</h3><canvas id="satLoyaltyChart"></canvas></div>
</div>

<!-- Managerial Insights -->
<div class="insights-section">
  <h2>Key Managerial Insights</h2>
  <div class="insight-grid">
    <div class="insight-box">
      <h4>1. Customer Retention</h4>
      <p>The repeat purchase rate is <strong>{repeat_rate:.1f}%</strong>. Focus retention campaigns on the
         {100 - repeat_rate:.0f}% of one-time buyers — targeted follow-up mailings within 30 days of
         first purchase can lift repeat rates significantly.</p>
    </div>
    <div class="insight-box">
      <h4>2. Loyalty Program ROI</h4>
      <p>Only <strong>{loyalty_rate:.1f}%</strong> of customers are loyalty members. Compare their
         lifetime value to non-members in the chart above — if members are materially more valuable,
         investing in enrollment incentives will improve margins.</p>
    </div>
    <div class="insight-box">
      <h4>3. Channel Effectiveness</h4>
      <p>Use the "Avg LTV by Acquisition Channel" chart to identify which channel brings the most
         valuable customers, not just the most customers. Shift marketing spend toward channels
         with higher LTV.</p>
    </div>
    <div class="insight-box">
      <h4>4. Product Mix Optimization</h4>
      <p>Compare the product category breakdown (volume) with average order value per category.
         Categories with high AOV but low volume may benefit from increased catalog placement.</p>
    </div>
    <div class="insight-box">
      <h4>5. Regional Strategy</h4>
      <p>Cross-reference the revenue-by-region chart with customer counts. Under-penetrated
         regions with strong per-customer revenue are prime candidates for geographic expansion.</p>
    </div>
    <div class="insight-box">
      <h4>6. Age-Based Targeting</h4>
      <p>Examine the average orders by age group chart. If older segments order more frequently,
         direct mail — which skews older in readership — is well-positioned. Digital channels
         may be needed to grow the younger segments.</p>
    </div>
  </div>
</div>

</div>

<footer>
  Customer Insights Dashboard &mdash; Built for MBA Analytics Course &mdash; Data: {total_customers} customers
</footer>

<script>
const PALETTE = ['#2e86de','#00b894','#fdcb6e','#d63031','#6c5ce7','#e17055','#00cec9','#fd79a8','#0984e3','#55efc4'];
const PALETTE2 = ['#1e3a5f','#2e86de','#00b894','#fdcb6e','#e17055','#6c5ce7'];

function barChart(id, data, label, color) {{
  new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{
      labels: data.labels,
      datasets: [{{ label: label, data: data.values, backgroundColor: color || PALETTE[0], borderRadius: 4 }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
  }});
}}

function pieChart(id, data) {{
  new Chart(document.getElementById(id), {{
    type: 'doughnut',
    data: {{
      labels: data.labels,
      datasets: [{{ data: data.values, backgroundColor: PALETTE.slice(0, data.labels.length) }}]
    }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
  }});
}}

function hBarChart(id, data, label, colors) {{
  new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{
      labels: data.labels,
      datasets: [{{ label: label, data: data.values, backgroundColor: colors || PALETTE.slice(0, data.labels.length), borderRadius: 4 }}]
    }},
    options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ beginAtZero: true }} }} }}
  }});
}}

// Demographics
barChart('ageChart', {safe_json(age_data)}, 'Customers', '#2e86de');
pieChart('genderChart', {safe_json(gender_data)});
pieChart('regionChart', {safe_json(region_data)});
hBarChart('stateChart', {safe_json(top_states_data)}, 'Customers');

// Behavioral
barChart('incomeChart', {safe_json(income_data)}, 'Customers', '#6c5ce7');
pieChart('channelChart', {safe_json(channel_data)});
pieChart('productChart', {safe_json(product_data)});
barChart('satChart', {safe_json(satisfaction_data)}, 'Customers', '#00b894');

// Cross-analysis
barChart('revRegionChart', {safe_json(revenue_by_region_data)}, 'Revenue ($)', '#e17055');
hBarChart('ltvChannelChart', {safe_json(ltv_by_channel_data)}, 'Avg LTV ($)');
barChart('aovProductChart', {safe_json(avg_order_by_product_data)}, 'Avg Order ($)', '#fdcb6e');
barChart('orderAgeChart', {safe_json(orders_by_age_data)}, 'Avg Orders', '#0984e3');
barChart('ltvIncomeChart', {safe_json(revenue_by_income_data)}, 'Avg LTV ($)', '#00b894');
barChart('satLoyaltyChart', {safe_json(satisfaction_by_loyalty_data)}, 'Avg Score', '#6c5ce7');
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# 4. Write the dashboard file
# ---------------------------------------------------------------------------

os.makedirs("dashboard", exist_ok=True)
out_path = os.path.join("dashboard", "index.html")
with open(out_path, "w") as f:
    f.write(html)

print(f"Dashboard written to {out_path}")
print("Open this file in any web browser to view the interactive dashboard.")
