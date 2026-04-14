"""
Configuration for Financial Database Benchmarking
Customize settings for data generation and benchmarking
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class BenchmarkConfig:
    """Configuration management for benchmarks"""
    
    def __init__(self, config_file: str = "benchmark_config.json"):
        self.config_file = config_file
        self.config = self._load_default_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "data_generation": {
                "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"],
                "start_date": "2023-01-01",
                "end_date": "2024-12-31",
                "data_points_per_day": 390,
                "output_format": "sqlite",
                "db_path": "financial_data.db"
            },
            "python_benchmarks": {
                "libraries": ["pandas", "sql", "polars"],
                "runs_per_operation": 5,
                "operations": [
                    "Filter by symbol",
                    "Group by symbol",
                    "Time range filter",
                    "Moving average",
                    "Join operation",
                    "Trade analysis"
                ]
            },
            "q_analysis": {
                "speedup_estimates": {
                    "filter": {"min": 40, "max": 60},
                    "group_by": {"min": 60, "max": 100},
                    "join": {"min": 80, "max": 150},
                    "complex": {"min": 100, "max": 200}
                },
                "compression_ratio": {"min": 8, "max": 15}
            },
            "output": {
                "directory": "benchmark_results",
                "formats": ["json", "markdown", "html"],
                "include_detailed_stats": True,
                "include_memory_metrics": True
            },
            "performance_thresholds": {
                "python_slow_query_ms": 500,
                "python_acceptable_query_ms": 100,
                "q_typical_speedup_min": 50
            }
        }
    
    def load_from_file(self, filepath: str):
        """Load configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.config = json.load(f)
            return True
        except FileNotFoundError:
            print(f"Config file not found: {filepath}")
            return False
    
    def save_to_file(self, filepath: str = None):
        """Save configuration to JSON file"""
        filepath = filepath or self.config_file
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"Configuration saved to {filepath}")
    
    def get_data_config(self) -> Dict[str, Any]:
        """Get data generation configuration"""
        return self.config.get("data_generation", {})
    
    def get_python_config(self) -> Dict[str, Any]:
        """Get Python benchmark configuration"""
        return self.config.get("python_benchmarks", {})
    
    def get_q_config(self) -> Dict[str, Any]:
        """Get Q analysis configuration"""
        return self.config.get("q_analysis", {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.config.get("output", {})
    
    def update_symbols(self, symbols: List[str]):
        """Update symbols to benchmark"""
        self.config["data_generation"]["symbols"] = symbols
    
    def update_date_range(self, start_date: str, end_date: str):
        """Update date range for data generation"""
        self.config["data_generation"]["start_date"] = start_date
        self.config["data_generation"]["end_date"] = end_date
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        # Check required fields
        if not self.config.get("data_generation", {}).get("symbols"):
            errors.append("No symbols configured")
        
        if not self.config.get("output", {}).get("directory"):
            errors.append("No output directory configured")
        
        # Check date format
        try:
            import datetime
            start = self.config["data_generation"]["start_date"]
            end = self.config["data_generation"]["end_date"]
            datetime.datetime.strptime(start, "%Y-%m-%d")
            datetime.datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid date format (use YYYY-MM-DD)")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True


# Example configurations for different scenarios

CONFIG_DEVELOPMENT = {
    "data_generation": {
        "symbols": ["AAPL", "MSFT"],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "data_points_per_day": 100,
    },
    "python_benchmarks": {
        "runs_per_operation": 2,
    },
    "description": "Small dataset for development and testing"
}

CONFIG_PRODUCTION = {
    "data_generation": {
        "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "SPY", "QQQ"],
        "start_date": "2020-01-01",
        "end_date": "2024-12-31",
        "data_points_per_day": 390,
    },
    "python_benchmarks": {
        "runs_per_operation": 10,
    },
    "description": "Large production-like dataset"
}

CONFIG_REALTIME = {
    "data_generation": {
        "symbols": ["ES", "NQ", "YM", "RTY"],  # Futures contracts
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "data_points_per_day": 1560,  # Every 15 seconds for 6.5 hour session
    },
    "python_benchmarks": {
        "focus": ["streaming", "windowing", "rolling_calculations"],
    },
    "description": "Real-time financial data configuration"
}

CONFIG_EDUCATION = {
    "data_generation": {
        "symbols": ["AAPL", "MSFT", "GOOGL"],
        "start_date": "2024-01-01",
        "end_date": "2024-03-31",
        "data_points_per_day": 50,
    },
    "python_benchmarks": {
        "runs_per_operation": 3,
    },
    "description": "Educational configuration for learning"
}


def create_config_file(scenario: str = "development"):
    """Create a configuration file for a specific scenario"""
    
    scenarios = {
        "development": CONFIG_DEVELOPMENT,
        "production": CONFIG_PRODUCTION,
        "realtime": CONFIG_REALTIME,
        "education": CONFIG_EDUCATION,
    }
    
    if scenario not in scenarios:
        print(f"Unknown scenario: {scenario}")
        print(f"Available: {', '.join(scenarios.keys())}")
        return False
    
    config_dict = BenchmarkConfig()._load_default_config()
    config_dict.update(scenarios[scenario])
    
    filename = f"benchmark_config_{scenario}.json"
    
    with open(filename, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    print(f"Configuration file created: {filename}")
    return True


if __name__ == "__main__":
    # Create default configuration
    config = BenchmarkConfig()
    
    print("Default Configuration:")
    print(json.dumps(config.config, indent=2))
    
    print("\n" + "="*70)
    print("Creating scenario configurations...")
    print("="*70 + "\n")
    
    for scenario in ["development", "production", "realtime", "education"]:
        create_config_file(scenario)
    
    print("\n✓ Configuration files created")
    print("  - benchmark_config_development.json")
    print("  - benchmark_config_production.json")
    print("  - benchmark_config_realtime.json")
    print("  - benchmark_config_education.json")
