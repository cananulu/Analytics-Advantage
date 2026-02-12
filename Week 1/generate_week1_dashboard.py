"""
Week 1 — Customer Insights Dashboard Generator
================================================
Reads direct_marketing.csv and produces an interactive HTML dashboard
with business insights for MBA class discussion.

Dataset: 1,000 customers of a direct mail catalog company.
Columns: AmountSpent, Age, Gender, OwnHome, Married, Location,
         Salary, Children, History, Catalogs, rnd1, rnd2

Usage:
    python3 generate_week1_dashboard.py
"""

import json
import os
import sys

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(SCRIPT_DIR, "data", "direct_marketing.csv")
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    sys.exit(1)

df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows from {csv_path}")

# Clean up: History has some NaN values — label them "New" (no prior purchase history)
df["History"] = df["History"].fillna("New")

# ---------------------------------------------------------------------------
# 2. Compute all analytics
# ---------------------------------------------------------------------------

def sj(obj):
    """JSON-serialize, handling numpy/pandas types."""
    return json.dumps(obj, default=lambda x: int(x) if isinstance(x, (np.integer,)) else float(x) if isinstance(x, (np.floating,)) else str(x))

# --- KPIs ---
total_customers = len(df)
total_revenue = round(float(df["AmountSpent"].sum()), 2)
avg_spend = round(float(df["AmountSpent"].mean()), 2)
median_spend = round(float(df["AmountSpent"].median()), 2)
avg_salary = round(float(df["Salary"].mean()), 2)
median_salary = round(float(df["Salary"].median()), 2)
avg_catalogs = round(float(df["Catalogs"].mean()), 1)
pct_homeowners = round(float((df["OwnHome"] == "Own").mean() * 100), 1)
pct_married = round(float((df["Married"] == "Married").mean() * 100), 1)
avg_children = round(float(df["Children"].mean()), 2)
pct_high_history = round(float((df["History"] == "High").mean() * 100), 1)

# --- Distributions ---
gender_counts = df["Gender"].value_counts()
gender_data = {"labels": gender_counts.index.tolist(), "values": gender_counts.values.tolist()}

age_counts = df["Age"].value_counts().reindex(["Young", "Middle", "Old"], fill_value=0)
age_data = {"labels": age_counts.index.tolist(), "values": age_counts.values.tolist()}

home_counts = df["OwnHome"].value_counts()
home_data = {"labels": home_counts.index.tolist(), "values": home_counts.values.tolist()}

married_counts = df["Married"].value_counts()
married_data = {"labels": married_counts.index.tolist(), "values": married_counts.values.tolist()}

location_counts = df["Location"].value_counts()
location_data = {"labels": location_counts.index.tolist(), "values": location_counts.values.tolist()}

history_order = ["New", "Low", "Medium", "High"]
history_counts = df["History"].value_counts().reindex(history_order, fill_value=0)
history_data = {"labels": history_counts.index.tolist(), "values": history_counts.values.tolist()}

children_counts = df["Children"].value_counts().sort_index()
children_data = {"labels": [str(c) for c in children_counts.index.tolist()], "values": children_counts.values.tolist()}

catalog_counts = df["Catalogs"].value_counts().sort_index()
catalog_data = {"labels": [str(c) for c in catalog_counts.index.tolist()], "values": catalog_counts.values.tolist()}

# Salary distribution (binned)
salary_bins = [0, 25000, 50000, 75000, 100000, 125000, 200000]
salary_labels = ["<$25K", "$25K-$50K", "$50K-$75K", "$75K-$100K", "$100K-$125K", "$125K+"]
df["salary_bin"] = pd.cut(df["Salary"], bins=salary_bins, labels=salary_labels, right=False)
salary_dist = df["salary_bin"].value_counts().reindex(salary_labels, fill_value=0)
salary_data = {"labels": salary_dist.index.tolist(), "values": salary_dist.values.tolist()}

