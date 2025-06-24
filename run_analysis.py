#!/usr/bin/env python3
"""
Simple IoT Protocol Comparison Runner
Runs both LwM2M and Matter analyzers and creates basic comparison
Windows Compatible Version
"""

import asyncio
import subprocess
import json
import sys
import time
import os
from pathlib import Path
from datetime import datetime

class SimpleProtocolRunner:
    """Simple runner for protocol comparison"""
    
    def __init__(self):
        self.results_dir = Path("./results")
        self.results_dir.mkdir(exist_ok=True)
        
    async def run_lwm2m_analysis(self):
        """Run LwM2M analysis"""
        print(">>> Running LwM2M Protocol Analysis...")
        print("=" * 50)
        
        try:
            # Change to LwM2M directory and run
            lwm2m_dir = Path("lwm2m-project")
            
            if not lwm2m_dir.exists():
                print(">>> lwm2m-project directory not found")
                return None
            
            # Set environment for UTF-8 output
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # Run LwM2M analyzer with proper encoding
            result = subprocess.run([
                sys.executable, "lwm2m_analyzer.py"
            ], cwd=lwm2m_dir, capture_output=True, text=True, 
               timeout=60, encoding='utf-8', errors='replace', env=env)
            
            if result.returncode == 0:
                print(">>> LwM2M analysis completed!")
                print(">>> LwM2M Output:")
                # Clean output of any problematic characters
                clean_output = result.stdout.encode('ascii', 'replace').decode('ascii')
                print(clean_output)
                
                # Load results
                results_file = Path("lwm2m_real_analysis.json")
                if results_file.exists():
                    with open(results_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    print(">>> LwM2M results file not found")
                    return None
            else:
                print(">>> LwM2M analysis failed:")
                clean_error = result.stderr.encode('ascii', 'replace').decode('ascii')
                print(clean_error)
                return None
                
        except Exception as e:
            print(f">>> LwM2M analysis error: {e}")
            return None
    
    def run_matter_analysis(self):
        """Run Matter analysis"""
        print("\n>>> Running Matter Protocol Analysis...")
        print("=" * 50)
        
        try:
            # Run Matter analyzer
            matter_exe = Path("matter-project/target/release/matter_analyzer.exe")
            if not matter_exe.exists():
                print(">>> Matter analyzer not found. Please build it first:")
                print("cd matter-project && cargo build --release")
                return None
            
            # Run with encoding handling
            result = subprocess.run([
                str(matter_exe)
            ], capture_output=True, timeout=60, encoding='utf-8', errors='replace')
            
            if result.returncode == 0:
                print(">>> Matter analysis completed!")
                print(">>> Matter Output:")
                # Clean output for display
                if result.stdout:
                    clean_output = result.stdout.encode('ascii', 'replace').decode('ascii')
                    print(clean_output)
                
                # Load results
                results_file = Path("matter_real_analysis.json")
                if results_file.exists():
                    with open(results_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    print(">>> Matter results file not found")
                    return None
            else:
                print(">>> Matter analysis failed:")
                if result.stderr:
                    clean_error = result.stderr.encode('ascii', 'replace').decode('ascii')
                    print(clean_error)
                return None
                
        except Exception as e:
            print(f">>> Matter analysis error: {e}")
            return None
    
    def create_simple_comparison(self, lwm2m_data, matter_data):
        """Create simple comparison report"""
        print("\n>>> Creating Protocol Comparison...")
        
        # Extract key metrics
        lwm2m_metrics = {
            'protocol': 'LwM2M',
            'transport_time': lwm2m_data['osi_layer_4_transport']['connection_time_ms'],
            'session_time': lwm2m_data['osi_layer_5_session']['registration_time_ms'],
            'encoding_time': lwm2m_data['osi_layer_6_presentation']['encoding_time_ms'],
            'discovery_time': lwm2m_data['osi_layer_7_application']['discovery_time_ms'],
            'total_latency': lwm2m_data['summary_metrics']['total_latency_ms'],
            'overall_efficiency': lwm2m_data['summary_metrics']['overall_efficiency']
        }
        
        matter_metrics = {
            'protocol': 'Matter',
            'transport_time': matter_data['osi_layer_4_transport']['udp_discovery_time_ms'] + 
                           matter_data['osi_layer_4_transport']['tcp_connection_time_ms'],
            'session_time': matter_data['osi_layer_5_session']['commissioning_time_ms'],
            'encoding_time': matter_data['osi_layer_6_presentation']['encoding_time_ms'],
            'discovery_time': matter_data['osi_layer_7_application']['discovery_time_ms'],
            'total_latency': matter_data['summary_metrics']['total_latency_ms'],
            'overall_efficiency': matter_data['summary_metrics']['overall_efficiency']
        }
        
        # Create comparison report
        comparison = {
            'comparison_timestamp': datetime.now().isoformat(),
            'protocols_compared': ['LwM2M', 'Matter'],
            'lwm2m_metrics': lwm2m_metrics,
            'matter_metrics': matter_metrics,
            'comparison_results': {
                'transport_winner': 'LwM2M' if lwm2m_metrics['transport_time'] < matter_metrics['transport_time'] else 'Matter',
                'session_winner': 'LwM2M' if lwm2m_metrics['session_time'] < matter_metrics['session_time'] else 'Matter',
                'encoding_winner': 'LwM2M' if lwm2m_metrics['encoding_time'] < matter_metrics['encoding_time'] else 'Matter',
                'discovery_winner': 'LwM2M' if lwm2m_metrics['discovery_time'] < matter_metrics['discovery_time'] else 'Matter',
                'overall_winner': 'LwM2M' if lwm2m_metrics['overall_efficiency'] > matter_metrics['overall_efficiency'] else 'Matter'
            },
            'performance_differences': {
                'transport_difference_ms': abs(lwm2m_metrics['transport_time'] - matter_metrics['transport_time']),
                'session_difference_ms': abs(lwm2m_metrics['session_time'] - matter_metrics['session_time']),
                'total_latency_difference_ms': abs(lwm2m_metrics['total_latency'] - matter_metrics['total_latency']),
                'efficiency_difference': abs(lwm2m_metrics['overall_efficiency'] - matter_metrics['overall_efficiency'])
            }
        }
        
        return comparison
    
    def save_results(self, lwm2m_data, matter_data, comparison):
        """Save all results"""
        print("\n>>> Saving Results...")
        
        # Save individual protocol results
        with open(self.results_dir / "lwm2m_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(lwm2m_data, f, indent=4)
        
        with open(self.results_dir / "matter_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(matter_data, f, indent=4)
        
        # Save comparison
        with open(self.results_dir / "protocol_comparison.json", 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=4)
        
        print(f">>> Results saved to: {self.results_dir}")
        print(f">>> Files created:")
        print(f"   - lwm2m_analysis.json")
        print(f"   - matter_analysis.json") 
        print(f"   - protocol_comparison.json")
    
    def display_results(self, comparison):
        """Display comparison results"""
        print("\n" + "=" * 70)
        print("*** IoT PROTOCOL COMPARISON RESULTS ***")
        print("   LwM2M vs Matter - OSI Layer 4-7 Analysis")
        print("=" * 70)
        
        lwm2m = comparison['lwm2m_metrics']
        matter = comparison['matter_metrics']
        results = comparison['comparison_results']
        
        print(f"\n>>> LAYER-BY-LAYER COMPARISON:")
        print(f"   Layer 4 (Transport): {results['transport_winner']} wins")
        print(f"      LwM2M: {lwm2m['transport_time']:.1f}ms vs Matter: {matter['transport_time']:.1f}ms")
        
        print(f"   Layer 5 (Session): {results['session_winner']} wins")
        print(f"      LwM2M: {lwm2m['session_time']:.1f}ms vs Matter: {matter['session_time']:.1f}ms")
        
        print(f"   Layer 6 (Presentation): {results['encoding_winner']} wins")
        print(f"      LwM2M: {lwm2m['encoding_time']:.1f}ms vs Matter: {matter['encoding_time']:.1f}ms")
        
        print(f"   Layer 7 (Application): {results['discovery_winner']} wins")
        print(f"      LwM2M: {lwm2m['discovery_time']:.1f}ms vs Matter: {matter['discovery_time']:.1f}ms")
        
        print(f"\n*** OVERALL WINNER: {results['overall_winner']} ***")
        print(f"   LwM2M Efficiency: {lwm2m['overall_efficiency']:.2f}")
        print(f"   Matter Efficiency: {matter['overall_efficiency']:.2f}")
        
        print(f"\n>>> PERFORMANCE SUMMARY:")
        print(f"   Total Latency - LwM2M: {lwm2m['total_latency']:.1f}ms, Matter: {matter['total_latency']:.1f}ms")
        print(f"   Difference: {comparison['performance_differences']['total_latency_difference_ms']:.1f}ms")
        
        print(f"\n>>> DETAILED RESULTS: {self.results_dir}")
        print("=" * 70)
    
    async def run_complete_comparison(self):
        """Run complete protocol comparison"""
        print("*** IoT PROTOCOL COMPARISON ***")
        print("Real LwM2M vs Real Matter Implementation")
        print("=" * 70)
        
        start_time = time.time()
        
        # Run both analyzers
        lwm2m_data = await self.run_lwm2m_analysis()
        matter_data = self.run_matter_analysis()
        
        if not lwm2m_data or not matter_data:
            print(">>> Failed to run both protocol analyses")
            return False
        
        # Create comparison
        comparison = self.create_simple_comparison(lwm2m_data, matter_data)
        
        # Save results
        self.save_results(lwm2m_data, matter_data, comparison)
        
        # Display results
        self.display_results(comparison)
        
        total_time = time.time() - start_time
        print(f"\n>>> Total Analysis Time: {total_time:.1f} seconds")
        print("*** Analysis completed successfully! ***")
        
        return True

async def main():
    """Main execution"""
    runner = SimpleProtocolRunner()
    success = await runner.run_complete_comparison()
    
    if success:
        print("\n*** SUCCESS! Protocol comparison completed! ***")
        print(">>> Check ./results/ folder for detailed analysis")
    else:
        print("\n>>> Analysis failed - check error messages above")

if __name__ == "__main__":
    asyncio.run(main())