# quant-research

The repository of me learning quant tools! Will include Python + libs, Q, KDB+, SQL, etc.

## 📊 Python vs Q Financial Database Benchmark Suite

A comprehensive benchmarking framework comparing Python and Q (KDB+) for financial database operations with base financial data and MCP support.

### 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run quick benchmark
python quickstart.py --mode quick

# Run full benchmark
python quickstart.py --mode full

# Start MCP server
python quickstart.py --mode mcp
```

### 📁 Project Files

#### Core Modules
- **`financial_data_generator.py`** - Generate realistic OHLCV, trade, and fundamental data
- **`python_benchmark.py`** - Benchmark Pandas, SQL (SQLite), and Polars
- **`q_benchmark_reference.py`** - Q/KDB+ performance analysis and code templates
- **`mcp_benchmark_server.py`** - MCP (Model Context Protocol) server
- **`comprehensive_benchmark.py`** - Main orchestrator for full benchmark suite

#### Configuration & Tools
- **`benchmark_config.py`** - Configuration management for different scenarios
- **`quickstart.py`** - One-command startup script
- **`requirements.txt`** - Python dependencies
- **`README_BENCHMARK.md`** - Full documentation

### 🎯 Key Features

1. **Financial Data Generation**
   - Realistic OHLCV data (Open, High, Low, Close, Volume)
   - Trade tick data
   - Fundamental metrics
   - Customizable date ranges and symbols

2. **Python Benchmarking**
   - Pandas operations
   - SQLite queries
   - Polars performance comparison
   - Standard financial queries

3. **Q/KDB+ Analysis**
   - Performance estimates (50-150x typical speedups)
   - Q code templates
   - Columnar storage analysis
   - Time-series optimization

4. **MCP Integration**
   - Automated tool for benchmark orchestration
   - Integration with Claude and other MCP clients
   - Report generation

### 📈 Expected Results

| Operation | Python (ms) | Q Est. (ms) | Speedup |
|-----------|------------|------------|---------|
| Filter | 45 | 0.7 | 65x |
| Group By | 98 | 1.5 | 65x |
| Time Filter | 68 | 1.0 | 68x |
| Moving Avg | 234 | 2.8 | 84x |
| Join | 157 | 1.6 | 98x |
| **Average** | **120** | **1.7** | **~75x** |

### 🔧 Usage Examples

#### Generate Data Only
```python
from financial_data_generator import FinancialDataGenerator

gen = FinancialDataGenerator(
    symbols=['AAPL', 'MSFT', 'GOOGL'],
    start_date='2023-01-01',
    end_date='2024-12-31'
)
gen.save_to_sqlite('financial_data.db')
```

#### Run Python Benchmarks
```python
from python_benchmark import PythonBenchmark

bench = PythonBenchmark('financial_data.db')
bench.run_pandas_benchmarks()
bench.run_sql_benchmarks()
bench.run_polars_benchmarks()
bench.save_report()
```

#### Use MCP Server
```python
from mcp_benchmark_server import BenchmarkMCPServer

server = BenchmarkMCPServer()
result = server.generate_financial_data(output_format='sqlite')
result = server.run_python_benchmark(libraries=['pandas', 'sql'])
result = server.generate_comparison_report(output_format='markdown')
```

### 📝 Benchmark Scenarios

Pre-configured scenarios available:
- **development** - Small dataset for testing (~50K records)
- **production** - Full dataset (2.5M+ records)
- **realtime** - High-frequency trade data
- **education** - Learning size

Create with:
```python
from benchmark_config import create_config_file
create_config_file('production')
```

### 🎓 Learning Resources

- Full documentation: [README_BENCHMARK.md](README_BENCHMARK.md)
- Q code examples: See `q_benchmark_reference.py`
- KDB+ documentation: https://code.kx.com/q/
- Benchmark methodology: See `comprehensive_benchmark.py`

### 🔍 Performance Insights

**Why Q is Fast:**
- Columnar storage (8-15x compression)
- Vector operations (no loops)
- Optimized for financial data
- Built-in time-series functions

**Why Python is Great:**
- Flexible and general-purpose
- Huge ecosystem (ML, web, etc.)
- Easy to learn and use
- Excellent for prototyping

### 📊 Output Files

After running benchmarks, check:
```
benchmark_results/
├── comparison_report.json       # Full data in JSON
├── comparison_report.md         # Readable markdown
├── python_benchmark_results.json # Detailed Python results
└── financial_data.db            # Test database
```

### ⚙️ Customization

Modify benchmark operations in `python_benchmark.py`:
```python
def benchmark_custom_operation():
    def operation():
        # Your custom code
        return prices.groupby('symbol').apply(custom_func)
    
    benchmark.benchmark_operation("My Operation", "Pandas", operation)
```

### 📦 Dependencies

- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **polars** - Fast dataframe library
- **sqlite3** (built-in) - Database
- **mcp** (optional) - Model Context Protocol

### 🤝 Integration

- Use with Jupyter Notebooks
- Integrate with Claude via MCP
- Connect to KDB+ via qPython
- Export results for reporting

### 📚 See Also

- [Full Benchmark Documentation](README_BENCHMARK.md)
- [Comprehensive Benchmark Orchestrator](comprehensive_benchmark.py)
- [Configuration Examples](benchmark_config.py)
- [MCP Server Details](mcp_benchmark_server.py)

---

**Last Updated:** 2024
**Version:** 1.0