# AmountSpent distribution (binned)
spend_bins = [0, 250, 500, 1000, 1500, 2000, 3000, 7000]
spend_labels = ["<$250", "$250-$500", "$500-$1K", "$1K-$1.5K", "$1.5K-$2K", "$2K-$3K", "$3K+"]
df["spend_bin"] = pd.cut(df["AmountSpent"], bins=spend_bins, labels=spend_labels, right=False)
spend_dist = df["spend_bin"].value_counts().reindex(spend_labels, fill_value=0)
spend_data = {"labels": spend_dist.index.tolist(), "values": spend_dist.values.tolist()}

# --- Cross-Analysis (the most valuable charts for managers) ---

# Avg spend by age group
spend_by_age = df.groupby("Age")["AmountSpent"].mean().reindex(["Young", "Middle", "Old"]).round(2)
spend_by_age_data = {"labels": spend_by_age.index.tolist(), "values": spend_by_age.values.tolist()}

# Avg spend by gender
spend_by_gender = df.groupby("Gender")["AmountSpent"].mean().round(2)
spend_by_gender_data = {"labels": spend_by_gender.index.tolist(), "values": spend_by_gender.values.tolist()}

# Avg spend by homeownership
spend_by_home = df.groupby("OwnHome")["AmountSpent"].mean().round(2)
spend_by_home_data = {"labels": spend_by_home.index.tolist(), "values": spend_by_home.values.tolist()}

# Avg spend by marital status
spend_by_married = df.groupby("Married")["AmountSpent"].mean().round(2)
spend_by_married_data = {"labels": spend_by_married.index.tolist(), "values": spend_by_married.values.tolist()}

# Avg spend by location
spend_by_location = df.groupby("Location")["AmountSpent"].mean().round(2)
spend_by_location_data = {"labels": spend_by_location.index.tolist(), "values": spend_by_location.values.tolist()}

# Avg spend by purchase history
spend_by_history = df.groupby("History")["AmountSpent"].mean().reindex(history_order).round(2)
spend_by_history_data = {"labels": spend_by_history.index.tolist(), "values": spend_by_history.values.tolist()}

# Avg spend by number of children
spend_by_children = df.groupby("Children")["AmountSpent"].mean().round(2)
spend_by_children_data = {"labels": [str(c) for c in spend_by_children.index.tolist()], "values": spend_by_children.values.tolist()}

# Avg spend by catalogs received
spend_by_catalogs = df.groupby("Catalogs")["AmountSpent"].mean().round(2)
spend_by_catalogs_data = {"labels": [str(c) for c in spend_by_catalogs.index.tolist()], "values": spend_by_catalogs.values.tolist()}

# Salary vs AmountSpent scatter data (sample for performance)
scatter_sample = df[["Salary", "AmountSpent"]].sample(n=min(500, len(df)), random_state=42)
scatter_data = [{"x": int(r["Salary"]), "y": int(r["AmountSpent"])} for _, r in scatter_sample.iterrows()]

# Avg salary by age group
salary_by_age = df.groupby("Age")["Salary"].mean().reindex(["Young", "Middle", "Old"]).round(0)
salary_by_age_data = {"labels": salary_by_age.index.tolist(), "values": salary_by_age.values.tolist()}

# History breakdown by age
history_by_age = df.groupby(["Age", "History"]).size().unstack(fill_value=0).reindex(
    index=["Young", "Middle", "Old"], columns=history_order, fill_value=0)
history_by_age_data = {
    "labels": history_by_age.index.tolist(),
    "datasets": [{"label": col, "data": history_by_age[col].values.tolist()} for col in history_order]
}

# Catalog effectiveness: avg spend per catalog sent
df["spend_per_catalog"] = df["AmountSpent"] / df["Catalogs"]
spend_per_cat_by_history = df.groupby("History")["spend_per_catalog"].mean().reindex(history_order).round(2)
spend_per_cat_data = {"labels": spend_per_cat_by_history.index.tolist(), "values": spend_per_cat_by_history.values.tolist()}

# Correlation matrix (key numeric variables)
corr_cols = ["AmountSpent", "Salary", "Children", "Catalogs"]
corr_matrix = df[corr_cols].corr().round(3)
corr_data = {
    "labels": corr_cols,
    "matrix": corr_matrix.values.tolist()
}

