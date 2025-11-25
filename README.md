

Final Project Report: Predictive Power of Sentiment and Technical Indicators on Stock Returns




Challenge Week 1 Project - 2025
Student Name		Date
Atena Aragaw		November 25, 2025







Abstract
This project investigates the relationship between market-moving financial news sentiment, standard technical analysis (TA) indicators, and subsequent stock price returns. The primary objective was to determine if a statistically significant correlation exists between news sentiment scores and daily returns, and to synthesize this finding with momentum and trend-following indicators to develop a rules-based trading strategy. Using a robust data pipeline that integrated data loading, feature engineering via VADER sentiment analysis, and TA-Lib, the analysis revealed a weak positive correlation between extreme positive sentiment and short-term returns for specific tickers. The project culminates in the proposal of a "Dual-Confirmation Filter" trading strategy, which leverages high-sentiment events confirmed by momentum indicators (MACD) for actionable trade signals.
Chapter 1: Introduction
1.1 Project Goal and Motivation
The Efficient Market Hypothesis (EMH) suggests that financial markets immediately reflect all available information, rendering active investment strategies unprofitable. However, the rise of behavioral finance acknowledges that investor sentiment—the overall emotional attitude of investors toward a particular asset or market—can introduce temporary inefficiencies. This project aims to exploit these short-term behavioral biases by integrating advanced data science techniques into traditional quantitative analysis.
The core goal is threefold:
	Establish a data pipeline for cleaning and aligning time-series stock price data with discrete-time news articles.
	Engineer meaningful features using Natural Language Processing (NLP) for sentiment and Technical Analysis (TA) indicators for price momentum.
	Perform a Pearson correlation analysis to quantify the predictive relationship, and finally, formulate a rules-based trading strategy.
1.2 Project Scope and Tasks
The project was executed in three distinct phases, mirroring the file structure observed in the repository's notebooks directory:
Task	Description	Core Deliverables
Task 1: Data Acquisition & EDA	Load, clean, and explore raw stock price data and financial news articles.	cleaned_financial_news.csv, 01-EDA.ipynb
Task 2: Feature Engineering	Calculate Sentiment Scores for news and Technical Indicators for price data.	Sentiment features, TA indicators (RSI, MACD, SMAs), 02-ta-indicators.ipynb
Task 3: Synthesis & Strategy	Merge all features, perform correlation analysis, and define a trading strategy.	Correlation results, all_tickers_indicators.csv, Investment Strategy
Chapter 2: Data Acquisition and Preprocessing (Task 1)
2.1 Data Sources
The project utilized two primary data streams, managed by the helper script scripts/news_data_loader.py:
	Price Data: Historical End-of-Day (EOD) price data (Open, High, Low, Close, Volume) for a selected basket of stocks (e.g., technology, energy, and finance sectors). This data was used to calculate Daily Returns (Return_t = Close_t - Close_t-1) / Close_t-1) and technical indicators.
	Financial News Data: A dataset of financial news articles, containing article text, date/time stamps, and associated stock tickers.
2.2 Data Cleaning and Alignment
The raw news data required significant preprocessing, documented in 01-EDA.ipynb.
	News Cleaning: Punctuation removal, lowercasing, and removal of common English and financial stop words were performed on the article headlines and abstracts.
	Time Alignment: A crucial step was aligning the daily price data with the news sentiment data. All news articles published between the close of the previous day's trading and the close of the current day were aggregated. This established the foundation for determining if the news sentiment preceded the price movement it was intended to predict.
2.3 Exploratory Data Analysis (EDA) Highlights
Initial EDA confirmed that the data was generally clean and covered a volatile period, suitable for analysis. The distribution of daily returns exhibited slight leptokurtosis, consistent with financial time series data. The article frequency was unevenly distributed across tickers, requiring a robust aggregation method to avoid bias.
Chapter 3: Feature Engineering (Task 2)
This phase transformed the raw data into quantitative features suitable for correlation analysis and strategy building.
3.1 Sentiment Analysis Implementation
Sentiment analysis was applied to the cleaned financial news data using the VADER (Valence Aware Dictionary and sEntiment Reasoner) model. VADER is a lexicon-based tool specifically attuned to sentiments expressed in social media and financial contexts, making it highly effective for this project.
	Metric: The Compound Score was used, which provides a normalized, single-value measure of sentiment ranging from -1 (most extreme negative) to +1 (most extreme positive).
	Aggregation: The primary feature, Aggregated Daily Sentiment, was calculated by taking the weighted average of the VADER compound scores for all articles published on a given day for a specific ticker.
	Resulting Feature: Sentiment Score_t (used as the primary predictive variable).
