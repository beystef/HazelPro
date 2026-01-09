# HazelPro: Analyzing Hazelnut Price Fluctuations  

**DSA 210 – Introduction to Data Science (Fall 2025)**  
**Student:** Yusuf Efdal Yılmaz  

---

## Motivation

I am originally from **Ordu**, one of Türkiye’s most important hazelnut-producing regions. Growing up, I witnessed how volatile hazelnut prices directly affect farmers’ income, local welfare, and economic stability. These price changes are often attributed to many factors—weather conditions, currency fluctuations, or seasonal market behavior—mostly understood through experience rather than data.

This project aims to **systematically analyze** these factors using data science methods. By combining agricultural, economic, and public-interest data, I seek to better understand what drives hazelnut price fluctuations and evaluate whether prices can be meaningfully modeled or predicted.

---

## Data Sources

This project integrates four heterogeneous datasets covering **1999–2025**, enriched and aligned temporally:

### 1. Hazelnut Prices (Ordu)
- **Source:** Ordu Ticaret Borsası (Ordu Commodity Exchange)  
- **Frequency:** Daily  
- **Collection Method:** Web scraping from official Excel files  
- **Preprocessing:**  
  - Converted pre-2005 prices to new Turkish Lira  
  - Adjusted nominal prices using USD/TRY exchange rates  

### 2. Weather Data (Ordu Region)
- **Source:** Open-Meteo Historical Weather API  
- **Frequency:** Daily  
- **Features:**  
  - Temperature (max/min)  
  - Precipitation & rain  
  - Wind speed  
  - FAO evapotranspiration  
- **Collection Method:** Python API requests with 7-day chunking  

### 3. USD/TRY Exchange Rates
- **Source:** Central Bank of the Republic of Türkiye (TCMB EVDS API)  
- **Frequency:** Daily  
- **Usage:** Normalization of hazelnut prices to reduce currency-driven volatility  

### 4. Google Trends
- **Keyword:** *“fındık fiyatı”*  
- **Region:** Türkiye  
- **Collection Tool:** `pytrends`  
- **Methodology:**  
  - 90-day overlapping windows  
  - Median scaling to stitch windows consistently  

**Data Organization:**  
- Raw data: `data/raw/`  
- Processed datasets: `data/processed/`  

---

## Data Analysis Pipeline

### 1. Data Preparation
- Interpolated missing values (7-day limit for prices, time-based for currency)
- Smoothed prices using **14-day rolling averages**
- Created **USD-adjusted real prices**
- Generated **lagged weather features** (30, 60, 90, 120, 180 days)

---

### 2. Exploratory Data Analysis (EDA)

EDA focused on understanding temporal structure and data quality:
- Missing data heatmaps  
- Long-term and yearly time series plots  
- Seasonal distributions and variance comparisons  

All generated figures are stored in the `figures/` directory.

---

### 3. Feature Engineering

Constructed explanatory variables including:
- Seasonal indicators (spring, development, harvest, off-season)
- Extreme weather flags (heatwaves, cold spells, heavy rain)
- Lagged meteorological variables
- Binary indicators for missing or unavailable observations

---

## Hypothesis Testing

The following hypotheses were evaluated using **ANOVA**, **Kruskal–Wallis**, and **Spearman correlation** tests:

| Hypothesis | Description | Result |
|-----------|-------------|--------|
| **H1** | Prices exhibit seasonal patterns | **Confirmed** (F = 14.17, p < 0.001) |
| **H2** | Lagged weather affects prices | **Partially confirmed** (weak but significant correlations) |
| **H3** | USD normalization reduces volatility | **Confirmed** |
| **H4** | Google Trends peaks during harvest | **Confirmed** (H = 635.03, p < 0.001) |
| **H5** | High prices drive search interest | **Weak positive relationship** (ρ = 0.077, p < 0.001) |

---

## Machine Learning Models

Two regression models were implemented to predict **USD-adjusted hazelnut prices**:

### Model Setup
- **Training period:** Pre-2019  
- **Testing period:** 2019 and later (time-aware split)

### Results

| Model | RMSE | MAE | R² |
|------|------|-----|----|
| Random Forest | 1.34 | 0.94 | -0.80 |
| Ridge Regression | 9.21 | 7.35 | -84.32 |

Although Random Forest significantly outperformed Ridge Regression, **both models yielded negative R²**, indicating limited predictive power.

---

## Key Findings

1. **Strong seasonality exists**  
   Hazelnut prices vary systematically across agricultural seasons, especially during harvest.

2. **Weather effects are delayed and subtle**  
   Lagged temperature and precipitation variables show statistically significant but weak associations with prices.

3. **Currency normalization is essential**  
   Adjusting prices using USD/TRY reveals more stable underlying trends, highlighting the role of macroeconomic factors.

4. **Public interest is seasonal, not extreme-driven**  
   Google search interest peaks during harvest periods and reflects public awareness rather than extreme price movements.

5. **Price forecasting remains challenging**  
   Machine learning models struggle to predict prices accurately, suggesting missing structural market factors.

---

## Limitations and Future Work

### Limitations
- Absence of global supply-demand indicators
- Weather data from a single geographic location
- Google Trends data only available after 2011
- Interpolated price gaps during non-trading days

### Future Improvements
- Incorporate global hazelnut production data (Italy, USA)
- Add macroeconomic indicators (inflation, interest rates)
- Apply time-series models (ARIMA, Prophet)
- Expand weather coverage across the Black Sea region
- Include news sentiment or policy indicators
- Experiment with deep learning architectures (LSTM, Transformers)

---

## Setup and Reproducibility

### Requirements
- Python 3.11+
- Dependencies listed in `requirements.txt`

### Installation

```bash
git clone https://github.com/yourusername/HazelPro.git
cd HazelPro
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Here is a **clean, properly formatted Markdown version** you can paste directly into your `README.md` 👌

---

## Running the Project

### Step 1: Data Collection

```bash
python scripts/data_fetching/fetch_exchange_rates.py
python scripts/data_fetching/fetch_weather_data.py
python scripts/data_fetching/fetch_trends_data.py
```

### Step 2: Data Processing

```bash
python scripts/process/prepare_exchange_rates.py
python scripts/process/clean_prepare_hazelnut_price.py
python scripts/process/merge_weather_data.py
python scripts/process/merge_standardize_trends.py
```

### Step 3: Run Analysis Notebooks (in order)

1. `EDA_*.ipynb`
2. `feature_engineering.ipynb`
3. `hypothesis_testing.ipynb`
4. `random_forest.ipynb`
5. `ridge_regression.ipynb`

---

## Project Structure

```
HazelPro/
├── data/
│   ├── raw/              # Original collected datasets
│   └── processed/        # Cleaned and merged datasets
├── figures/              # Generated plots and visualizations
├── notebooks/            # Jupyter notebooks for analysis
├── scripts/
│   ├── data_fetching/    # Data collection scripts
│   └── process/          # Data cleaning and merging scripts
├── requirements.txt
└── README.md
```

---

## AI Assistance Disclosure

AI tools (ChatGPT, Claude) were used for:

* Debugging and refactoring Python code
* Improving visualization clarity
* Reviewing statistical interpretations
* Enhancing documentation and README structure

All data collection, modeling decisions, hypothesis formulation, and interpretation were performed independently.

---

## Acknowledgments

* **Data Providers:** Ordu Ticaret Borsası, TCMB, Open-Meteo, Google Trends
* **Development Tips:** ChatGPT, Gemini, Claude
* **Course:** DSA 210 – Introduction to Data Science
* **Institution:** Sabancı University
* **Term:** Fall 2025–2026

---
