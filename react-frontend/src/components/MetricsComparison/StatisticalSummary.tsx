import React, { useState } from 'react';
import { clsx } from 'clsx';
import { TrendingUp, TrendingDown, Minus, AlertTriangle, ChevronDown, ChevronRight, Star } from 'lucide-react';
import { StatisticalMetric } from '../../types/comparison';

interface StatisticalSummaryProps {
  metrics: StatisticalMetric[];
  className?: string;
}

interface MetricCardProps {
  metric: StatisticalMetric;
}

// Helper functions for business-focused interpretations
const getSignificanceStars = (pValue: number): { stars: number; label: string } => {
  if (pValue < 0.001) return { stars: 3, label: 'Highly significant difference' };
  if (pValue < 0.01) return { stars: 2, label: 'Very significant difference' };
  if (pValue < 0.05) return { stars: 1, label: 'Significant difference' };
  return { stars: 0, label: 'No significant difference' };
};

const getEffectSizeIndicator = (effectSize: number): { icon: string; label: string; color: string } => {
  const absEffect = Math.abs(effectSize);
  if (absEffect >= 0.8) return { icon: '🔴', label: 'Large impact', color: 'text-red-600' };
  if (absEffect >= 0.5) return { icon: '🟡', label: 'Medium impact', color: 'text-orange-600' };
  if (absEffect >= 0.2) return { icon: '🟢', label: 'Small impact', color: 'text-green-600' };
  return { icon: '⚪', label: 'Minimal impact', color: 'text-gray-600' };
};

const getConfidenceIndicator = (ciLower: number, ciUpper: number): { icon: string; label: string; color: string } => {
  const includesZero = ciLower <= 0 && ciUpper >= 0;
  if (!includesZero) return { icon: '✅', label: 'High confidence', color: 'text-green-600' };
  return { icon: '⚠️', label: 'Low confidence', color: 'text-yellow-600' };
};

const generateBusinessInterpretation = (metric: StatisticalMetric): string => {
  const difference = metric.dataset_b_value - metric.dataset_a_value; // Dataset B relative to Dataset A
  const isSignificant = metric.statistical_significance < 0.05;
  const effectSize = Math.abs(metric.effect_size);
  const metricName = metric.name.replace(/_/g, ' ').toLowerCase();
  const direction = difference > 0 ? 'higher' : 'lower';
  const relativeDiff = metric.dataset_a_value !== 0 ? Math.abs(difference / metric.dataset_a_value * 100) : 0;

  if (!isSignificant) {
    return `Both datasets show similar values for ${metricName}. The observed ${relativeDiff.toFixed(1)}% difference is likely due to normal variation.`;
  }

  if (effectSize >= 0.8) {
    return `Dataset B shows substantially ${direction} values for ${metricName} (${relativeDiff.toFixed(1)}% difference). This is a major distinguishing factor between the datasets.`;
  } else if (effectSize >= 0.5) {
    return `Dataset B shows moderately ${direction} values for ${metricName} (${relativeDiff.toFixed(1)}% difference). This difference may be meaningful for your use case.`;
  } else {
    return `Dataset B shows slightly ${direction} values for ${metricName} (${relativeDiff.toFixed(1)}% difference). While statistically significant, the practical impact may be limited.`;
  }
};

const generateBusinessRecommendation = (metric: StatisticalMetric): string => {
  const isSignificant = metric.statistical_significance < 0.05;
  const effectSize = Math.abs(metric.effect_size);
  const metricName = metric.name.replace(/_/g, ' ').toLowerCase();

  if (!isSignificant) {
    return `Consider this metric neutral in your model selection. Focus on other differentiating factors.`;
  }

  if (effectSize >= 0.8) {
    return `Prioritize this metric in your decision-making. The large difference suggests ${metricName} could significantly impact your application's performance.`;
  } else if (effectSize >= 0.5) {
    return `Weigh this metric against your specific requirements. The moderate difference in ${metricName} may be important depending on your use case.`;
  } else {
    return `Consider whether this small difference in ${metricName} matters for your specific application. Other factors may be more decisive.`;
  }
};

