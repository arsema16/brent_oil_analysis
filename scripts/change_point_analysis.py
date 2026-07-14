# scripts/change_point_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from datetime import datetime
warnings.filterwarnings('ignore')

# Set up paths - get the root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FIGURES_DIR = os.path.join(ROOT_DIR, 'figures')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

print("="*70)
print("BRENT OIL - CHANGE POINT ANALYSIS")
print("="*70)

# ============================================
# STEP 1: LOAD DATA
# ============================================
print("\n[STEP 1] Loading Data...")

data_file = os.path.join(DATA_DIR, 'BrentOilPrices.csv')
df = pd.read_csv(data_file)
print(f"✓ Data loaded: {df.shape[0]} rows")

# Parse dates
def parse_dates(date_str):
    try:
        return pd.to_datetime(date_str, format='%d-%b-%y')
    except:
        try:
            return pd.to_datetime(date_str, format='%b %d, %Y')
        except:
            return pd.NaT

df['Date'] = df['Date'].apply(parse_dates)
df = df.dropna(subset=['Date'])
df = df.sort_values('Date').reset_index(drop=True)

print(f"✓ Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
print(f"✓ Total observations: {len(df)}")

# ============================================
# STEP 2: PREPARE DATA
# ============================================
print("\n[STEP 2] Preparing Data...")

prices = df['Price'].values
dates = df['Date'].values
log_prices = np.log(prices)
log_returns = np.diff(log_prices)

print(f"✓ Price range: ${prices.min():.2f} to ${prices.max():.2f}")
print(f"✓ Mean price: ${prices.mean():.2f}")

# ============================================
# STEP 3: CHANGE POINT DETECTION
# ============================================
print("\n[STEP 3] Detecting Change Points...")

def detect_change_points(data, window_size=30, threshold=2.0):
    n = len(data)
    scores = np.zeros(n)
    changes = []
    
    for i in range(window_size, n - window_size):
        before = data[i-window_size:i]
        after = data[i:i+window_size]
        
        mean_before = np.mean(before)
        mean_after = np.mean(after)
        std_before = np.std(before)
        std_after = np.std(after)
        
        if std_before > 0 and std_after > 0:
            pooled_std = np.sqrt((std_before**2 + std_after**2) / 2)
            if pooled_std > 0:
                t_stat = abs(mean_after - mean_before) / pooled_std
                scores[i] = t_stat
                if t_stat > threshold:
                    changes.append(i)
    
    return changes, scores

window_choice = 60
changes, scores = detect_change_points(prices, window_size=window_choice, threshold=2.0)

print(f"✓ Found {len(changes)} change points using {window_choice}-day window")

# Get change dates (convert numpy datetime64 to pandas datetime)
change_dates = []
change_indices = []

for i in changes:
    if i < len(dates):
        # Convert numpy datetime64 to pandas Timestamp
        date_val = pd.Timestamp(dates[i])
        change_dates.append(date_val)
        change_indices.append(i)

print(f"✓ Converted {len(change_dates)} change points to dates")

print("\nTop 10 Change Points:")
for i in range(min(10, len(change_dates))):
    date_val = change_dates[i]
    idx = change_indices[i]
    price_at_change = prices[idx] if idx < len(prices) else 0
    print(f"  {i+1}. {date_val.strftime('%Y-%m-%d')}: ${price_at_change:.2f}")

# ============================================
# STEP 4: CREATE EVENTS DATASET
# ============================================
print("\n[STEP 4] Creating Events Dataset...")

events_data = [
    ('1990-08-02', 'Gulf War - Kuwait Invasion', 'Geopolitical_Conflict', 'High'),
    ('1991-01-17', 'Operation Desert Storm', 'Geopolitical_Conflict', 'High'),
    ('1997-07-02', 'Asian Financial Crisis', 'Economic_Shock', 'Medium'),
    ('2001-09-11', '9/11 Attacks', 'Geopolitical_Event', 'Medium'),
    ('2003-03-20', 'Iraq War Invasion', 'Geopolitical_Conflict', 'High'),
    ('2008-09-15', 'Global Financial Crisis', 'Economic_Shock', 'Very_High'),
    ('2008-12-17', 'OPEC Production Cuts', 'OPEC_Policy', 'High'),
    ('2011-02-15', 'Arab Spring - Libya', 'Geopolitical_Conflict', 'High'),
    ('2014-06-01', 'Oil Price Crash', 'Market_Event', 'High'),
    ('2016-11-30', 'OPEC+ Agreement', 'OPEC_Policy', 'High'),
    ('2018-05-08', 'US Iran Sanctions', 'Political', 'Medium'),
    ('2020-01-30', 'COVID-19 Pandemic', 'Public_Health', 'Very_High'),
    ('2020-03-06', 'OPEC+ Dispute', 'OPEC_Policy', 'Very_High'),
    ('2022-02-24', 'Russia-Ukraine War', 'Geopolitical_Conflict', 'Very_High')
]

events_df = pd.DataFrame(events_data, 
                        columns=['Date', 'Event_Name', 'Category', 'Expected_Impact'])
events_df['Date'] = pd.to_datetime(events_df['Date'])
events_df.to_csv(os.path.join(DATA_DIR, 'events_dataset.csv'), index=False)
print(f"✓ Created {len(events_df)} events")

print("\nEvents:")
for idx, row in events_df.iterrows():
    print(f"  {row['Date'].strftime('%Y-%m-%d')}: {row['Event_Name']} ({row['Expected_Impact']})")

# ============================================
# STEP 5: ASSOCIATE EVENTS WITH CHANGE POINTS
# ============================================
print("\n[STEP 5] Associating Events with Change Points...")

def find_closest_change(event_date, change_dates, change_indices, max_days=90):
    closest = None
    closest_idx = None
    min_diff = float('inf')
    
    for change_date, change_idx in zip(change_dates, change_indices):
        diff = abs((change_date - event_date).days)
        if diff < min_diff:
            min_diff = diff
            closest = change_date
            closest_idx = change_idx
    
    if closest is not None and min_diff <= max_days:
        if closest_idx is not None and closest_idx >= 30 and closest_idx < len(prices) - 30:
            price_before = prices[closest_idx - 30]
            price_after = prices[closest_idx + 30]
            pct_change = ((price_after / price_before) - 1) * 100
            return closest, min_diff, price_before, price_after, pct_change
    
    return None, None, None, None, None

associations = []

for idx, event in events_df.iterrows():
    event_date = event['Date']
    closest_date, days_diff, price_before, price_after, pct_change = find_closest_change(
        event_date, change_dates, change_indices, max_days=90
    )
    
    if closest_date is not None:
        associations.append({
            'Event': event['Event_Name'],
            'Event_Date': event_date,
            'Category': event['Category'],
            'Expected_Impact': event['Expected_Impact'],
            'Change_Date': closest_date,
            'Days_Difference': days_diff,
            'Price_Before': price_before,
            'Price_After': price_after,
            'Price_Change': price_after - price_before,
            'Percent_Change': pct_change
        })

associations_df = pd.DataFrame(associations)
associations_df.to_csv(os.path.join(DATA_DIR, 'event_associations.csv'), index=False)

print(f"✓ Found {len(associations_df)} event associations")
print("\nAssociations:")
for idx, row in associations_df.head(10).iterrows():
    print(f"\n{row['Event']}")
    print(f"  Event Date: {row['Event_Date'].strftime('%Y-%m-%d')}")
    print(f"  Change Point: {row['Change_Date'].strftime('%Y-%m-%d')}")
    print(f"  Days Apart: {row['Days_Difference']}")
    print(f"  Price Change: ${row['Price_Change']:.2f} ({row['Percent_Change']:.1f}%)")

# ============================================
# STEP 6: CREATE VISUALIZATIONS
# ============================================
print("\n[STEP 6] Creating Visualizations...")

# Figure 1: Change Points
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df['Date'], prices, color='darkblue', linewidth=1, label='Brent Oil Price')

