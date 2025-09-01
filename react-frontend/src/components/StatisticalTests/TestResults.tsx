import React from 'react';
import { clsx } from 'clsx';
import { TrendingUp, TrendingDown, Minus, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { StatisticalMetric } from '../../types/comparison';

interface TestResultsProps {
  metrics: StatisticalMetric[];
  significanceLevel: number;
  className?: string;
}

interface StatisticalTest {
  name: string;
  description: string;
  metric: StatisticalMetric;
  interpretation: string;
  recommendation: string;
}

export const TestResults: React.FC<TestResultsProps> = ({ 
  metrics, 
  significanceLevel = 0.05, 
  className 
}) => {
  const statisticalTests: StatisticalTest[] = metrics.map(metric => {
    const isSignificant = metric.statistical_significance < significanceLevel;
    const effectSize = Math.abs(metric.effect_size);
    const effectCategory = 
      effectSize < 0.2 ? 'negligible' :
      effectSize < 0.5 ? 'small' :
      effectSize < 0.8 ? 'medium' : 'large';
    
    const difference = metric.dataset_a_value - metric.dataset_b_value;
    const direction = difference > 0 ? 'higher' : 'lower';
    const absoluteDiff = Math.abs(difference);
    const relativeDiff = metric.dataset_b_value !== 0 
      ? Math.abs(difference / metric.dataset_b_value * 100)
      : 0;

    let interpretation = '';
    let recommendation = '';

    if (!isSignificant) {
      interpretation = `No statistically significant difference detected (p = ${metric.statistical_significance.toFixed(4)} > ${significanceLevel})`;
      recommendation = 'The observed difference could be due to random variation. Consider collecting more data or investigating other metrics.';
    } else {
      interpretation = `Dataset A shows ${direction} values with ${effectCategory} effect size (d = ${metric.effect_size.toFixed(3)}, p = ${metric.statistical_significance.toExponential(3)})`;
      
      if (effectCategory === 'large') {
        recommendation = `Strong evidence of meaningful difference. This ${metric.name} difference should be considered in model selection.`;
      } else if (effectCategory === 'medium') {
        recommendation = `Moderate difference detected. Consider practical significance alongside statistical significance.`;
      } else {
        recommendation = `Small but significant difference. May not be practically meaningful depending on use case.`;
      }
    }

    return {
      name: metric.name, // Now using clean names from backend
      description: `Comparing ${metric.dataset_a} vs ${metric.dataset_b}`,
      metric,
      interpretation,
      recommendation
    };
  });

  const significantTests = statisticalTests.filter(t => t.metric.statistical_significance < significanceLevel);
  const largeEffectTests = statisticalTests.filter(t => Math.abs(t.metric.effect_size) >= 0.8);

  if (metrics.length === 0) {
    return (
      <div className={clsx('text-center py-8 text-gray-500', className)}>
        <Info className="w-8 h-8 mx-auto mb-2" />
        <p>No statistical test results available</p>
      </div>
    );
  }

  // This component is now redundant - StatisticalSummary provides all this functionality
  // in a more business-focused way. Return null to hide this section.
  return null;
};