const MetricCard: React.FC<MetricCardProps> = ({ metric }) => {
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);
  
  const difference = metric.dataset_b_value - metric.dataset_a_value; // Dataset B relative to Dataset A
  const relativeDifference = metric.dataset_a_value !== 0 
    ? ((difference / metric.dataset_a_value) * 100)
    : 0;
  
  const isSignificant = metric.statistical_significance < 0.05;
  const significance = getSignificanceStars(metric.statistical_significance);
  const effectIndicator = getEffectSizeIndicator(metric.effect_size);
  const confidenceIndicator = getConfidenceIndicator(metric.confidence_interval_lower, metric.confidence_interval_upper);
  
  const interpretation = generateBusinessInterpretation(metric);
  const recommendation = generateBusinessRecommendation(metric);

  const getTrendIcon = () => {
    if (Math.abs(difference) < 0.01) {
      return <Minus className="w-5 h-5 text-gray-500" />;
    }
    return difference > 0 
      ? <TrendingUp className="w-5 h-5 text-green-500" />
      : <TrendingDown className="w-5 h-5 text-red-500" />;
  };

  const renderStars = (count: number) => {
    return (
      <div className="flex items-center gap-1">
        {[1, 2, 3].map((star) => (
          <Star
            key={star}
            className={clsx('w-4 h-4', {
              'text-yellow-400 fill-yellow-400': star <= count,
              'text-gray-300': star > count
            })}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white">
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-gray-900 capitalize">
          {metric.name.replace(/_/g, ' ')}
        </h3>
        {getTrendIcon()}
      </div>

      {/* Dataset Values - Always Visible */}
      <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
        <div>
          <div className="text-gray-500">Dataset A</div>
          <div className="font-medium text-lg">{metric.dataset_a_value.toFixed(3)}</div>
        </div>
        <div>
          <div className="text-gray-500">Dataset B</div>
          <div className="font-medium text-lg">{metric.dataset_b_value.toFixed(3)}</div>
        </div>
      </div>

      {/* Difference - Always Visible */}
      <div className="mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-500">Difference</span>
          <div className="text-right">
            <div className={clsx('font-medium text-lg', {
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

      {/* Business-focused indicators */}
      <div className="space-y-3 mb-4">
        {/* Significance Rating */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Statistical Significance</span>
          <div className="flex items-center gap-2">
            {renderStars(significance.stars)}
            <span className="text-xs text-gray-500">{significance.label}</span>
          </div>
        </div>

        {/* Effect Size Indicator */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Business Impact</span>
          <div className="flex items-center gap-2">
            <span className="text-lg">{effectIndicator.icon}</span>
            <span className={clsx('text-xs font-medium', effectIndicator.color)}>
              {effectIndicator.label}
            </span>
          </div>
        </div>

        {/* Confidence Indicator */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Result Confidence</span>
          <div className="flex items-center gap-2">
            <span className="text-lg">{confidenceIndicator.icon}</span>
            <span className={clsx('text-xs font-medium', confidenceIndicator.color)}>
              {confidenceIndicator.label}
            </span>
          </div>
        </div>
      </div>

      {/* Business Interpretation */}
      <div className="space-y-3 mb-4 p-3 bg-blue-50 rounded-lg">
        <div>
          <h4 className="text-sm font-medium text-blue-900 mb-1">Interpretation</h4>
          <p className="text-sm text-blue-800">{interpretation}</p>
        </div>
        <div>
          <h4 className="text-sm font-medium text-blue-900 mb-1">Recommendation</h4>
          <p className="text-sm text-blue-800">{recommendation}</p>
        </div>
      </div>

      {/* Expandable Technical Details */}
      <div className="border-t border-gray-200 pt-3">
        <button
          onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
          className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
        >
          {showTechnicalDetails ? (
            <ChevronDown className="w-4 h-4" />
          ) : (
            <ChevronRight className="w-4 h-4" />
          )}
          Statistical Details
        </button>

        {showTechnicalDetails && (
          <div className="mt-3 space-y-3">
            {/* Statistical metrics */}
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-gray-500">p-value</span>
                <span className={clsx('font-medium', {
                  'text-red-600': metric.statistical_significance < 0.001,
                  'text-orange-600': metric.statistical_significance < 0.01,
                  'text-yellow-600': metric.statistical_significance < 0.05,
                  'text-gray-600': metric.statistical_significance >= 0.05
                })}>
                  {metric.statistical_significance < 0.001 
                    ? '< 0.001' 
                    : metric.statistical_significance.toFixed(4)
                  }
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-500">Effect size (Cohen's d)</span>
                <span className={clsx('font-medium', effectIndicator.color)}>
                  {metric.effect_size.toFixed(3)}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-500">95% Confidence Interval</span>
                <span className="text-gray-600 font-mono text-sm">
                  [{metric.confidence_interval_lower.toFixed(3)}, {metric.confidence_interval_upper.toFixed(3)}]
                </span>
              </div>
            </div>

            {/* Technical Interpretation */}
            <div className="pt-2 border-t border-gray-200 text-xs text-gray-600">
              <p><strong>Technical Note:</strong> Effect size (Cohen's d) measures the magnitude of difference in standard deviation units. Confidence interval shows the range where the true difference likely falls with 95% confidence.</p>
            </div>
          </div>
        )}
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

  const highImpactMetrics = metrics.filter(m => Math.abs(m.effect_size) >= 0.8);
  const mediumImpactMetrics = metrics.filter(m => Math.abs(m.effect_size) >= 0.5 && Math.abs(m.effect_size) < 0.8);
  const highConfidenceMetrics = metrics.filter(m => m.statistical_significance < 0.001);

  return (
    <div className={clsx('space-y-6', className)}>
      {/* Business-Focused Overview */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-4 text-lg">Model Comparison Summary</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-700">{metrics.length}</div>
            <div className="text-blue-600 text-sm">Metrics Analyzed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">{highImpactMetrics.length}</div>
            <div className="text-blue-600 text-sm">High Impact</div>
            <div className="text-xs text-gray-500">🔴 Large differences</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{mediumImpactMetrics.length}</div>
            <div className="text-blue-600 text-sm">Medium Impact</div>
            <div className="text-xs text-gray-500">🟡 Moderate differences</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{highConfidenceMetrics.length}</div>
            <div className="text-blue-600 text-sm">High Confidence</div>
            <div className="text-xs text-gray-500">⭐⭐⭐ Very significant</div>
          </div>
        </div>

        {/* Quick Decision Guide */}
        {highImpactMetrics.length > 0 && (
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-blue-900 mb-2 flex items-center gap-2">
              <span className="text-lg">🎯</span>
              Quick Decision Guide
            </h4>
            <p className="text-sm text-blue-800">
              {highImpactMetrics.length} metric{highImpactMetrics.length > 1 ? 's show' : ' shows'} large, 
              practically significant differences between your models. These should be your primary 
              decision-making factors.
            </p>
          </div>
        )}
        
        {highImpactMetrics.length === 0 && significantMetrics.length > 0 && (
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-blue-900 mb-2 flex items-center gap-2">
              <span className="text-lg">⚖️</span>
              Balanced Comparison
            </h4>
            <p className="text-sm text-blue-800">
              While {significantMetrics.length} metric{significantMetrics.length > 1 ? 's show' : ' shows'} 
              statistically significant differences, the practical impact is moderate. Consider your 
              specific use case requirements when making decisions.
            </p>
          </div>
        )}

        {significantMetrics.length === 0 && (
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <h4 className="font-medium text-blue-900 mb-2 flex items-center gap-2">
              <span className="text-lg">🤝</span>
              Similar Values
            </h4>
            <p className="text-sm text-blue-800">
              No statistically significant differences detected. Both datasets show similar values 
              on the analyzed metrics. Consider other factors like cost, speed, or specific 
              capabilities for your decision.
            </p>
          </div>
        )}
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, index) => (
          <MetricCard key={`${metric.name}-${index}`} metric={metric} />
        ))}
      </div>

      {/* Business Insights */}
      {significantMetrics.length > 0 && (
        <div className="bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-200 rounded-lg p-6">
          <h3 className="font-semibold text-amber-900 mb-4 text-lg flex items-center gap-2">
            <span className="text-xl">💡</span>
            Key Business Insights
          </h3>
          
          <div className="space-y-3">
            {highImpactMetrics.map((metric, index) => {
              const metricName = metric.name.replace(/_/g, ' ').toLowerCase();
              const relativeDiff = metric.dataset_b_value !== 0 
                ? Math.abs((metric.dataset_a_value - metric.dataset_b_value) / metric.dataset_b_value * 100)
                : 0;
              const direction = metric.dataset_a_value > metric.dataset_b_value ? 'lower' : 'higher';
              
              return (
                <div key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-amber-200">
                  <span className="text-lg mt-0.5">🔴</span>
                  <div>
                    <h4 className="font-medium text-amber-900 capitalize">{metricName}</h4>
                    <p className="text-sm text-amber-800">
                      <strong>Dataset B</strong> shows {relativeDiff.toFixed(1)}% {direction} values than Dataset A. 
                      This is a major differentiator that should influence your model choice.
                    </p>
                  </div>
                </div>
              );
            })}
            
            {mediumImpactMetrics.map((metric, index) => {
              const metricName = metric.name.replace(/_/g, ' ').toLowerCase();
              const relativeDiff = metric.dataset_b_value !== 0 
                ? Math.abs((metric.dataset_a_value - metric.dataset_b_value) / metric.dataset_b_value * 100)
                : 0;
              const direction = metric.dataset_a_value > metric.dataset_b_value ? 'lower' : 'higher';
              
              return (
                <div key={`medium-${index}`} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-amber-200">
                  <span className="text-lg mt-0.5">🟡</span>
                  <div>
                    <h4 className="font-medium text-amber-900 capitalize">{metricName}</h4>
                    <p className="text-sm text-amber-800">
                      <strong>Dataset B</strong> shows {relativeDiff.toFixed(1)}% {direction} values than Dataset A. 
                      Consider if this difference matters for your specific use case.
                    </p>
                  </div>
                </div>
              );
            })}

            {significantMetrics.length > (highImpactMetrics.length + mediumImpactMetrics.length) && (
              <div className="flex items-start gap-3 p-3 bg-white rounded-lg border border-amber-200">
                <span className="text-lg mt-0.5">🟢</span>
                <div>
                  <h4 className="font-medium text-amber-900">Additional Differences</h4>
                  <p className="text-sm text-amber-800">
                    {significantMetrics.length - highImpactMetrics.length - mediumImpactMetrics.length} more 
                    metrics show small but statistically significant differences. These may be less 
                    critical for decision-making but worth noting.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};