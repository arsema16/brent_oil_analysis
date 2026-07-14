# Assumptions and Limitations

## Statistical Assumptions

### 1. Independence of Observations
We assume that observations are conditionally independent given the model parameters. This is a standard assumption for time series analysis, though oil prices may exhibit autocorrelation.

### 2. Normality of Errors
The likelihood assumes a Normal distribution for log-returns. While log-returns are approximately normal, the distribution exhibits heavy tails (leptokurtosis) during crisis periods.

### 3. Single Change Point
Our initial model focuses on detecting structural breaks sequentially. In reality, multiple overlapping events may occur simultaneously, making it difficult to isolate individual effects.

### 4. Known Prior Distributions
We use uniform priors for change point locations, which assumes no prior knowledge about where changes might occur.

## Analytical Limitations

### 1. Correlation vs. Causation
**Critical Distinction**: Change point detection identifies statistical breaks in time series data, but does not prove causality. When we associate a change point with an event, we are identifying a temporal correlation, not establishing a causal relationship.

**Example**: A price change detected on August 2, 1990 (the date of Iraq's invasion of Kuwait) is temporally correlated with that event. However, other factors (market sentiment, supply chain disruptions, geopolitical tensions) may have also contributed to the price movement.

**Implication**: Our analysis provides evidence of association, not proof of causation. Multiple events may coincide, and price changes can result from complex interactions.

### 2. Event Date Ambiguity
Many events unfold over days or weeks, making it difficult to pinpoint exact start dates. For example:
- OPEC negotiations may take weeks before a decision is announced
- Military conflicts may have gradual escalations
- Economic crises often build up over time

**Mitigation**: We use a 90-day window for event association to account for uncertainty in event timing.

### 3. Model Simplicity
Our model captures structural breaks but does not account for:
- Exchange rate fluctuations
- GDP growth rates
- Inflation data
- Interest rates
- Supply-demand dynamics

### 4. Data Limitations

#### Date Format Issues
The dataset contains two date formats:
- '%d-%b-%y' (e.g., 20-May-87)
- '%b %d, %Y' (e.g., Apr 22, 2020)

**Mitigation**: Flexible date parsing with fallback formats.

#### Missing Data
- Weekends and holidays are not recorded
- Some dates may be missing due to data collection gaps

**Mitigation**: Identified 1,897 missing dates out of 12,908 total days (85% coverage).

#### Price Data
- Prices are in USD per barrel only
- No adjustment for inflation
- No associated volume or trading data

### 5. External Factors Not Included
- Exchange rates (USD strength)
- Global economic conditions
- Alternative energy prices
- Storage and inventory levels
- Production capacity

## Data Source Information

| Attribute | Details |
|-----------|---------|
| **Dataset Name** | Brent Oil Prices |
| **Provider** | U.S. Energy Information Administration (EIA) |
| **Data Type** | Daily closing prices |
| **Period** | May 20, 1987 - November 14, 2022 |
| **Currency** | USD per barrel |
| **Format** | CSV (Date, Price) |

## Mitigation Strategies

| Limitation | Strategy |
|------------|----------|
| Correlation vs. Causation | Explicitly distinguish between association and causation in reporting |
| Event Ambiguity | Use 90-day window for association; document event uncertainty |
| Missing Data | Identify and document missing dates; use forward fill where appropriate |
| Date Formats | Implement flexible parsing with multiple format support |
| External Factors | Acknowledge in reports; suggest future work with additional data sources |

## Best Practices Followed

1. **Reproducibility**: All code and data are version-controlled
2. **Documentation**: Assumptions and limitations clearly stated
3. **Flexibility**: Multiple date formats supported
4. **Transparency**: All analysis steps documented
5. **Validation**: Stationarity testing performed on all time series

## Future Work Recommendations

1. **Add External Data Sources**
   - GDP growth rates
   - Exchange rates (USD/EUR, USD/JPY)
   - OPEC production data
   - Global oil demand indicators

2. **Advanced Models**
   - VAR (Vector Autoregression) for multivariate analysis
   - Markov-Switching models for regime detection
   - Bayesian structural time series models

3. **Causal Inference**
   - Apply causal inference methods (e.g., difference-in-differences)
   - Use synthetic control methods
   - Implement event study methodology