# ---------------------------------------------------------------------------
# 3. Generate HTML Dashboard
# ---------------------------------------------------------------------------

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Week 1 — Direct Mail Customer Insights Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --primary: #1a365d; --accent: #2b6cb0; --accent2: #3182ce;
    --bg: #f7fafc; --card: #ffffff; --text: #1a202c; --muted: #718096;
    --border: #e2e8f0; --green: #38a169; --orange: #dd6b20; --red: #e53e3e;
    --purple: #805ad5; --teal: #319795;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI',system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--text); }}
  header {{
    background:linear-gradient(135deg, var(--primary) 0%, var(--accent) 60%, var(--accent2) 100%);
    color:#fff; padding:32px; text-align:center;
  }}
  header h1 {{ font-size:2rem; font-weight:800; letter-spacing:-0.5px; }}
  header p {{ opacity:.85; margin-top:6px; font-size:1rem; }}
  .tag {{ display:inline-block; background:rgba(255,255,255,.2); border-radius:20px; padding:4px 14px; font-size:.8rem; margin-top:8px; }}
  .container {{ max-width:1440px; margin:0 auto; padding:24px; }}

  .section-title {{
    font-size:1.15rem; font-weight:700; color:var(--primary); margin:28px 0 16px;
    border-left:4px solid var(--accent); padding-left:12px;
  }}

  .kpi-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:14px; margin-bottom:8px; }}
  .kpi {{ background:var(--card); border-radius:10px; padding:18px 14px; text-align:center;
          box-shadow:0 1px 6px rgba(0,0,0,.06); border-top:4px solid var(--accent); }}
  .kpi .val {{ font-size:1.6rem; font-weight:800; color:var(--primary); }}
  .kpi .lbl {{ font-size:.75rem; color:var(--muted); margin-top:3px; text-transform:uppercase; letter-spacing:.6px; }}

  .grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(420px,1fr)); gap:18px; margin-bottom:8px; }}
  .grid3 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:18px; margin-bottom:8px; }}
  .card {{ background:var(--card); border-radius:10px; padding:20px; box-shadow:0 1px 6px rgba(0,0,0,.06); }}
  .card h3 {{ font-size:.95rem; color:var(--primary); border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:12px; }}
  canvas {{ width:100%!important; }}

  .insight-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:14px; margin-bottom:28px; }}
  .insight {{ background:var(--card); border-radius:10px; padding:18px 20px;
              box-shadow:0 1px 6px rgba(0,0,0,.06); border-left:4px solid var(--green); }}
  .insight.warn {{ border-left-color: var(--orange); }}
  .insight.action {{ border-left-color: var(--purple); }}
  .insight h4 {{ font-size:.92rem; color:var(--primary); margin-bottom:5px; }}
  .insight p {{ font-size:.85rem; color:var(--muted); line-height:1.55; }}
  .insight strong {{ color:var(--text); }}

  .corr-table {{ width:100%; border-collapse:collapse; font-size:.85rem; }}
  .corr-table th, .corr-table td {{ padding:10px 12px; text-align:center; border:1px solid var(--border); }}
  .corr-table th {{ background:var(--primary); color:#fff; font-weight:600; }}

  footer {{ text-align:center; padding:20px; color:var(--muted); font-size:.78rem; border-top:1px solid var(--border); margin-top:20px; }}
  @media(max-width:480px){{ .grid2,.grid3{{grid-template-columns:1fr;}} .kpi-grid{{grid-template-columns:repeat(2,1fr);}} }}
</style>
</head>
<body>

<header>
  <h1>Week 1: Customer Insights Dashboard</h1>
  <p>Direct Mail Catalog Company &mdash; Customer Analytics for Managerial Decision-Making</p>
  <span class="tag">MBA Analytics &bull; {total_customers:,} Customers</span>
</header>

<div class="container">

<!-- ===== KPIs ===== -->
<div class="section-title">Key Performance Indicators</div>
<div class="kpi-grid">
  <div class="kpi"><div class="val">{total_customers:,}</div><div class="lbl">Total Customers</div></div>
  <div class="kpi"><div class="val">${total_revenue:,.0f}</div><div class="lbl">Total Revenue</div></div>
  <div class="kpi"><div class="val">${avg_spend:,.0f}</div><div class="lbl">Avg Amount Spent</div></div>
  <div class="kpi"><div class="val">${median_spend:,.0f}</div><div class="lbl">Median Spent</div></div>
  <div class="kpi"><div class="val">${avg_salary:,.0f}</div><div class="lbl">Avg Salary</div></div>
  <div class="kpi"><div class="val">{avg_catalogs:.0f}</div><div class="lbl">Avg Catalogs Sent</div></div>
  <div class="kpi"><div class="val">{pct_homeowners:.0f}%</div><div class="lbl">Homeowners</div></div>
  <div class="kpi"><div class="val">{pct_married:.0f}%</div><div class="lbl">Married</div></div>
  <div class="kpi"><div class="val">{avg_children:.1f}</div><div class="lbl">Avg Children</div></div>
  <div class="kpi"><div class="val">{pct_high_history:.0f}%</div><div class="lbl">High-History Buyers</div></div>
</div>

<!-- ===== Customer Demographics ===== -->
<div class="section-title">Customer Demographics</div>
<div class="grid2">
  <div class="card"><h3>Age Group Distribution</h3><canvas id="ageChart"></canvas></div>
  <div class="card"><h3>Gender Distribution</h3><canvas id="genderChart"></canvas></div>
  <div class="card"><h3>Homeownership</h3><canvas id="homeChart"></canvas></div>
  <div class="card"><h3>Marital Status</h3><canvas id="marriedChart"></canvas></div>
  <div class="card"><h3>Location (Proximity to Store)</h3><canvas id="locationChart"></canvas></div>
  <div class="card"><h3>Number of Children</h3><canvas id="childrenChart"></canvas></div>
  <div class="card"><h3>Salary Distribution</h3><canvas id="salaryChart"></canvas></div>
  <div class="card"><h3>Spending Distribution</h3><canvas id="spendChart"></canvas></div>
</div>

<!-- ===== Purchasing Behavior ===== -->
<div class="section-title">Purchasing Behavior</div>
<div class="grid2">
  <div class="card"><h3>Purchase History Level</h3><canvas id="historyChart"></canvas></div>
  <div class="card"><h3>Catalogs Received</h3><canvas id="catalogChart"></canvas></div>
</div>

<!-- ===== Spending Drivers (Cross-Analysis) ===== -->
<div class="section-title">What Drives Customer Spending?</div>
<div class="grid2">
  <div class="card"><h3>Avg Amount Spent by Age Group</h3><canvas id="spendAgeChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Gender</h3><canvas id="spendGenderChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Homeownership</h3><canvas id="spendHomeChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Marital Status</h3><canvas id="spendMarriedChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Location</h3><canvas id="spendLocationChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Purchase History</h3><canvas id="spendHistoryChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Number of Children</h3><canvas id="spendChildrenChart"></canvas></div>
  <div class="card"><h3>Avg Amount Spent by Catalogs Received</h3><canvas id="spendCatalogsChart"></canvas></div>
</div>

<!-- ===== Advanced Analytics ===== -->
<div class="section-title">Advanced Analytics</div>
<div class="grid2">
  <div class="card"><h3>Salary vs. Amount Spent (Scatter)</h3><canvas id="scatterChart"></canvas></div>
  <div class="card"><h3>Avg Salary by Age Group</h3><canvas id="salaryAgeChart"></canvas></div>
  <div class="card"><h3>Purchase History Breakdown by Age</h3><canvas id="historyAgeChart"></canvas></div>
  <div class="card"><h3>Spending per Catalog by History Level</h3><canvas id="spendPerCatChart"></canvas></div>
</div>

<!-- ===== Correlation Matrix ===== -->
<div class="section-title">Correlation Matrix (Key Numeric Variables)</div>
<div class="grid3">
  <div class="card" style="grid-column: span 1;">
    <h3>Pearson Correlations</h3>
    <table class="corr-table">
      <tr><th></th>{"".join(f"<th>{c}</th>" for c in corr_data["labels"])}</tr>
      {"".join("<tr><th>" + corr_data["labels"][i] + "</th>" + "".join(
          f'<td style="background:rgba({("43,133,43" if v > 0 else "211,47,47")},{abs(v)*0.4:.2f})">{v:.3f}</td>'
          for v in row
      ) + "</tr>" for i, row in enumerate(corr_data["matrix"]))}
    </table>
    <p style="font-size:.8rem;color:var(--muted);margin-top:10px;">
      Green = positive correlation; Red = negative. Darker = stronger relationship.
    </p>
  </div>
</div>

<!-- ===== Managerial Insights ===== -->
<div class="section-title">Managerial Insights &amp; Discussion Questions</div>
<div class="insight-grid">
  <div class="insight">
    <h4>1. Catalog Volume Drives Spending</h4>
    <p>Customers who received <strong>more catalogs spent significantly more</strong>. This is the single most actionable lever — but managers must weigh catalog printing/mailing costs against incremental revenue. <em>Discussion: At what point do marginal catalog costs exceed marginal revenue?</em></p>
  </div>
  <div class="insight">
    <h4>2. Purchase History Predicts Future Value</h4>
    <p>Customers with <strong>High purchase history</strong> spend far more than Low or New customers. This suggests a strong case for <strong>customer segmentation</strong> — target high-history customers with premium catalogs and new customers with introductory offers.</p>
  </div>
  <div class="insight warn">
    <h4>3. The "New Customer" Opportunity</h4>
    <p><strong>{round((df['History']=='New').mean()*100,1)}%</strong> of customers have no prior purchase history. These are first-time buyers. Their conversion into repeat customers is critical. <em>What onboarding strategies would you recommend?</em></p>
  </div>
  <div class="insight">
    <h4>4. Salary and Spending Relationship</h4>
    <p>The scatter plot shows a <strong>positive correlation between salary and spending</strong>. Higher-income customers are more valuable. Consider whether the company should focus acquisition on higher-income demographics.</p>
  </div>
  <div class="insight warn">
    <h4>5. Children Reduce Spending</h4>
    <p>Customers with <strong>more children tend to spend less</strong>. Household budget competition from child-related expenses likely reduces discretionary catalog spending. <em>Should the product mix be adjusted for family customers?</em></p>
  </div>
  <div class="insight action">
    <h4>6. Location Matters</h4>
    <p>Compare spending by location (Close vs. Far). Does proximity to a physical store affect catalog purchasing behavior? This has implications for <strong>where to target direct mail campaigns geographically</strong>.</p>
  </div>
  <div class="insight action">
    <h4>7. Age Group Strategy</h4>
    <p>Middle-aged and older customers tend to have <strong>higher salaries and spending</strong>. The young segment earns less but may have long-term value. <em>How should marketing budgets be allocated across age segments?</em></p>
  </div>
  <div class="insight">
    <h4>8. Homeownership as a Proxy</h4>
    <p>Homeowners tend to spend differently than renters. Homeownership may serve as a <strong>useful proxy variable</strong> for financial stability in targeting models. <em>What other demographic proxies could improve targeting?</em></p>
  </div>
</div>

</div>

<footer>Week 1 — Customer Insights Dashboard &bull; MBA Analytics Course &bull; {total_customers:,} customers analyzed</footer>

<script>
const P = ['#2b6cb0','#38a169','#dd6b20','#e53e3e','#805ad5','#d69e2e','#319795','#d53f8c','#3182ce','#68d391'];
const P2 = ['#2b6cb0','#38a169','#dd6b20','#e53e3e'];

function bar(id, d, lbl, clr) {{
  new Chart(document.getElementById(id), {{
    type:'bar',
    data:{{ labels:d.labels, datasets:[{{ label:lbl, data:d.values, backgroundColor:clr||P[0], borderRadius:5 }}] }},
    options:{{ responsive:true, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ beginAtZero:true }} }} }}
  }});
}}