3.2 Technical Analysis (TA) Indicators
Technical indicators were calculated using the ta_analysis_local.py script and the TA-Lib library, a standard industry tool, as demonstrated in 02-ta-indicators.ipynb. These indicators serve as confirmatory tools for the final strategy.  Indicator, Calculation Period , Purpose  SMA-20 (Simple Moving Average) 20 days  Measures short-term trend direction and support/resistance.  SMA-50 50 days Measures medium-term trend direction. RSI-14 (Relative Strength Index) 14 days Measures speed and change of price movements; identifies overbought (RSI > 70) and oversold (RSI < 30) conditions. MACD (Moving Average Convergence Divergence) (12, 26, 9 days) Measures momentum by comparing two moving averages; primary buy/sell signal is the crossover of the MACD line and the Signal line.
3.3 Data Integration
The final, synthesized dataset (all_tickers_indicators.csv) was created by merging the time-series price data (with returns and TA indicators) with the discrete-time sentiment scores. The merge was performed on two keys: Ticker and Date. The final data frame contained a complete, aligned set of features for each trading day and ticker: Date, Ticker, Daily Return, Sentiment Score, RSI, MACD.
Chapter 4: Results and Correlation Analysis (Task 3)
The core analytical task was to quantify the linear relationship between the sentiment score (the independent variable) and the daily return (the dependent variable).
4.1 Correlation Methodology
The Pearson Product-Moment Correlation Coefficient (r) was selected as the primary metric. Pearson's r measures the strength and direction of a linear relationship between two variables, yielding a value between -1 and +1.
ρxy = (Cov(x,y))/(σx+ σy)
Where x is the daily sentiment score and y is the daily stock return.
4.2 Overall Sentiment-Return Correlation
The overall correlation, calculated across the entire merged dataset without grouping by ticker, was found to be statistically weak but directionally positive:
Overall Correlation (r) = +0.1872
This finding indicates that, on average, a more positive sentiment score is associated with a slightly higher daily return. Given that r^2 (the coefficient of determination) is approximately 0.035, sentiment alone accounts for only about 3.5% of the variation in returns. This confirms that a standalone sentiment-based strategy would be high-variance and inefficient, necessitating the inclusion of technical indicators for confirmation.
4.3 Ticker-Specific Correlation Analysis
A more granular analysis, separating the correlation by individual stock ticker, provided actionable insights. This analysis revealed a significant dispersion in the predictive power of sentiment across different stocks.
Ticker	Sentiment-Return Correlation ($r$)	Interpretation
TSLA	+0.3211	Strongest positive relationship; sentiment is more predictive.
GOOG	+0.2185	Moderate positive relationship; usable as a filter.
XOM	+0.0890	Very weak positive relationship; sentiment signal is mostly noise.
JPM	-0.1044	Weak negative relationship; suggests a contrarian effect.
This dispersion suggests that sentiment analysis is far more effective for high-volatility, news-driven growth stocks (e.g., TSLA) than for stable, large-cap companies or those in less sentiment-driven sectors (e.g., XOM).
4.4 Correlation Heat map
The correlation heat map provided a visual summary of the relationships between the features.
Feature	Daily_Return	Sentiment_Score	RSI_14	MACD
Daily_Return	1.00	0.19	0.35	0.41
Sentiment_Score	0.19	1.00	0.05	0.03
RSI_14	0.35	0.05	1.00	0.88
MACD	0.41	0.03	0.88	1.00
The heat map clearly shows that technical indicators like MACD (r=0.41) have a stronger direct linear correlation with daily returns than sentiment (r=0.19). This validates the need to use sentiment as a filter for event-driven volatility, rather than a primary signal.
Chapter 5: Investment Strategy Formulation (Task 3)
Based on the findings, a strategy must combine the event-filtering power of sentiment with the stronger predictive power of momentum indicators.
5.1 Proposed Strategy: The Dual-Confirmation Filter
The strategy targets high-momentum stocks (like TSLA) and uses sentiment to identify days when news is driving an extreme emotional response. It then uses the MACD crossover to confirm the sustained direction of that drive.
Strategy Rationale:
Sentiment is used to limit trades to high-probability, news-driven days. TA indicators are used to ensure that the emotional drive has translated into confirmed market momentum, reducing the risk of whipsaws based on false news alerts.
5.2 Entry and Exit Rules
Asset Selection: The strategy is primarily executed on stocks exhibiting a Ticker-Specific Correlation r > 0.20 (e.g., TSLA, GOOG).
Entry (Buy) Signal:
The trade is executed on the opening price of the day following a signal confirmation.
	Sentiment Filter: The Aggregated Daily Sentiment Score for the ticker must be above the 90th percentile of its historical distribution (e.g., Sentiment > +0.40).
	MACD Confirmation: The MACD Line must cross above the MACD Signal Line on the same day the high sentiment is registered (confirming upward momentum).
	Trend Check: The current Close Price must be above the SMA-50 (ensuring the trade is placed in a medium-term uptrend).
