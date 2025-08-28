import React, { useMemo } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  ErrorBar,
  LineChart,
  Line,
  Area,
  AreaChart
} from 'recharts';
import { clsx } from 'clsx';
import { StatisticalMetric } from '../../types/comparison';

interface ComparisonChartsProps {
  metrics: StatisticalMetric[];
  className?: string;
}

interface ChartData {
  name: string;
  datasetA: number;
  datasetB: number;
  difference: number;
  pValue: number;
  effectSize: number;
  ciLower: number;
  ciUpper: number;
  significant: boolean;
}

export const ComparisonCharts: React.FC<ComparisonChartsProps> = ({ 
  metrics, 
  className 
}) => {
  const chartData = useMemo((): ChartData[] => {
    return metrics.map(metric => ({
      name: metric.name.replace(/_/g, ' '),
      datasetA: metric.dataset_a_value,
      datasetB: metric.dataset_b_value,
      difference: metric.dataset_a_value - metric.dataset_b_value,
      pValue: metric.statistical_significance,
      effectSize: metric.effect_size,
      ciLower: metric.confidence_interval_lower,
      ciUpper: metric.confidence_interval_upper,
      significant: metric.statistical_significance < 0.05
    }));
  }, [metrics]);

  const significantData = chartData.filter(d => d.significant);
  const effectSizeData = chartData.map(d => ({
    name: d.name,
    effectSize: Math.abs(d.effectSize),
    pValue: -Math.log10(d.pValue), // Convert to -log10 scale for better visualization
    significant: d.significant
  }));

  if (metrics.length === 0) {
    return (
      <div className={clsx('text-center py-8 text-gray-500', className)}>
        No metrics data available for visualization
      </div>
    );
  }

  return (
    <div className={clsx('space-y-8', className)}>
      {/* Side-by-side Comparison */}
      <div className="bg-white p-6 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold mb-4">Metric Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={12}
            />
            <YAxis />
            <Tooltip 
              formatter={(value: number, name: string) => [
                value.toFixed(3), 
                name === 'datasetA' ? 'Dataset A' : 'Dataset B'
              ]}
            />
            <Legend />
            <Bar dataKey="datasetA" fill="#3b82f6" name="Dataset A" />
            <Bar dataKey="datasetB" fill="#10b981" name="Dataset B" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Effect Size vs P-Value Scatter */}
      <div className="bg-white p-6 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold mb-4">Effect Size vs Statistical Significance</h3>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              type="number" 
              dataKey="effectSize"
              name="Effect Size"
              domain={[0, 'dataMax']}
              label={{ value: 'Effect Size (|d|)', position: 'insideBottom', offset: -10 }}
            />
            <YAxis 
              type="number" 
              dataKey="pValue"
              name="-log10(p-value)"
              domain={[0, 'dataMax']}
              label={{ value: '-log10(p-value)', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip 
              formatter={(value: number, name: string, props: any) => {
                if (name === 'effectSize') {
                  return [value.toFixed(3), 'Effect Size'];
                }
                if (name === 'pValue') {
                  return [value.toFixed(2), '-log10(p-value)'];
                }
                return [value, name];
              }}
              labelFormatter={(label) => `Metric: ${label}`}
            />
            <Scatter 
              name="Significant" 
              data={effectSizeData.filter(d => d.significant)} 
              fill="#ef4444" 
            />
            <Scatter 
              name="Not Significant" 
              data={effectSizeData.filter(d => !d.significant)} 
              fill="#9ca3af" 
            />
            {/* Significance threshold line */}
            <Line 
              type="monotone" 
              dataKey={() => 1.301} // -log10(0.05) ≈ 1.301
              stroke="#fbbf24" 
              strokeDasharray="5 5"
              name="p=0.05 threshold"
            />
          </ScatterChart>
        </ResponsiveContainer>
        <div className="mt-2 text-sm text-gray-600">
          Points above the dashed line are statistically significant (p &lt; 0.05)
        </div>
      </div>

      {/* Difference Chart with Confidence Intervals */}
      {significantData.length > 0 && (
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Significant Differences (95% CI)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={significantData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45}
                textAnchor="end"
                height={80}
                fontSize={12}
              />
              <YAxis />
              <Tooltip 
                formatter={(value: number) => [value.toFixed(3), 'Difference (A - B)']}
              />
              <Bar dataKey="difference" fill="#8b5cf6">
                <ErrorBar 
                  dataKey="ciLower" 
                  width={4} 
                  stroke="#6d28d9"
                />
                <ErrorBar 
                  dataKey="ciUpper" 
                  width={4} 
                  stroke="#6d28d9"
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-2 text-sm text-gray-600">
            Error bars represent 95% confidence intervals
          </div>
        </div>
      )}

      {/* Summary Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h4 className="font-semibold text-blue-900">Average Effect Size</h4>
          <div className="text-2xl font-bold text-blue-700">
            {chartData.length > 0 
              ? (chartData.reduce((sum, d) => sum + Math.abs(d.effectSize), 0) / chartData.length).toFixed(2)
              : '0.00'
            }
          </div>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <h4 className="font-semibold text-green-900">Significant Metrics</h4>
          <div className="text-2xl font-bold text-green-700">
            {significantData.length}/{chartData.length}
          </div>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <h4 className="font-semibold text-purple-900">Large Effects</h4>
          <div className="text-2xl font-bold text-purple-700">
            {chartData.filter(d => Math.abs(d.effectSize) >= 0.5).length}
          </div>
        </div>
      </div>
    </div>
  );
};