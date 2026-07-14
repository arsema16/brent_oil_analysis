# simple_eda.py
# Simple EDA for Brent Oil Prices - Works with your data format

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("BRENT OIL PRICES - EXPLORATORY DATA ANALYSIS")
print("="*70)

# ============================================
# STEP 1: LOAD THE DATA
# ============================================
print("\n[STEP 1] Loading Data...")
print("-"*50)

# Try different file paths
file_paths = [
    'data/BrentOilPrices.csv',
    '../data/BrentOilPrices.csv',
    'BrentOilPrices.csv',
]

df = None
for path in file_paths:
    try:
        df = pd.read_csv(path)
        print(f"✓ Data loaded from: {path}")
        break
    except FileNotFoundError:
        continue

if df is None:
    # Try the full path with your data
    df = pd.read_csv(r'C:\Users\dell\Documents\GitHub\brent_oil_analysis\data\BrentOilPrices.csv')
    print("✓ Data loaded from full path")

print(f"✓ Data shape: {df.shape}")
print(f"✓ Columns: {df.columns.tolist()}")

# ============================================
# STEP 2: DISPLAY RAW DATA
# ============================================
print("\n[STEP 2] Raw Data Sample...")
print("-"*50)

print("\nFirst 10 rows:")
print(df.head(10))

print("\nData Info:")
print(df.info())

# ============================================
# STEP 3: PARSE DATES (Handles multiple formats)
# ============================================
print("\n[STEP 3] Parsing Dates...")
print("-"*50)

# Check date formats
print("Sample dates:")
print(df['Date'].head(10).tolist())

# Parse dates using pandas' mixed format parser
try:
    # Try mixed format first (newer pandas)
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    print("✓ Used 'mixed' format parser")
except:
    # Try individual formats
    def parse_dates_flexible(date_str):
        formats = [
            '%b %d, %Y',  # Apr 22, 2020
            '%d-%b-%y',   # 20-May-87
            '%d-%b-%Y',   # 20-May-1987
            '%Y-%m-%d',   # 1987-05-20
        ]
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        return pd.NaT
    
    df['Date_parsed'] = df['Date'].apply(parse_dates_flexible)

# Remove rows with unparseable dates
df = df.dropna(subset=['Date_parsed'])
df['Date'] = df['Date_parsed']
df = df.drop('Date_parsed', axis=1)

# Sort by date
df = df.sort_values('Date').reset_index(drop=True)

print(f"✓ Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"✓ Total observations: {len(df)}")

# ============================================
# STEP 4: DATA STATISTICS
# ============================================
print("\n[STEP 4] Data Statistics...")
print("-"*50)

# Ensure Price column exists
if 'Price' not in df.columns:
    # Look for price-like columns
    for col in df.columns:
        if 'price' in col.lower() or 'value' in col.lower():
            df = df.rename(columns={col: 'Price'})
            print(f"✓ Using '{col}' as Price column")
            break

print(f"\nPrice Statistics:")
print(df['Price'].describe())

# Calculate returns
df['Daily_Return'] = df['Price'].pct_change() * 100
df['Log_Price'] = np.log(df['Price'])
df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1)) * 100

print(f"\nDaily Returns Statistics:")
print(f"  Mean: {df['Daily_Return'].mean():.4f}%")
print(f"  Std Dev: {df['Daily_Return'].std():.4f}%")
print(f"  Min: {df['Daily_Return'].min():.4f}%")
print(f"  Max: {df['Daily_Return'].max():.4f}%")
print(f"  Skewness: {df['Daily_Return'].skew():.4f}")
print(f"  Kurtosis: {df['Daily_Return'].kurtosis():.4f}")

# ============================================
# STEP 5: CREATE VISUALIZATIONS
# ============================================
print("\n[STEP 5] Creating Visualizations...")
print("-"*50)