# Mark change points (show first 20)
for i in range(min(20, len(change_dates))):
    change_date = change_dates[i]
    ax.axvline(x=change_date, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)

# Mark events
for idx, row in associations_df.iterrows():
    event_date = row['Event_Date']
    # Find price at event
    event_idx = np.argmin(np.abs(df['Date'] - event_date))
    if event_idx < len(prices):
        price_at_event = prices[event_idx]
        ax.scatter(event_date, price_at_event, color='red', s=100, zorder=5)
        
        label = row['Event'][:20] + '...' if len(row['Event']) > 20 else row['Event']
        ax.text(event_date, price_at_event + 5, label, 
               rotation=45, fontsize=8, ha='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax.set_title('Brent Oil Prices with Events and Change Points', fontsize=16, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD/barrel)')
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'events_vs_changes.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: figures/events_vs_changes.png")

# Figure 2: Impact by Category
fig, ax = plt.subplots(figsize=(12, 6))
category_impact = associations_df.groupby('Category')['Percent_Change'].mean().sort_values(ascending=True)
category_impact.plot(kind='barh', ax=ax, color='steelblue')
ax.set_title('Average Price Change by Event Category', fontsize=14, fontweight='bold')
ax.set_xlabel('Average Percent Change (%)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'impact_by_category.png'), dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: figures/impact_by_category.png")

# ============================================
# STEP 7: SUMMARY
# ============================================
print("\n" + "="*70)
print("SUMMARY REPORT")
print("="*70)

print(f"""
1. DATA OVERVIEW
   - Period: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}
   - Total Observations: {len(prices):,}
   - Price Range: ${prices.min():.2f} to ${prices.max():.2f}
   - Mean Price: ${prices.mean():.2f}

2. CHANGE POINT DETECTION
   - Total Change Points: {len(changes)}
   - Window Size Used: {window_choice} days
   - Threshold: 2.0 standard deviations

3. EVENT ASSOCIATIONS
   - Events Analyzed: {len(events_df)}
   - Events Associated with Changes: {len(associations_df)}
   - Association Rate: {len(associations_df)/len(events_df)*100:.1f}%

4. KEY FINDINGS
   - Most Significant Event: {associations_df.loc[associations_df['Percent_Change'].idxmax(), 'Event']} 
     ({associations_df['Percent_Change'].max():.1f}% change)
   - Highest Impact Category: {associations_df.groupby('Category')['Percent_Change'].mean().idxmax()}

5. OUTPUT FILES
   - data/events_dataset.csv
   - data/event_associations.csv
   - figures/events_vs_changes.png
   - figures/impact_by_category.png
""")

print("="*70)
print("✓ CHANGE POINT ANALYSIS COMPLETE!")
print("="*70)

# Show top events
print("\n" + "="*70)
print("TOP 5 MOST SIGNIFICANT EVENTS")
print("="*70)
top_events = associations_df.sort_values('Percent_Change', ascending=False).head(5)
for idx, row in top_events.iterrows():
    print(f"\n{row['Event']}")
    print(f"  Change: {row['Percent_Change']:.1f}% (${row['Price_Change']:.2f})")
    print(f"  Category: {row['Category']}")
    print(f"  Impact: {row['Expected_Impact']}")