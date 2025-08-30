// Statistical test utilities for client-side calculations

export interface TTestResult {
  statistic: number;
  pValue: number;
  degreesOfFreedom: number;
  effectSize: number;
  confidenceInterval: [number, number];
}

export interface DescriptiveStats {
  mean: number;
  std: number;
  variance: number;
  min: number;
  max: number;
  count: number;
  median: number;
  q25: number;
  q75: number;
}

export const calculateDescriptiveStats = (values: number[]): DescriptiveStats => {
  if (values.length === 0) {
    return {
      mean: 0, std: 0, variance: 0, min: 0, max: 0,
      count: 0, median: 0, q25: 0, q75: 0
    };
  }

  const sorted = [...values].sort((a, b) => a - b);
  const n = values.length;
  const mean = values.reduce((sum, val) => sum + val, 0) / n;
  const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / (n - 1);
  const std = Math.sqrt(variance);

  const getPercentile = (p: number) => {
    const index = (n - 1) * p;
    const lower = Math.floor(index);
    const upper = Math.ceil(index);
    const weight = index - lower;
    return sorted[lower] * (1 - weight) + sorted[upper] * weight;
  };

  return {
    mean,
    std,
    variance,
    min: Math.min(...values),
    max: Math.max(...values),
    count: n,
    median: getPercentile(0.5),
    q25: getPercentile(0.25),
    q75: getPercentile(0.75)
  };
};

export const calculateCohenD = (mean1: number, mean2: number, std1: number, std2: number, n1: number, n2: number): number => {
  const pooledStd = Math.sqrt(((n1 - 1) * std1 * std1 + (n2 - 1) * std2 * std2) / (n1 + n2 - 2));
  return (mean1 - mean2) / pooledStd;
};

export const calculateWelchTTest = (sample1: number[], sample2: number[]): TTestResult => {
  const stats1 = calculateDescriptiveStats(sample1);
  const stats2 = calculateDescriptiveStats(sample2);
  
  const n1 = sample1.length;
  const n2 = sample2.length;
  
  if (n1 < 2 || n2 < 2) {
    throw new Error('Each sample must have at least 2 observations');
  }

  const meanDiff = stats1.mean - stats2.mean;
  const se = Math.sqrt(stats1.variance / n1 + stats2.variance / n2);
  const statistic = meanDiff / se;
  
  // Welch's degrees of freedom
  const df = Math.pow(stats1.variance / n1 + stats2.variance / n2, 2) /
    (Math.pow(stats1.variance / n1, 2) / (n1 - 1) + Math.pow(stats2.variance / n2, 2) / (n2 - 1));
  
  // Approximate p-value using t-distribution (simplified)
  const pValue = approximateTTestPValue(Math.abs(statistic), df);
  
  // Effect size (Cohen's d)
  const effectSize = calculateCohenD(stats1.mean, stats2.mean, stats1.std, stats2.std, n1, n2);
  
  // Confidence interval (95%)
  const tCritical = 1.96; // Approximate for large df
  const margin = tCritical * se;
  const confidenceInterval: [number, number] = [meanDiff - margin, meanDiff + margin];

  return {
    statistic,
    pValue,
    degreesOfFreedom: df,
    effectSize,
    confidenceInterval
  };
};

// Simplified t-test p-value approximation
const approximateTTestPValue = (tStat: number, df: number): number => {
  // Very rough approximation for demonstration
  // In production, you'd use a proper t-distribution implementation
  const zApprox = tStat;
  
  // Standard normal approximation (gets better as df increases)
  if (zApprox < 0.674) return 1.0;
  if (zApprox < 1.282) return 0.2;
  if (zApprox < 1.645) return 0.1;
  if (zApprox < 1.960) return 0.05;
  if (zApprox < 2.326) return 0.02;
  if (zApprox < 2.576) return 0.01;
  if (zApprox < 3.090) return 0.002;
  if (zApprox < 3.291) return 0.001;
  return 0.0001;
};

export const interpretEffectSize = (effectSize: number): string => {
  const absEffect = Math.abs(effectSize);
  if (absEffect < 0.2) return 'negligible';
  if (absEffect < 0.5) return 'small';
  if (absEffect < 0.8) return 'medium';
  return 'large';
};

export const interpretPValue = (pValue: number, alpha: number = 0.05): string => {
  if (pValue < 0.001) return 'highly significant';
  if (pValue < 0.01) return 'very significant';
  if (pValue < alpha) return 'significant';
  if (pValue < alpha * 2) return 'marginally significant';
  return 'not significant';
};

export const calculatePowerAnalysis = (effectSize: number, n1: number, n2: number, alpha: number = 0.05): number => {
  // Simplified power calculation
  const nHarmonic = 2 / (1/n1 + 1/n2);
  const delta = Math.abs(effectSize) * Math.sqrt(nHarmonic / 2);
  
  // Rough approximation - in practice you'd use proper power analysis libraries
  if (delta < 1.64) return 0.5; // 50% power
  if (delta < 2.49) return 0.8; // 80% power
  if (delta < 2.94) return 0.9; // 90% power
  return 0.95; // 95% power
};