function pie(id, d) {{
  new Chart(document.getElementById(id), {{
    type:'doughnut',
    data:{{ labels:d.labels, datasets:[{{ data:d.values, backgroundColor:P.slice(0,d.labels.length) }}] }},
    options:{{ responsive:true, plugins:{{ legend:{{ position:'bottom' }} }} }}
  }});
}}

function hbar(id, d, lbl, clr) {{
  new Chart(document.getElementById(id), {{
    type:'bar',
    data:{{ labels:d.labels, datasets:[{{ label:lbl, data:d.values, backgroundColor:clr||P.slice(0,d.labels.length), borderRadius:5 }}] }},
    options:{{ indexAxis:'y', responsive:true, plugins:{{ legend:{{ display:false }} }}, scales:{{ x:{{ beginAtZero:true }} }} }}
  }});
}}

// Demographics
bar('ageChart', {sj(age_data)}, 'Customers', P.slice(0,3));
pie('genderChart', {sj(gender_data)});
pie('homeChart', {sj(home_data)});
pie('marriedChart', {sj(married_data)});
pie('locationChart', {sj(location_data)});
bar('childrenChart', {sj(children_data)}, 'Customers', '#805ad5');
bar('salaryChart', {sj(salary_data)}, 'Customers', '#319795');
bar('spendChart', {sj(spend_data)}, 'Customers', '#2b6cb0');

