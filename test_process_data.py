import unittest
import pandas as pd
import os
from process_data import load_real_time_data, load_gold_data

class TestProcessData(unittest.TestCase):

    def setUp(self):
        os.makedirs("tests", exist_ok=True)  # 🧠 Ensure test dir exists!

        self.realtime_path = "tests/temp_realtime.csv"
        df_rt = pd.DataFrame({
            "timestamp": pd.date_range("2023-01-01", periods=5, freq='h'),
            "value": [10, 20, 30, 40, 50]
        })
        df_rt.to_csv(self.realtime_path, index=False)

        self.gold_path = "tests/temp_gold.csv"
        df_gold = pd.DataFrame({
            "Date": pd.date_range("2023-01-01", periods=5, freq='D'),
            "Close": [1500, 1520, 1510, 1530, 1540]
        })
        df_gold.to_csv(self.gold_path, sep=';', index=False)

    def tearDown(self):
        if os.path.exists(self.realtime_path):
            os.remove(self.realtime_path)
        if os.path.exists(self.gold_path):
            os.remove(self.gold_path)

    def test_load_real_time_data_no_smooth(self):
        df = load_real_time_data(file_path=self.realtime_path, smooth=False)
        self.assertEqual(len(df), 5)
        self.assertIn("value", df.columns)
        self.assertNotIn("smoothed", df.columns)

    def test_load_real_time_data_with_smooth(self):
        df = load_real_time_data(file_path=self.realtime_path, smooth=True, window=2)
        self.assertIn("smoothed", df.columns)
        self.assertAlmostEqual(df["smoothed"].iloc[1], 15.0)

    def test_load_gold_data_no_smooth(self):
        df = load_gold_data(file_path=self.gold_path, smooth=False)
        self.assertIn("Price", df.columns)
        self.assertNotIn("smoothed", df.columns)
        self.assertEqual(len(df), 5)

    def test_load_gold_data_with_smooth(self):
        df = load_gold_data(file_path=self.gold_path, smooth=True, window=2)
        self.assertIn("smoothed", df.columns)
        self.assertAlmostEqual(df["smoothed"].iloc[1], 1510.0)

if __name__ == "__main__":
    unittest.main()
