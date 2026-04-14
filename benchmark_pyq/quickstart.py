#!/usr/bin/env python
"""
Quick Start Script for Python vs Q Benchmark Comparison
Run this to generate data and run all benchmarks with one command
"""

import os
import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Python vs Q Financial Database Benchmark Suite'
    )
    parser.add_argument(
        '--mode',
        choices=['quick', 'full', 'analysis', 'mcp'],
        default='quick',
        help='Benchmark mode (quick/full/analysis/mcp)'
    )
    parser.add_argument(
        '--symbols',
        nargs='+',
        default=['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
        help='Stock symbols to benchmark'
    )
    parser.add_argument(
        '--output',
        default='benchmark_results',
        help='Output directory for results'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("Python vs Q Financial Database Benchmarking")
    print("="*70 + "\n")
    
    # Check dependencies
    try:
        import pandas
        import numpy
        print("✓ Required packages found")
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("  Install with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    os.chdir(args.output)
    
    if args.mode == 'quick':
        print("\n📊 Quick Benchmark Mode")
        print("   - Generate sample data (100K-1M records)")
        print("   - Run Python benchmarks (Pandas + SQL)")
        print("   - Estimate Q performance")
        print("   - Generate summary report")
        
        from comprehensive_benchmark import ComprehensiveBenchmarkRunner
        runner = ComprehensiveBenchmarkRunner()
        
        # Reduce data size for quick mode
        runner.run_all(symbols=['AAPL', 'MSFT', 'GOOGL'])
        
    elif args.mode == 'full':
        print("\n🔬 Full Benchmark Mode")
        print("   - Generate full data (2.5M+ records)")
        print("   - Run all Python benchmarks (Pandas + SQL + Polars)")
        print("   - Detailed Q analysis")
        print("   - Comprehensive reports")
        
        from comprehensive_benchmark import ComprehensiveBenchmarkRunner
        runner = ComprehensiveBenchmarkRunner()
        runner.run_all(symbols=args.symbols)
        
    elif args.mode == 'analysis':
        print("\n📈 Analysis Only Mode")
        print("   - Analyze existing benchmark results")
        print("   - Generate comparison insights")
        print("   - Speedup estimates")
        
        try:
            from q_benchmark_reference import QBenchmarkReference
            import json
            
            if os.path.exists('python_benchmark_results.json'):
                with open('python_benchmark_results.json') as f:
                    results = json.load(f)
                
                ref = QBenchmarkReference()
                for result in results.get('results', []):
                    if result['library'] == 'Pandas':
                        ref.set_python_time(
                            result['operation'],
                            result['duration_ms']
                        )
                
                ref.print_analysis()
            else:
                print("No previous benchmark results found")
                print("Run with --mode quick or --mode full first")
        except Exception as e:
            print(f"Error: {e}")
            
    elif args.mode == 'mcp':
        print("\n🔧 MCP Server Mode")
        print("   Starting MCP server for automated benchmarking")
        print("   Connect Claude or other MCP clients")
        
        try:
            from mcp_benchmark_server import BenchmarkMCPServer
            server = BenchmarkMCPServer()
            if server.server:
                print("\n✓ MCP Server initialized")
                print("  Available tools:")
                print("  - generate_financial_data")
                print("  - run_python_benchmark")
                print("  - generate_comparison_report")
                print("  - analyze_speedup")
                print("  - get_q_code_template")
            else:
                print("MCP not installed. Install with: pip install mcp")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*70)
    print("Results saved to: " + os.path.abspath('.')
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