// Purchasing behavior
bar('historyChart', {sj(history_data)}, 'Customers', P2);
bar('catalogChart', {sj(catalog_data)}, 'Customers', '#dd6b20');

// Spending drivers
bar('spendAgeChart', {sj(spend_by_age_data)}, 'Avg $', P.slice(0,3));
bar('spendGenderChart', {sj(spend_by_gender_data)}, 'Avg $', ['#2b6cb0','#d53f8c']);
bar('spendHomeChart', {sj(spend_by_home_data)}, 'Avg $', ['#38a169','#dd6b20']);
bar('spendMarriedChart', {sj(spend_by_married_data)}, 'Avg $', ['#805ad5','#319795']);
bar('spendLocationChart', {sj(spend_by_location_data)}, 'Avg $', ['#2b6cb0','#e53e3e']);
bar('spendHistoryChart', {sj(spend_by_history_data)}, 'Avg $', P2);
bar('spendChildrenChart', {sj(spend_by_children_data)}, 'Avg $', '#805ad5');
bar('spendCatalogsChart', {sj(spend_by_catalogs_data)}, 'Avg $', '#dd6b20');

// Advanced
new Chart(document.getElementById('scatterChart'), {{
  type:'scatter',
  data:{{ datasets:[{{ label:'Customer', data:{json.dumps(scatter_data)},
    backgroundColor:'rgba(43,108,176,0.4)', borderColor:'rgba(43,108,176,0.8)', pointRadius:3 }}] }},
  options:{{ responsive:true, plugins:{{ legend:{{ display:false }} }},
    scales:{{ x:{{ title:{{ display:true, text:'Salary ($)' }} }}, y:{{ title:{{ display:true, text:'Amount Spent ($)' }}, beginAtZero:true }} }} }}
}});

