# HazelPro
# Understanding The Effects of Weather, Currency, and Public Interest Data in Hazelnut Prices.

## Overview

This project will focus on Ordu city which is a key hazelnut producing region in Turkey. The project will make use of local market prices, weather data, currency exhange rates and search engine metrics to evaluate the possible active parameters in price fluctuation. In the project, first data will be collected, then data will be prepared for analysis. Afterwards, exploratory data analysis and visualizations will be prepared. Then, predictive model will be trained and hypothesis will be tested.

---

## Goal

The goal of my project is to understand the weather effect on hazelnut yields and develop a ML model to make predictions about the fluctuations and the prices in the hazelnut market.

---

## Motivation

Basically, the fact that Ordu is my hometown encourages me to do research about Ordu. Ordu is famous with the hazelnut, and it is among the most hazelnut producing cities. Hazelnut prices have an importance in term of yielding a welfare for the locals and supporting national economy. The hazelnut prices fluctuate over time in the market, thus, the project will facilitate making decisions on sales of hazelnuts. With this project, I want to underline how variables such as weather, public attention, and currency affect the prices.

---

## Data Sources and Collection Plan

| Data                          | Description                | Source                 | Collection Method                 |
| -------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------- |
| **Hazelnut Prices (Ordu)**       | Daily and monthly hazelnut prices                    | [Ordu Ticaret Borsası](https://www.ordutb.org.tr)    | Webscraping |
| **Currency Exchange Rates**      | Daily USD/TRY rates                                             | TCMB                 | API requests and webscraping                                |
| **Weather Data**                 | Temperature, precipitation, humidity                                        | Meteoroloji Genel Müdürlüğü and Open Weather Map  | API requests and webscraping                         |
| **Google Trends**                | Search engine keyword-interest such as “fındık fiyatı”, “Ordu fındık” | [Google Trends](https://trends.google.com)| Python (pytrends)                                    |

---

## Analysis Plan

First, I will collect the data as mentioned in the table above. Then, I will handle the missing values and standardize the data. Afterwards, I will do exploratory data analysis to understand the seasonal and temporal patterns. Then I will make analysis to understand whether we can use parameters to predict the hazelnut prices and if variables correlates. Furthermore, I will apply machine learning models to predict the hazelnut pricess. Finaly, I will visualize findings as graphics and tables and support them with statistical metrics.

---

## Expected Findings

With this project, it is anticipated that:

- There is a relation between the weather patterns and the hazelnut prices.
- Public interest in hazelnuts on search engines get affected through significant price changes.
- It is possible to foresee the hazelnut prices using weather patterns.
