# analysis/statistical_analyzer.py
"""
Statistical Analysis for Protocol Comparison
Confidence intervals, significance testing, effect sizes
"""
import statistics
import math
from typing import Dict, Any, List, Tuple

class StatisticalAnalyzer:
    """Statistical analysis framework for protocol comparison"""
    
    def __init__(self):
        self.confidence_level = 0.95
        self.alpha = 0.05
    
    def analyze_protocols(self, lwm2m_data: Dict[str, Any], matter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis"""
        
        # Extract metrics for analysis
        lwm2m_metrics = self.extract_metrics(lwm2m_data)
        matter_metrics = self.extract_metrics(matter_data)
        
        # Perform statistical tests
        statistical_results = {
            'descriptive_statistics': {
                'lwm2m': self.calculate_descriptive_stats(lwm2m_metrics),
                'matter': self.calculate_descriptive_stats(matter_metrics)
            },
            'comparative_analysis': self.perform_comparative_analysis(lwm2m_metrics, matter_metrics),
            'effect_sizes': self.calculate_effect_sizes(lwm2m_metrics, matter_metrics),
            'confidence_intervals': self.calculate_confidence_intervals(lwm2m_metrics, matter_metrics),
            'significance_tests': self.perform_significance_tests(lwm2m_metrics, matter_metrics)
        }
        
        return statistical_results
    
    def extract_metrics(self, protocol_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """Extract numerical metrics from protocol data"""
        
        layers = protocol_data.get('layers', {})
        
        return {
            'transport_time': [layers.get('layer_4_transport', {}).get('connection_time_ms', 0)],
            'transport_overhead': [layers.get('layer_4_transport', {}).get('overhead_bytes', 0)],
            'session_time': [layers.get('layer_5_session', {}).get('setup_time_ms', 0)],
            'session_overhead': [layers.get('layer_5_session', {}).get('overhead_bytes', 0)],
            'encoding_time': [layers.get('layer_6_presentation', {}).get('encoding_time_ms', 0)],
            'compression_ratio': [layers.get('layer_6_presentation', {}).get('compression_ratio', 1.0)],
            'discovery_time': [layers.get('layer_7_application', {}).get('discovery_time_ms', 0)],
            'feature_count': [len(layers.get('layer_7_application', {}).get('supported_entities', []))]
        }
    
    def calculate_descriptive_stats(self, metrics: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
        """Calculate descriptive statistics for each metric"""
        
        stats = {}
        for metric_name, values in metrics.items():
            if values:
                stats[metric_name] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
            else:
                stats[metric_name] = {
                    'mean': 0, 'median': 0, 'std_dev': 0,
                    'min': 0, 'max': 0, 'count': 0
                }
        
        return stats
    
    def perform_comparative_analysis(self, lwm2m_metrics: Dict[str, List[float]], 
                                   matter_metrics: Dict[str, List[float]]) -> Dict[str, Any]:
        """Perform comparative analysis between protocols"""
        
        comparisons = {}
        
        for metric_name in lwm2m_metrics.keys():
            lwm2m_values = lwm2m_metrics[metric_name]
            matter_values = matter_metrics[metric_name]
            
            if lwm2m_values and matter_values:
                lwm2m_mean = statistics.mean(lwm2m_values)
                matter_mean = statistics.mean(matter_values)
                
                difference = lwm2m_mean - matter_mean
                percentage_diff = (difference / matter_mean * 100) if matter_mean != 0 else 0
                
                better_protocol = 'LwM2M' if self.is_lower_better(metric_name) and difference < 0 or \
                                           not self.is_lower_better(metric_name) and difference > 0 else 'Matter'
                
                comparisons[metric_name] = {
                    'lwm2m_mean': lwm2m_mean,
                    'matter_mean': matter_mean,
                    'absolute_difference': difference,
                    'percentage_difference': percentage_diff,
                    'better_protocol': better_protocol,
                    'improvement_factor': abs(percentage_diff) / 100
                }
        
        return comparisons
    
    def is_lower_better(self, metric_name: str) -> bool:
        """Determine if lower values are better for a metric"""
        lower_better_metrics = [
            'transport_time', 'transport_overhead', 'session_time', 
            'session_overhead', 'encoding_time', 'discovery_time'
        ]
        return metric_name in lower_better_metrics
    
    def calculate_effect_sizes(self, lwm2m_metrics: Dict[str, List[float]], 
                              matter_metrics: Dict[str, List[float]]) -> Dict[str, float]:
        """Calculate Cohen's d effect sizes"""
        
        effect_sizes = {}
        
        for metric_name in lwm2m_metrics.keys():
            lwm2m_values = lwm2m_metrics[metric_name]
            matter_values = matter_metrics[metric_name]
            
            if len(lwm2m_values) > 0 and len(matter_values) > 0:
                lwm2m_mean = statistics.mean(lwm2m_values)
                matter_mean = statistics.mean(matter_values)
                
                # Pooled standard deviation
                if len(lwm2m_values) > 1 and len(matter_values) > 1:
                    lwm2m_std = statistics.stdev(lwm2m_values)
                    matter_std = statistics.stdev(matter_values)
                    pooled_std = math.sqrt(((len(lwm2m_values) - 1) * lwm2m_std**2 + 
                                          (len(matter_values) - 1) * matter_std**2) / 
                                         (len(lwm2m_values) + len(matter_values) - 2))
                    
                    effect_size = (lwm2m_mean - matter_mean) / pooled_std if pooled_std != 0 else 0
                else:
                    effect_size = 0
                
                effect_sizes[metric_name] = effect_size
        
        return effect_sizes
    
    def calculate_confidence_intervals(self, lwm2m_metrics: Dict[str, List[float]], 
                                     matter_metrics: Dict[str, List[float]]) -> Dict[str, Any]:
        """Calculate confidence intervals for differences"""
        
        confidence_intervals = {}
        z_score = 1.96  # 95% confidence interval
        
        for metric_name in lwm2m_metrics.keys():
            lwm2m_values = lwm2m_metrics[metric_name]
            matter_values = matter_metrics[metric_name]
            
            if lwm2m_values and matter_values:
                lwm2m_mean = statistics.mean(lwm2m_values)
                matter_mean = statistics.mean(matter_values)
                difference = lwm2m_mean - matter_mean
                
                # Standard error of difference (simplified for single measurements)
                if len(lwm2m_values) > 1 and len(matter_values) > 1:
                    lwm2m_std = statistics.stdev(lwm2m_values)
                    matter_std = statistics.stdev(matter_values)
                    se_diff = math.sqrt((lwm2m_std**2 / len(lwm2m_values)) + 
                                       (matter_std**2 / len(matter_values)))
                else:
                    # Assume 10% coefficient of variation for single measurements
                    se_diff = abs(difference) * 0.1
                
                margin_error = z_score * se_diff
                
                confidence_intervals[metric_name] = {
                    'difference': difference,
                    'lower_bound': difference - margin_error,
                    'upper_bound': difference + margin_error,
                    'margin_of_error': margin_error,
                    'confidence_level': '95%'
                }
        
        return confidence_intervals
    
    def perform_significance_tests(self, lwm2m_metrics: Dict[str, List[float]], 
                                  matter_metrics: Dict[str, List[float]]) -> Dict[str, Any]:
        """Perform statistical significance tests"""
        
        significance_results = {
            'test_type': 'Descriptive Analysis (Single Measurement)',
            'alpha_level': self.alpha,
            'results': {}
        }
        
        for metric_name in lwm2m_metrics.keys():
            lwm2m_values = lwm2m_metrics[metric_name]
            matter_values = matter_metrics[metric_name]
            
            if lwm2m_values and matter_values:
                difference = statistics.mean(lwm2m_values) - statistics.mean(matter_values)
                
                # For single measurements, use practical significance
                practical_significance_threshold = {
                    'transport_time': 10,    # 10ms difference
                    'session_time': 50,     # 50ms difference  
                    'encoding_time': 5,     # 5ms difference
                    'discovery_time': 20,   # 20ms difference
                    'transport_overhead': 10, # 10 bytes
                    'session_overhead': 50,   # 50 bytes
                    'compression_ratio': 0.1, # 0.1 ratio difference
                    'feature_count': 2       # 2 features difference
                }
                
                threshold = practical_significance_threshold.get(metric_name, 0)
                is_significant = abs(difference) > threshold
                
                significance_results['results'][metric_name] = {
                    'difference': difference,
                    'threshold': threshold,
                    'practically_significant': is_significant,
                    'effect_magnitude': 'Large' if abs(difference) > threshold * 2 else 
                                      'Medium' if abs(difference) > threshold else 'Small'
                }
        
        return significance_results