bar('salaryAgeChart', {sj(salary_by_age_data)}, 'Avg Salary', P.slice(0,3));

// Stacked bar: history by age
new Chart(document.getElementById('historyAgeChart'), {{
  type:'bar',
  data:{{
    labels: {json.dumps(history_by_age_data["labels"])},
    datasets: [
      {{label:'New', data:{json.dumps(history_by_age_data["datasets"][0]["data"])}, backgroundColor:P2[0], borderRadius:3}},
      {{label:'Low', data:{json.dumps(history_by_age_data["datasets"][1]["data"])}, backgroundColor:P2[1], borderRadius:3}},
      {{label:'Medium', data:{json.dumps(history_by_age_data["datasets"][2]["data"])}, backgroundColor:P2[2], borderRadius:3}},
      {{label:'High', data:{json.dumps(history_by_age_data["datasets"][3]["data"])}, backgroundColor:P2[3], borderRadius:3}}
    ]
  }},
  options:{{ responsive:true, scales:{{ x:{{ stacked:true }}, y:{{ stacked:true, beginAtZero:true }} }}, plugins:{{ legend:{{ position:'bottom' }} }} }}
}});

bar('spendPerCatChart', {sj(spend_per_cat_data)}, '$/Catalog', P2);
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# 4. Write output
# ---------------------------------------------------------------------------

out_dir = os.path.join(SCRIPT_DIR, "dashboard")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "index.html")
with open(out_path, "w") as f:
    f.write(html)

print(f"Dashboard written to {out_path}")
print("Open this file in any web browser to view the interactive dashboard.")
