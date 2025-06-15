# dashboard.py
import streamlit as st
import time
from process_data import load_real_time_data, load_gold_data
import matplotlib.pyplot as plt
import datetime


st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose Analysis", [
    "Real-Time Data", "Gold Price Data", "Real-Time Monitoring", "User Guide", "System Architecture"
])


smooth = st.sidebar.checkbox("Apply Smoothing")
window = st.sidebar.slider("Smoothing Window", 2, 50, 10)

# Performance tracking
start_time = time.time()

if page == "Real-Time Data":
    st.title("Real-Time Data Analysis")
    df = load_real_time_data("realtime_data.csv", smooth, window)
    
    if df.empty:
        st.warning("Waiting for real-time data...")
    else:
        latest = df.iloc[-1]
        st.metric("Latest Value", f"{latest['value']:.2f}")
        st.metric("Last Timestamp", f"{latest['timestamp']}")
        st.metric("Number of Points", len(df))

        st.line_chart(df.set_index("timestamp")[["value", "smoothed"]] if smooth else df.set_index("timestamp")["value"])

        st.write("Basic Stats:")
        st.write(df.describe())

elif page == "Gold Price Data":
    st.title("Gold Price Analysis (XAU/USD)")
    df = load_gold_data("kaggle_gold.csv", smooth, window)

    st.metric("First Date", df['Date'].min().strftime("%Y-%m-%d"))
    st.metric("Last Date", df['Date'].max().strftime("%Y-%m-%d"))
    st.metric("Data Points", len(df))

    st.line_chart(df.set_index("Date")[["Price", "smoothed"]] if smooth else df.set_index("Date")["Price"])

    st.write("Basic Stats:")
    st.write(df.describe())

    st.subheader("Daily Change Distribution")
    df['daily_return'] = df['Price'].pct_change()
    st.bar_chart(df['daily_return'].dropna())

    st.subheader("Rolling Volatility")
    df['volatility'] = df['daily_return'].rolling(window=window).std()
    st.line_chart(df.set_index("Date")["volatility"])

elif page == "User Guide":
    st.title("User Guide")
    st.markdown("""
    ### What You Can Do Here:
    
    **1. Real-Time Tab**  
    - View simulated sensor/streaming data.
    - Toggle smoothing to eliminate noise.
    - See number of points, latency, and last value.
    
    **2. Gold Price Tab**  
    - Analyze gold prices from 2004–present.
    - Toggle smoothing to identify long-term trends.
    - See price changes and volatility (standard deviation of returns).

    **3. Performance Metrics**
    - All tabs show latency, data volume, and basic summary stats.

    **4. Smoothing & Rolling Analysis**
    - Enable smoothing in the sidebar.
    - Set custom window size (e.g., 7-day or 30-point).

    **Enjoy analyzing data!**
    """)

elif page == "Real-Time Monitoring":
    st.title("Real-Time Monitoring & Performance")

    processing_start = time.time()
    df_rt = load_real_time_data("realtime_data.csv", False)
    df_gold = load_gold_data("kaggle_gold.csv", False)
    processing_end = time.time()
    processing_duration = processing_end - processing_start

    st.metric("⏱ Processing Time", f"{processing_duration:.2f} s")

    if not df_rt.empty:
        now = datetime.datetime.utcnow()
        last_time = df_rt['timestamp'].iloc[-1].to_pydatetime()
        latency = (now - last_time).total_seconds()

        st.metric("Streaming Latency", f"{latency:.2f} s")
        st.metric("Real-Time Data Volume", len(df_rt))
        st.metric("Gold Data Volume", len(df_gold))

        if latency > 10:
            st.warning(f"Real-time data is stale! Last update was {latency:.2f} seconds ago.")
    else:
        st.warning("No real-time data available.")

    st.write("Timestamp of last real-time data:")
    if not df_rt.empty:
        st.write(df_rt['timestamp'].iloc[-1])

elif page == "System Architecture":
    st.title("System Architecture & Data Flow")
    st.markdown("""
    ### System Components

    - **data_generator.py**  
      Simulates and writes real-time sensor-style data to `realtime_data.csv` every 2 seconds.

    - **process_data.py**  
      Loads, cleans, and smooths both real-time and historical gold datasets.

    - **dashboard.py**  
      Streamlit frontend displaying data in 4 views:
      - Real-Time
      - Gold Price
      - Monitoring
      - Documentation

    ### Data Flow Overview

    ```mermaid
    graph TD
        A[Real-time Generator] --> B[realtime_data.csv]
        B --> D[Streamlit Dashboard]
        C[Gold CSV (2004–present)] --> D
        D --> E[Rolling Avg, Charts, Metrics]
    ```

    ### Folder Structure

    - `data_generator.py`
    - `realtime_data.csv`
    - `kaggle_gold.csv`
    - `process_data.py`
    - `dashboard.py`
    - `README.md`
    """)

  
elapsed = time.time() - start_time
st.sidebar.success(f"Dashboard loaded in {elapsed:.2f}s")
