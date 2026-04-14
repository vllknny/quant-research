"""
Financial Data Generator for Benchmarking
Generates base financial market data for Python vs Q comparison
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
from typing import Tuple, List
import pickle


class FinancialDataGenerator:
    """Generate realistic financial data for benchmarking"""
    
    def __init__(self, 
                 symbols: List[str] = None,
                 start_date: str = "2020-01-01",
                 end_date: str = "2024-12-31",
                 data_points_per_day: int = 390):  # ~1 per minute for trading day
        
        self.symbols = symbols or ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'SPY']
        self.start_date = pd.Timestamp(start_date)
        self.end_date = pd.Timestamp(end_date)
        self.data_points_per_day = data_points_per_day
        
    def generate_price_data(self) -> pd.DataFrame:
        """Generate OHLCV data"""
        data = []
        
        # Create trading dates (business days only)
        dates = pd.bdate_range(self.start_date, self.end_date)
        
        for symbol in self.symbols:
            # Initial price
            price = np.random.uniform(50, 500)
            
            for date in dates:
                # Generate intraday data
                for minute in range(self.data_points_per_day):
                    # Random walk for price
                    price_change = np.random.normal(0, 0.5)
                    open_price = price
                    close_price = price + price_change
                    high_price = max(open_price, close_price) + abs(np.random.normal(0, 0.3))
                    low_price = min(open_price, close_price) - abs(np.random.normal(0, 0.3))
                    volume = int(np.random.uniform(1000, 10000000))
                    
                    timestamp = date + timedelta(minutes=minute)
                    
                    data.append({
                        'timestamp': timestamp,
                        'symbol': symbol,
                        'open': open_price,
                        'high': high_price,
                        'low': low_price,
                        'close': close_price,
                        'volume': volume
                    })
                    
                    price = close_price
        
        df = pd.DataFrame(data)
        df = df.sort_values(['symbol', 'timestamp']).reset_index(drop=True)
        return df
    
    def generate_trades(self) -> pd.DataFrame:
        """Generate individual trade data"""
        data = []
        
        dates = pd.bdate_range(self.start_date, self.end_date)
        
        for symbol in self.symbols:
            price = np.random.uniform(50, 500)
            
            for date in dates:
                num_trades = np.random.randint(100, 5000)
                
                for trade_num in range(num_trades):
                    price_change = np.random.normal(0, 0.2)
                    price = price + price_change
                    
                    timestamp = date + timedelta(
                        hours=np.random.uniform(9.5, 16),
                        minutes=np.random.uniform(0, 60)
                    )
                    
                    data.append({
                        'trade_id': len(data),
                        'timestamp': timestamp,
                        'symbol': symbol,
                        'price': price,
                        'size': int(np.random.uniform(100, 100000)),
                        'side': np.random.choice(['BUY', 'SELL']),
                        'exchange': np.random.choice(['NYSE', 'NASDAQ', 'BATS'])
                    })
        
        df = pd.DataFrame(data)
        df = df.sort_values(['symbol', 'timestamp']).reset_index(drop=True)
        return df
    
    def generate_fundamentals(self) -> pd.DataFrame:
        """Generate company fundamental data"""
        data = []
        
        dates = pd.date_range(self.start_date, self.end_date, freq='Q')
        
        for symbol in self.symbols:
            pe_ratio = np.random.uniform(10, 50)
            pb_ratio = np.random.uniform(1, 5)
            dividend = np.random.uniform(0, 5)
            
            for date in dates:
                pe_ratio += np.random.normal(0, 2)
                pb_ratio += np.random.normal(0, 0.3)
                dividend += np.random.normal(0, 0.2)
                
                data.append({
                    'date': date,
                    'symbol': symbol,
                    'pe_ratio': max(pe_ratio, 1),
                    'pb_ratio': max(pb_ratio, 0.5),
                    'dividend_yield': max(dividend, 0),
                    'eps': np.random.uniform(0.5, 10),
                    'roe': np.random.uniform(0, 40),
                    'debt_to_equity': np.random.uniform(0, 2)
                })
        
        df = pd.DataFrame(data)
        return df
    
    def save_to_sqlite(self, output_file: str = "financial_data.db"):
        """Save all data to SQLite database"""
        conn = sqlite3.connect(output_file)
        
        print("Generating price data...")
        price_df = self.generate_price_data()
        price_df.to_sql('prices', conn, if_exists='replace', index=False)
        
        print("Generating trade data...")
        trades_df = self.generate_trades()
        trades_df.to_sql('trades', conn, if_exists='replace', index=False)
        
        print("Generating fundamental data...")
        fund_df = self.generate_fundamentals()
        fund_df.to_sql('fundamentals', conn, if_exists='replace', index=False)
        
        conn.close()
        print(f"Database saved to {output_file}")
        
        return price_df, trades_df, fund_df
    
    def save_to_pickle(self, output_dir: str = "data"):
        """Save data as pickle files"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating price data...")
        price_df = self.generate_price_data()
        price_df.to_pickle(f"{output_dir}/prices.pkl")
        
        print("Generating trade data...")
        trades_df = self.generate_trades()
        trades_df.to_pickle(f"{output_dir}/trades.pkl")
        
        print("Generating fundamental data...")
        fund_df = self.generate_fundamentals()
        fund_df.to_pickle(f"{output_dir}/fundamentals.pkl")
        
        print(f"Data saved to {output_dir}/")
        
        return price_df, trades_df, fund_df


if __name__ == "__main__":
    # Generate sample data
    generator = FinancialDataGenerator(
        start_date="2023-01-01",
        end_date="2024-12-31",
        data_points_per_day=390
    )
    
    price_df, trades_df, fund_df = generator.save_to_sqlite("financial_data.db")
    
    print("\n=== Data Summary ===")
    print(f"Prices: {len(price_df)} records, {price_df['symbol'].nunique()} symbols")
    print(f"Trades: {len(trades_df)} records")
    print(f"Fundamentals: {len(fund_df)} records")
