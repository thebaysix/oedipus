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
        recommendation = `Strong evidence of meaningful difference. This ${metric.name.replace(/_/g, ' ')} difference should be considered in model selection.`;
      } else if (effectCategory === 'medium') {
        recommendation = `Moderate difference detected. Consider practical significance alongside statistical significance.`;
      } else {
        recommendation = `Small but significant difference. May not be practically meaningful depending on use case.`;
      }
    }

    return {
      name: metric.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      description: `Comparing ${metric.name.replace(/_/g, ' ')} between datasets`,
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

  return (
    <div className={clsx('space-y-6', className)}>
      {/* Overview */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-3">Statistical Test Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="text-center">
            <div className="text-xl font-bold text-blue-700">{statisticalTests.length}</div>
            <div className="text-blue-600">Total Tests</div>
          </div>
          <div className="text-center">
            <div className="text-xl font-bold text-green-600">{significantTests.length}</div>
            <div className="text-blue-600">Significant</div>
          </div>
          <div className="text-center">
            <div className="text-xl font-bold text-orange-600">{largeEffectTests.length}</div>
            <div className="text-blue-600">Large Effects</div>
          </div>
          <div className="text-center">
            <div className="text-xl font-bold text-gray-600">α = {significanceLevel}</div>
            <div className="text-blue-600">Threshold</div>
          </div>
        </div>
      </div>

      {/* Individual Test Results */}
      <div className="space-y-4">
        {statisticalTests.map((test, index) => {
          const isSignificant = test.metric.statistical_significance < significanceLevel;
          const effectSize = Math.abs(test.metric.effect_size);
          const difference = test.metric.dataset_a_value - test.metric.dataset_b_value;

          return (
            <div
              key={index}
              className={clsx(
                'border rounded-lg p-4 bg-white',
                isSignificant ? 'border-orange-200' : 'border-gray-200'
              )}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  {isSignificant ? (
                    <AlertTriangle className="w-5 h-5 text-orange-500" />
                  ) : (
                    <CheckCircle className="w-5 h-5 text-gray-400" />
                  )}
                  <div>
                    <h4 className="font-semibold text-gray-900">{test.name}</h4>
                    <p className="text-sm text-gray-600">{test.description}</p>
                  </div>
                </div>
                
                {/* Trend indicator */}
                <div className="flex items-center gap-2">
                  {Math.abs(difference) < 0.01 ? (
                    <Minus className="w-5 h-5 text-gray-500" />
                  ) : difference > 0 ? (
                    <TrendingUp className="w-5 h-5 text-green-500" />
                  ) : (
                    <TrendingDown className="w-5 h-5 text-red-500" />
                  )}
                  <span className={clsx('text-sm font-medium', {
                    'text-green-600': difference > 0,
                    'text-red-600': difference < 0,
                    'text-gray-600': Math.abs(difference) < 0.01
                  })}>
                    {difference > 0 ? '+' : ''}{difference.toFixed(3)}
                  </span>
                </div>
              </div>

              {/* Statistical Details */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm bg-gray-50 rounded p-3">
                <div>
                  <div className="text-gray-500">p-value</div>
                  <div className={clsx('font-medium', {
                    'text-red-600': isSignificant,
                    'text-gray-600': !isSignificant
                  })}>
                    {test.metric.statistical_significance < 0.001 
                      ? '< 0.001' 
                      : test.metric.statistical_significance.toFixed(4)
                    }
                  </div>
                </div>
                <div>
                  <div className="text-gray-500">Effect Size</div>
                  <div className={clsx('font-medium', {
                    'text-red-600': effectSize >= 0.8,
                    'text-orange-600': effectSize >= 0.5,
                    'text-yellow-600': effectSize >= 0.2,
                    'text-gray-600': effectSize < 0.2
                  })}>
                    {test.metric.effect_size.toFixed(3)}
                  </div>
                </div>
                <div>
                  <div className="text-gray-500">95% CI</div>
                  <div className="font-medium text-gray-700 text-xs">
                    [{test.metric.confidence_interval_lower.toFixed(3)}, {test.metric.confidence_interval_upper.toFixed(3)}]
                  </div>
                </div>
                <div>
                  <div className="text-gray-500">Status</div>
                  <div className={clsx('text-xs px-2 py-1 rounded font-medium', {
                    'bg-red-100 text-red-700': isSignificant && effectSize >= 0.8,
                    'bg-orange-100 text-orange-700': isSignificant && effectSize >= 0.5,
                    'bg-yellow-100 text-yellow-700': isSignificant && effectSize < 0.5,
                    'bg-gray-100 text-gray-700': !isSignificant
                  })}>
                    {!isSignificant ? 'Not Significant' :
                     effectSize >= 0.8 ? 'Large Effect' :
                     effectSize >= 0.5 ? 'Medium Effect' : 'Small Effect'}
                  </div>
                </div>
              </div>

              {/* Interpretation */}
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium text-gray-700">Interpretation: </span>
                  <span className="text-gray-600">{test.interpretation}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">Recommendation: </span>
                  <span className="text-gray-600">{test.recommendation}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Key Insights */}
      {significantTests.length > 0 && (
        <div className={clsx('rounded-lg p-4', {
          'bg-red-50 border border-red-200': largeEffectTests.length > 0,
          'bg-orange-50 border border-orange-200': largeEffectTests.length === 0
        })}>
          <h4 className={clsx('font-semibold mb-2', {
            'text-red-900': largeEffectTests.length > 0,
            'text-orange-900': largeEffectTests.length === 0
          })}>
            Key Findings
          </h4>
          <ul className={clsx('text-sm space-y-1', {
            'text-red-800': largeEffectTests.length > 0,
            'text-orange-800': largeEffectTests.length === 0
          })}>
            {largeEffectTests.length > 0 && (
              <li>• {largeEffectTests.length} metric{largeEffectTests.length > 1 ? 's show' : ' shows'} large, practically significant differences</li>
            )}
            <li>• {significantTests.length} out of {statisticalTests.length} metrics show statistically significant differences</li>
            <li>• Consider the practical impact of these differences in your specific use case</li>
            {significantTests.length === statisticalTests.length && (
              <li>• All metrics show significant differences - strong evidence of model performance differences</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};