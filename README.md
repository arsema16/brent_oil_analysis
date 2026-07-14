# 📊 Brent Oil Price Analysis

## Project Overview
Comprehensive analysis of Brent crude oil prices (1987-2022) to identify and quantify the impact of major geopolitical and economic events using statistical change point detection.

## 🎯 Objectives
- Identify key events impacting Brent oil prices over the past decade
- Quantify event effects using statistical methods
- Provide data-driven insights for investors and policymakers
- Build an interactive dashboard for exploring price-event relationships

## 📁 Repository Structure
```
brent_oil_analysis/
├── data/
│ ├── BrentOilPrices.csv # Raw price data (1987-2022)
│ ├── events_dataset.csv # 14 key events with metadata
│ └── event_associations.csv # Event-change point associations
├── notebooks/
│ ├── 01_eda.ipynb # Exploratory data analysis
│ └── 02_change_point_model.ipynb # Change point detection
├── scripts/
│ └── change_point_analysis.py # Change point detection script
├── backend/ # Flask API backend
│ ├── app.py
│ ├── api/routes.py
│ └── models/data_loader.py
├── frontend/ # React dashboard
│ └── src/
│ ├── App.js
│ └── components/
├── figures/ # Generated visualizations
├── docs/ # Documentation
│ ├── analysis_workflow.md
│ └── assumptions_limitations.md
├── requirements.txt
├── .gitignore
└── README.md
```
## 📦 Data Source

| Attribute | Details |
|-----------|---------|
| **Dataset** | Brent Oil Prices |
| **Provider** | U.S. Energy Information Administration (EIA) |
| **Period** | May 20, 1987 - November 14, 2022 |
| **Observations** | 9,011 daily records |
| **Format** | CSV (Date, Price) |
| **Currency** | USD per barrel |
| **Access** | Included in /data/BrentOilPrices.csv |

## 🚀 Quick Start

### Prerequisites
`ash
# Clone the repository
git clone https://github.com/arsema16/brent_oil_analysis.git
cd brent_oil_analysis

# Create virtual environment (optional but recommended)
python -m venv brent_env
source brent_env/bin/activate  # On Windows: brent_env\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
