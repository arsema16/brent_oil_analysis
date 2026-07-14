# Brent Oil Price Analysis: Data Analysis Workflow

## 1. Executive Summary
This analysis identifies and quantifies the impact of major geopolitical and economic events on Brent crude oil prices using Bayesian change point detection methods.

## 2. Analysis Workflow

### Phase 1: Data Preparation
- **Data Loading**: Load Brent oil price dataset from CSV
- **Date Parsing**: Convert to datetime format (handles both '%d-%b-%y' and '%b %d, %Y')
- **Quality Check**: Identify missing values, gaps, and outliers
- **Data Types**: Ensure correct data types for analysis

### Phase 2: Exploratory Data Analysis (EDA)
- **Univariate Analysis**: Price distribution, returns distribution
- **Time Series Visualization**: Raw prices, log prices
- **Trend Analysis**: Long-term trends using moving averages (50-day, 200-day)
- **Stationarity Testing**: ADF test on prices and returns
- **Volatility Analysis**: Identify volatility clustering periods using rolling windows

### Phase 3: Event Data Compilation
- **Research**: Identify major global events affecting oil prices from historical records
- **Structuring**: Create CSV with event dates, names, categories
- **Categorization**: Group events by type (Geopolitical_Conflict, Economic_Shock, OPEC_Policy, etc.)
- **Impact Rating**: Classify events by expected impact (Very_High, High, Medium)

### Phase 4: Change Point Detection
- **Method Selection**: Rolling window statistics with t-test
- **Implementation**: Python script with configurable window sizes (30, 60, 90 days)
- **Threshold**: 2.0 standard deviations for significance
- **Detection**: Identify structural breaks in price series

### Phase 5: Event Association & Impact Quantification
- **Temporal Mapping**: Associate detected change points with events within 90 days
- **Impact Calculation**: Quantify price changes in $ and %
- **Categorization**: Group impacts by event category
- **Ranking**: Identify most significant events

### Phase 6: Insights Generation
- **Key Findings**: Document major detected changes
- **Visualization**: Create charts for stakeholder communication
- **Recommendations**: Develop actionable insights
- **Limitations**: Acknowledge constraints and caveats

### Phase 7: Dashboard Development
- **Backend**: Flask API serving analysis results
- **Frontend**: React dashboard with interactive visualizations
- **Features**: Date filtering, event highlighting, drill-down capability

## 3. Methodology Summary

### Change Point Detection Algorithm:

### Event Association:
- Match change points to events within 90-day window
- Calculate price change before/after (30-day windows)
- Quantify impact in $ and %

## 4. Tools and Technologies

| Component | Tool |
|-----------|------|
| Data Processing | Python (Pandas, NumPy) |
| Analysis | Jupyter Notebooks |
| Visualization | Matplotlib, Seaborn |
| Change Detection | Custom rolling window algorithm |
| Backend | Flask |
| Frontend | React, Material-UI, Recharts |
| Version Control | Git, GitHub |

## 5. Expected Outputs

1. **EDA Notebook**: Comprehensive exploratory analysis with visualizations
2. **Events Dataset**: CSV with 14+ key events and metadata
3. **Change Point Analysis**: Detected structural breaks with timestamps
4. **Event Associations**: Mapping of events to price changes
5. **Impact Quantification**: $ and % impacts per event
6. **Interactive Dashboard**: Flask + React application
7. **Summary Report**: Key findings and recommendations