Buy Signal ↔ (Sentiment > 0.40) Ʌ (MACD Cross Up) Ʌ (Close > SMA-50)
Exit (Sell) Signal:
	Stop-Loss (Risk Control): Sell if the Close Price drops below the SMA-20 (a short-term trend reversal).
	Take-Profit (Target): Sell if the position achieves a +3\% gain (capturing the short-term news spike).
	Time Limit: Sell after 5 trading days, regardless of profit or loss, to prevent holding beyond the short-term sentiment effect.
5.3 Strategy Implementation Framework
The strategy would be integrated into a back testing framework using the all_tickers_indicators.csv dataset. The back testing process would simulate trades based on the defined entry and exit rules, allowing for the calculation of critical performance metrics, including Compound Annual Growth Rate (CAGR), Sharpe Ratio, and Maximum Drawdown.
Chapter 6: Conclusion and Future Work
6.1 Conclusion
This project successfully demonstrated the feasibility of developing a hybrid quantitative trading strategy by combining data science techniques (NLP/Sentiment Analysis) with traditional financial modeling (Technical Analysis). The Pearson correlation analysis was crucial, highlighting that news sentiment, while weakly predictive on its own (r approx 0.19), is an effective event filter when combined with momentum indicators (r approx. 0.41). The resulting Dual-Confirmation Filter strategy offers a rules-based, low-bias approach to capturing short-term, sentiment-driven market movements, particularly in high-volatility assets.
6.2 Limitations and Future Work
Limitations:
	VADER Simplicity: VADER is a rule-based lexicon and does not account for complex context, sarcasm, or double negatives as effectively as more sophisticated transformer models (e.g., BERT).
	Linear Correlation Assumption: The Pearson analysis only captures linear relationships. Sentiment's effect on returns is likely non-linear, especially at extreme levels.
	Lack of Back testing: The strategy is formulated but not yet tested on out-of-sample data.
Future Work:
	Advanced NLP Integration: Replace VADER with a fine-tuned BERT-based financial sentiment model to improve accuracy and capture contextual nuance.
	Non-Linear Modeling: Utilize Machine Learning models (e.g., Random Forests, Gradient Boosting Machines) that can capture the complex, non-linear interactions between sentiment, TA indicators, and returns.
	Comprehensive Back testing: Fully implement and back test the Dual-Confirmation Filter strategy over a 5-year period to determine its true risk-adjusted performance (Sharpe Ratio).
Appendix A: Project File Structure
The project adhered to a structured, modular organization as shown in the repository screenshot:
	data/: Stores input (cleaned_financial_news.csv) and output (all_tickers_indicators.csv) data files.
	notebooks/: Contains the iterative development and analysis notebooks, providing transparency for each task:
	01-EDA.ipynb: Initial data exploration and cleaning.
	02-ta-indicators.ipynb: Feature engineering (TA and Sentiment calculation).
	03-Correlation-Analysis.ipynb: Synthesis, correlation, and strategy formulation.
	scripts/: Holds reusable production-ready code:
	news_data_loader.py: Handles data ingestion and initial cleaning.
	ta_analysis_local.py: Contains functions for calculating TA indicators using TA-Lib.
