import React from 'react';
import { clsx } from 'clsx';
import { TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react';
import { StatisticalMetric } from '../../types/comparison';

interface StatisticalSummaryProps {
  metrics: StatisticalMetric[];
  className?: string;
}

interface MetricCardProps {
  metric: StatisticalMetric;
}

const MetricCard: React.FC<MetricCardProps> = ({ metric }) => {
  const difference = metric.dataset_a_value - metric.dataset_b_value;
  const relativeDifference = metric.dataset_b_value !== 0 
    ? ((difference / metric.dataset_b_value) * 100)
    : 0;
  
  const isSignificant = metric.statistical_significance < 0.05;
  const effectSizeCategory = 
    Math.abs(metric.effect_size) < 0.2 ? 'small' :
    Math.abs(metric.effect_size) < 0.5 ? 'medium' : 'large';

  const getTrendIcon = () => {
    if (Math.abs(difference) < 0.01) {
      return <Minus className="w-5 h-5 text-gray-500" />;
    }
    return difference > 0 
      ? <TrendingUp className="w-5 h-5 text-green-500" />
      : <TrendingDown className="w-5 h-5 text-red-500" />;
  };

  const getSignificanceColor = () => {
    if (!isSignificant) return 'text-gray-500';
    return effectSizeCategory === 'large' ? 'text-red-600' :
           effectSizeCategory === 'medium' ? 'text-orange-500' : 'text-yellow-600';
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-gray-900 capitalize">
          {metric.name.replace(/_/g, ' ')}
        </h3>
        {getTrendIcon()}
      </div>

      <div className="space-y-2">
        {/* Values */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-gray-500">Dataset A</div>
            <div className="font-medium">{metric.dataset_a_value.toFixed(3)}</div>
          </div>
          <div>
            <div className="text-gray-500">Dataset B</div>
            <div className="font-medium">{metric.dataset_b_value.toFixed(3)}</div>
          </div>
        </div>

        {/* Difference */}
        <div className="pt-2 border-t border-gray-100">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Difference</span>
            <div className="text-right">
              <div className={clsx('font-medium', {
                'text-green-600': difference > 0,
                'text-red-600': difference < 0,
                'text-gray-600': Math.abs(difference) < 0.01
              })}>
                {difference >= 0 ? '+' : ''}{difference.toFixed(3)}
              </div>
              <div className="text-xs text-gray-400">
                ({relativeDifference >= 0 ? '+' : ''}{relativeDifference.toFixed(1)}%)
              </div>
            </div>
          </div>
        </div>

        {/* Statistical significance */}
        <div className="space-y-1 text-xs">
          <div className="flex items-center justify-between">
            <span className="text-gray-500">p-value</span>
            <span className={getSignificanceColor()}>
              {metric.statistical_significance.toExponential(2)}
            </span>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-gray-500">Effect size</span>
            <span className={getSignificanceColor()}>
              {metric.effect_size.toFixed(3)} ({effectSizeCategory})
            </span>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-gray-500">95% CI</span>
            <span className="text-gray-600">
              [{metric.confidence_interval_lower.toFixed(3)}, {metric.confidence_interval_upper.toFixed(3)}]
            </span>
          </div>
        </div>

        {/* Significance indicator */}
        <div className={clsx('flex items-center gap-2 px-2 py-1 rounded text-xs', {
          'bg-red-50 text-red-700': isSignificant && effectSizeCategory === 'large',
          'bg-orange-50 text-orange-700': isSignificant && effectSizeCategory === 'medium',
          'bg-yellow-50 text-yellow-700': isSignificant && effectSizeCategory === 'small',
          'bg-gray-50 text-gray-600': !isSignificant
        })}>
          {isSignificant && <AlertTriangle className="w-3 h-3" />}
          <span>
            {isSignificant ? `Significant ${effectSizeCategory} effect` : 'Not significant'}
          </span>
        </div>
      </div>
    </div>
  );
};

export const StatisticalSummary: React.FC<StatisticalSummaryProps> = ({ 
  metrics, 
  className 
}) => {
  if (metrics.length === 0) {
    return (
      <div className={clsx('text-center py-8 text-gray-500', className)}>
        No statistical metrics available
      </div>
    );
  }

  const significantMetrics = metrics.filter(m => m.statistical_significance < 0.05);
  const largeEffects = metrics.filter(m => Math.abs(m.effect_size) >= 0.5);

  return (
    <div className={clsx('space-y-6', className)}>
      {/* Overview */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2">Statistical Overview</h3>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <div className="text-blue-700 font-medium">{metrics.length}</div>
            <div className="text-blue-600">Total Metrics</div>
          </div>
          <div>
            <div className="text-blue-700 font-medium">{significantMetrics.length}</div>
            <div className="text-blue-600">Significant (p &lt; 0.05)</div>
          </div>
          <div>
            <div className="text-blue-700 font-medium">{largeEffects.length}</div>
            <div className="text-blue-600">Large Effects (|d| ≥ 0.5)</div>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, index) => (
          <MetricCard key={`${metric.name}-${index}`} metric={metric} />
        ))}
      </div>

      {/* Key Findings */}
      {significantMetrics.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h3 className="font-semibold text-amber-900 mb-2">Key Findings</h3>
          <ul className="space-y-1 text-sm text-amber-800">
            {largeEffects.map((metric, index) => (
              <li key={index}>
                • <strong>{metric.name.replace(/_/g, ' ')}</strong> shows a large effect 
                ({metric.effect_size > 0 ? 'Dataset A higher' : 'Dataset B higher'})
              </li>
            ))}
            {significantMetrics.length > largeEffects.length && (
              <li>
                • {significantMetrics.length - largeEffects.length} additional significant differences detected
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};