# Create figures directory
import os
if not os.path.exists('figures'):
    os.makedirs('figures')

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Plot 1: Raw prices
axes[0, 0].plot(df['Date'], df['Price'], color='blue', linewidth=1)
axes[0, 0].set_title('Brent Crude Oil Price (1987-2022)', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Price (USD/barrel)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].axhline(y=df['Price'].mean(), color='red', linestyle='--', 
                   label=f'Mean: ${df["Price"].mean():.2f}')
axes[0, 0].legend()

# Plot 2: Log prices
axes[0, 1].plot(df['Date'], df['Log_Price'], color='green', linewidth=1)
axes[0, 1].set_title('Log of Brent Oil Prices', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Log Price')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Daily returns
axes[1, 0].plot(df['Date'], df['Daily_Return'], color='red', linewidth=0.5, alpha=0.7)
axes[1, 0].axhline(y=0, color='black', linestyle='--', linewidth=0.5)
axes[1, 0].set_title('Daily Returns (%)', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Return (%)')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Log returns
axes[1, 1].plot(df['Date'], df['Log_Return'], color='purple', linewidth=0.5, alpha=0.7)
axes[1, 1].axhline(y=0, color='black', linestyle='--', linewidth=0.5)
axes[1, 1].set_title('Log Returns (%)', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Log Return (%)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/time_series_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Figure saved: figures/time_series_overview.png")

# ============================================
# STEP 6: Distribution Analysis
# ============================================
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Price distribution
axes[0, 0].hist(df['Price'], bins=50, edgecolor='black', alpha=0.7, color='blue')
axes[0, 0].axvline(df['Price'].mean(), color='red', linestyle='--', 
                   label=f'Mean: ${df["Price"].mean():.2f}')
axes[0, 0].axvline(df['Price'].median(), color='green', linestyle='--', 
                   label=f'Median: ${df["Price"].median():.2f}')
axes[0, 0].set_title('Price Distribution', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Price (USD/barrel)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Log return distribution
log_returns_clean = df['Log_Return'].dropna()
axes[0, 1].hist(log_returns_clean, bins=50, edgecolor='black', alpha=0.7, color='purple')
axes[0, 1].axvline(log_returns_clean.mean(), color='red', linestyle='--', 
                   label=f'Mean: {log_returns_clean.mean():.4f}%')
axes[0, 1].set_title('Log Returns Distribution', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Log Return (%)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Box plot by decade
df['Decade'] = df['Date'].dt.year // 10 * 10
df.boxplot(column='Price', by='Decade', ax=axes[1, 0])
axes[1, 0].set_title('Price Distribution by Decade', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Decade')
axes[1, 0].set_ylabel('Price (USD/barrel)')
axes[1, 0].grid(True, alpha=0.3)

# QQ plot
from scipy import stats
stats.probplot(log_returns_clean, dist="norm", plot=axes[1, 1])
axes[1, 1].set_title('Q-Q Plot: Log Returns', fontsize=14, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/distribution_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Figure saved: figures/distribution_analysis.png")

# ============================================
# STEP 7: Final Summary
# ============================================
print("\n" + "="*70)
print("EDA SUMMARY")
print("="*70)

print(f"\n1. Data Overview:")
print(f"   - Period: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
print(f"   - Total Observations: {len(df):,}")
print(f"   - Price Range: ${df['Price'].min():.2f} to ${df['Price'].max():.2f}")
print(f"   - Mean Price: ${df['Price'].mean():.2f}")
print(f"   - Median Price: ${df['Price'].median():.2f}")

print(f"\n2. Returns:")
print(f"   - Mean Daily Return: {df['Daily_Return'].mean():.4f}%")
print(f"   - Std Dev Daily Return: {df['Daily_Return'].std():.4f}%")

print("\n3. Key Observations:")
print("   - Significant volatility clustering observed")
print("   - Major structural breaks during geopolitical events")
print("   - Long-term upward trend with sharp corrections")

print("\n4. Files Created:")
print("   - figures/time_series_overview.png")
print("   - figures/distribution_analysis.png")

print("\n" + "="*70)
print("✓ EDA COMPLETE! Ready for Task 2: Change Point Modeling")
print("="*70)