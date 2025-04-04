#Sports Arbitrage

# IPL Arbitrage Betting Simulator & Visualizer

This project simulates arbitrage betting opportunities in IPL cricket matches using Python. It calculates potential guaranteed profits across multiple bookmakers and provides animated visualizations to analyze profit patterns.

## Features

- **Arbitrage Detection**: Calculates implied probabilities from bookmaker odds and identifies arbitrage scenarios.
- **Optimal Staking Strategy**: Computes stake allocation and guaranteed profit based on best odds.
- **Data Simulation**: Generates fake IPL match odds with realistic bookmaker ranges.
- **Real-Time Visualizations**:
  - Scatter plot of match-wise arbitrage profits
  - Cumulative profit line chart
  - Histogram of profit distribution
- **Detailed Match Analysis**: Console output of all matches with arbitrage opportunities.

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn

## How It Works

1. Fake IPL match odds are generated for 100 matches.
2. Best odds are selected from 2 bookmakers.
3. If the sum of implied probabilities < 1, an arbitrage exists.
4. The tool calculates the optimal stake distribution for guaranteed profit.
5. Three animated graphs help visualize profits over time.

## Demo

![scatter](https://imgur.com/a/iaSDlWj)
![cumulative](https://imgur.com/a/0X83LTi)

## Future Improvements

- Integrate live IPL match odds via API
- Add more bookmakers for more realistic analysis
- Deploy as a web app using Streamlit or Flask

---

> **Created by a 12th-grade student passionate about finance, data science, and algorithmic thinking.**

