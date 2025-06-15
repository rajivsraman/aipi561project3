# Advanced Analytics Integration - Real-Time Dashboard

## Overview
This project simulates a real-time data pipeline and displays it using a live dashboard built with Streamlit.

## Architecture


## How to Run

1. Start the data simulator:
    ```
    python data_generator.py
    ```

2. In another terminal, start the dashboard:
    ```
    streamlit run dashboard.py
    ```

3. Dashboard auto-refreshes every 2 seconds to show new values.

## Features

- Real-time monitoring
- Visualization with line charts and metrics
- Modular code
- Easy to extend for real APIs or databases



# Advanced Analytics Dashboard

## Overview
This dashboard lets you explore:
- 🔁 Real-time simulated data (auto-updating)
- 🏆 Historical gold price data (XAU/USD from 2004–present)
- 📉 Performance metrics, rolling averages, and smoothing

## How to Run

1. Start the real-time simulator (optional):
    ```bash
    python data_generator.py
    ```

2. Launch the dashboard:
    ```bash
    streamlit run dashboard.py
    ```

## Features

- **Real-Time Tab**: View live data, smoothing toggle, metrics
- **Gold Price Tab**: Historical price, volatility, daily returns
- **User Guide**: Explanations for non-technical users
