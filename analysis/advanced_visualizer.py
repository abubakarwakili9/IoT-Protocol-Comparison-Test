"""
Advanced Visualizer for IoT Protocol Comparison
Creates publication-quality charts and graphs
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json
import os

class ProtocolVisualizer:
    """Creates advanced visualizations for protocol comparison"""
    
    def __init__(self):
        # Set style for publication-quality plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def load_results(self):
        """Load analysis results"""
        try:
            with open('results/complete_analysis.json', 'r') as f:
                self.results = json.load(f)
            return True
        except FileNotFoundError:
            print("❌ No results found. Run analysis first!")
            return False
    
    def create_comparison_chart(self):
        """Create comparison bar chart"""
        if not hasattr(self, 'results'):
            return
            
        comparison = self.results.get('comparison', {})
        
        # Prepare data
        metrics = []
        lwm2m_values = []
        matter_values = []
        
        if 'setup_time' in comparison:
            metrics.append('Setup Time\n(ms)')
            lwm2m_values.append(comparison['setup_time']['lwm2m_ms'])
            matter_values.append(comparison['setup_time']['matter_ms'])
        
        if 'data_efficiency' in comparison:
            metrics.append('Data Size\n(bytes)')
            lwm2m_values.append(comparison['data_efficiency']['lwm2m_bytes'])
            matter_values.append(comparison['data_efficiency']['matter_bytes'])
        
        if 'discovery_time' in comparison:
            metrics.append('Discovery\n(ms)')
            lwm2m_values.append(comparison['discovery_time']['lwm2m_ms'])
            matter_values.append(comparison['discovery_time']['matter_ms'])
        
        # Create chart
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width/2, lwm2m_values, width, label='LwM2M', color='skyblue')
        bars2 = ax.bar(x + width/2, matter_values, width, label='Matter', color='lightcoral')
        
        ax.set_xlabel('Performance Metrics')
        ax.set_ylabel('Values')
        ax.set_title('IoT Protocol Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom')
        
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('results/protocol_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Comparison chart saved as results/protocol_comparison.png")

def main():
    """Generate visualizations"""
    viz = ProtocolVisualizer()
    if viz.load_results():
        viz.create_comparison_chart()

if __name__ == "__main__":
    main()