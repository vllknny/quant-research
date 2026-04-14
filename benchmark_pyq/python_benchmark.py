"""
Python Database Benchmarking for Financial Data
Tests various Python libraries: pandas, SQL, Polars against common financial queries
"""

import pandas as pd
import sqlite3
import time
import json
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np

try:
    import polars as pl
except ImportError:
    pl = None


@dataclass
class BenchmarkResult:
    """Store benchmark results"""
    operation: str
    library: str
    duration_ms: float
    memory_mb: float
    rows_returned: int
    

class PythonBenchmark:
    """Benchmark various Python approaches to financial data queries"""
    
    def __init__(self, db_path: str = "financial_data.db"):
        self.db_path = db_path
        self.results: List[BenchmarkResult] = []
        self.conn = sqlite3.connect(db_path)
        
    def load_data_pandas(self) -> Dict[str, pd.DataFrame]:
        """Load data into pandas DataFrames"""
        prices = pd.read_sql("SELECT * FROM prices", self.conn)
        trades = pd.read_sql("SELECT * FROM trades", self.conn)
        fundamentals = pd.read_sql("SELECT * FROM fundamentals", self.conn)
        
        # Convert timestamp columns
        prices['timestamp'] = pd.to_datetime(prices['timestamp'])
        trades['timestamp'] = pd.to_datetime(trades['timestamp'])
        fundamentals['date'] = pd.to_datetime(fundamentals['date'])
        
        return {'prices': prices, 'trades': trades, 'fundamentals': fundamentals}
    
    def load_data_polars(self) -> Dict[str, pl.DataFrame]:
        """Load data into Polars DataFrames"""
        if not pl:
            return None
            
        prices = pl.read_database_uri(
            f"SELECT * FROM prices",
            uri=f"sqlite://{self.db_path}"
        )
        trades = pl.read_database_uri(
            f"SELECT * FROM trades",
            uri=f"sqlite://{self.db_path}"
        )
        fundamentals = pl.read_database_uri(
            f"SELECT * FROM fundamentals",
            uri=f"sqlite://{self.db_path}"
        )
        
        return {'prices': prices, 'trades': trades, 'fundamentals': fundamentals}
    
    def benchmark_operation(self, 
                           name: str, 
                           library: str,
                           operation: Callable) -> BenchmarkResult:
        """Run a single benchmark operation"""
        
        # Warm up
        try:
            operation()
        except:
            pass
        
        # Actual benchmark - multiple runs
        times = []
        result_size = 0
        
        for _ in range(5):
            start = time.perf_counter()
            result = operation()
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
            
            if hasattr(result, '__len__'):
                result_size = len(result)
            elif hasattr(result, 'height'):  # Polars
                result_size = result.height
        
        avg_time = np.mean(times)
        
        benchmark = BenchmarkResult(
            operation=name,
            library=library,
            duration_ms=avg_time,
            memory_mb=0,
            rows_returned=result_size
        )
        
        self.results.append(benchmark)
        return benchmark
    
    def run_pandas_benchmarks(self):
        """Run pandas benchmarks"""
        print("\n=== Pandas Benchmarks ===")
        data = self.load_data_pandas()
        prices = data['prices']
        trades = data['trades']
        fundamentals = data['fundamentals']
        
        # Benchmark 1: Filter by symbol
        def filter_symbol():
            return prices[prices['symbol'] == 'AAPL']
        
        result = self.benchmark_operation("Filter by symbol", "Pandas", filter_symbol)
        print(f"Filter by symbol: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 2: Group by and aggregation
        def group_agg():
            return prices.groupby('symbol')['close'].agg(['mean', 'std', 'min', 'max'])
        
        result = self.benchmark_operation("Group by symbol", "Pandas", group_agg)
        print(f"Group by symbol: {result.duration_ms:.2f}ms")
        
        # Benchmark 3: Time range filter
        def time_filter():
            start = pd.Timestamp("2024-01-01")
            end = pd.Timestamp("2024-06-30")
            return prices[(prices['timestamp'] >= start) & (prices['timestamp'] <= end)]
        
        result = self.benchmark_operation("Time range filter", "Pandas", time_filter)
        print(f"Time range filter: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 4: Moving average calculation
        def moving_avg():
            apple = prices[prices['symbol'] == 'AAPL'].sort_values('timestamp')
            return apple['close'].rolling(window=20).mean()
        
        result = self.benchmark_operation("Moving average", "Pandas", moving_avg)
        print(f"Moving average: {result.duration_ms:.2f}ms")
        
        # Benchmark 5: Multi-symbol join
        def join_op():
            apple_prices = prices[prices['symbol'] == 'AAPL'][['timestamp', 'close']]
            msft_prices = prices[prices['symbol'] == 'MSFT'][['timestamp', 'close']]
            return pd.merge(apple_prices, msft_prices, on='timestamp', how='inner')
        
        result = self.benchmark_operation("Join operation", "Pandas", join_op)
        print(f"Join operation: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 6: Trade analysis
        def trade_analysis():
            buy_trades = trades[trades['side'] == 'BUY']
            return buy_trades.groupby(['symbol', 'exchange']).agg({
                'size': ['sum', 'mean'],
                'price': 'mean'
            })
        
        result = self.benchmark_operation("Trade analysis", "Pandas", trade_analysis)
        print(f"Trade analysis: {result.duration_ms:.2f}ms")
    
    def run_sql_benchmarks(self):
        """Run SQL benchmarks"""
        print("\n=== SQL Benchmarks ===")
        
        # Benchmark 1: Filter by symbol
        def filter_symbol():
            return pd.read_sql(
                "SELECT * FROM prices WHERE symbol = 'AAPL'",
                self.conn
            )
        
        result = self.benchmark_operation("Filter by symbol", "SQL", filter_symbol)
        print(f"Filter by symbol: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 2: Group by
        def group_agg():
            return pd.read_sql("""
                SELECT symbol, 
                       AVG(close) as avg_price,
                       MIN(close) as min_price,
                       MAX(close) as max_price
                FROM prices
                GROUP BY symbol
            """, self.conn)
        
        result = self.benchmark_operation("Group by symbol", "SQL", group_agg)
        print(f"Group by symbol: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 3: Time range
        def time_filter():
            return pd.read_sql("""
                SELECT * FROM prices 
                WHERE timestamp BETWEEN '2024-01-01' AND '2024-06-30'
            """, self.conn)
        
        result = self.benchmark_operation("Time range filter", "SQL", time_filter)
        print(f"Time range filter: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 4: Complex analysis
        def complex_query():
            return pd.read_sql("""
                SELECT p.symbol,
                       COUNT(t.trade_id) as trade_count,
                       AVG(t.price) as avg_trade_price,
                       SUM(t.size) as total_volume
                FROM prices p
                LEFT JOIN trades t ON p.symbol = t.symbol 
                    AND DATE(p.timestamp) = DATE(t.timestamp)
                GROUP BY p.symbol
            """, self.conn)
        
        result = self.benchmark_operation("Complex join", "SQL", complex_query)
        print(f"Complex join: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
    
    def run_polars_benchmarks(self):
        """Run Polars benchmarks"""
        if not pl:
            print("\nPolars not installed, skipping...")
            return
        
        print("\n=== Polars Benchmarks ===")
        data = self.load_data_polars()
        if data is None:
            print("Could not load data into Polars")
            return
        
        prices = data['prices']
        trades = data['trades']
        
        # Benchmark 1: Filter by symbol
        def filter_symbol():
            return prices.filter(pl.col('symbol') == 'AAPL')
        
        result = self.benchmark_operation("Filter by symbol", "Polars", filter_symbol)
        print(f"Filter by symbol: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
        
        # Benchmark 2: Group by aggregation
        def group_agg():
            return prices.group_by('symbol').agg([
                pl.col('close').mean(),
                pl.col('close').std(),
                pl.col('close').min(),
                pl.col('close').max()
            ])
        
        result = self.benchmark_operation("Group by symbol", "Polars", group_agg)
        print(f"Group by symbol: {result.duration_ms:.2f}ms ({result.rows_returned} rows)")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate benchmark comparison report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_operations': len(self.results),
            'libraries': list(set(r.library for r in self.results)),
            'operations': list(set(r.operation for r in self.results)),
            'results': []
        }
        
        for result in self.results:
            report['results'].append({
                'operation': result.operation,
                'library': result.library,
                'duration_ms': result.duration_ms,
                'rows_returned': result.rows_returned
            })
        
        # Calculate speedup ratios
        operations = set(r.operation for r in self.results)
        for op in operations:
            op_results = [r for r in self.results if r.operation == op]
            if len(op_results) > 1:
                min_time = min(r.duration_ms for r in op_results)
                report.setdefault('speedups', {})[op] = {
                    r.library: f"{r.duration_ms/min_time:.2f}x" for r in op_results
                }
        
        return report
    
    def save_report(self, filename: str = "python_benchmark_results.json"):
        """Save results to JSON"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nResults saved to {filename}")
        return report
    
    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    benchmark = PythonBenchmark("financial_data.db")
    
    try:
        benchmark.run_pandas_benchmarks()
        benchmark.run_sql_benchmarks()
        benchmark.run_polars_benchmarks()
        
        report = benchmark.save_report()
        
        print("\n=== Summary ===")
        print(f"Total benchmarks run: {report['total_operations']}")
        print(f"Libraries tested: {', '.join(report['libraries'])}")
        
    finally:
        benchmark.close()
