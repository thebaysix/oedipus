import { StatisticalMetric, AlignmentResult, AlignedRow } from '../types/comparison';

export interface GeneratedInsight {
  type: 'performance' | 'quality' | 'consistency' | 'coverage' | 'recommendation' | 'outlier';
  title: string;
  description: string;
  impact: 'high' | 'medium' | 'low';
  confidence: number; // 0-1
  metrics: string[];
  data?: any;
}

export class InsightGenerator {
  private metrics: StatisticalMetric[];
  private alignment: AlignmentResult | null;
  private significanceThreshold: number;

  constructor(metrics: StatisticalMetric[], alignment: AlignmentResult | null, significanceThreshold = 0.05) {
    this.metrics = metrics;
    this.alignment = alignment;
    this.significanceThreshold = significanceThreshold;
  }

  generateInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];

    insights.push(...this.generatePerformanceInsights());
    insights.push(...this.generateCoverageInsights());
    insights.push(...this.generateQualityInsights());
    insights.push(...this.generateConsistencyInsights());
    insights.push(...this.generateOutlierInsights());
    insights.push(...this.generateRecommendationInsights());

    return insights.sort((a, b) => {
      // Sort by impact first, then confidence
      const impactOrder = { high: 3, medium: 2, low: 1 };
      const impactDiff = impactOrder[b.impact] - impactOrder[a.impact];
      if (impactDiff !== 0) return impactDiff;
      return b.confidence - a.confidence;
    });
  }

  private generatePerformanceInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];
    const significantMetrics = this.metrics.filter(m => m.statistical_significance < this.significanceThreshold);
    const largeEffectMetrics = significantMetrics.filter(m => Math.abs(m.effect_size) >= 0.8);

    if (largeEffectMetrics.length > 0) {
      const dominantDataset = this.getDominantDataset(largeEffectMetrics);
      insights.push({
        type: 'performance',
        title: `Clear Performance Leader: ${dominantDataset.name}`,
        description: `${dominantDataset.name} consistently outperforms in ${largeEffectMetrics.length} key metric${largeEffectMetrics.length > 1 ? 's' : ''} with large effect sizes (avg: ${dominantDataset.avgEffect.toFixed(2)}).`,
        impact: 'high',
        confidence: this.calculateConfidence(largeEffectMetrics),
        metrics: largeEffectMetrics.map(m => m.name)
      });
    }

    if (significantMetrics.length > 0 && largeEffectMetrics.length === 0) {
      insights.push({
        type: 'performance',
        title: 'Moderate Performance Differences',
        description: `${significantMetrics.length} metrics show significant but small-to-medium effect sizes. Consider practical significance alongside statistical significance.`,
        impact: 'medium',
        confidence: this.calculateConfidence(significantMetrics),
        metrics: significantMetrics.map(m => m.name)
      });
    }

    return insights;
  }

  private generateCoverageInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];
    
    if (!this.alignment?.coverageStats) return insights;

    const { coveragePercentage, totalInputs, matchedInputs } = this.alignment.coverageStats;

    if (coveragePercentage < 70) {
      insights.push({
        type: 'coverage',
        title: 'Low Data Alignment Coverage',
        description: `Only ${coveragePercentage.toFixed(1)}% of inputs have matching outputs (${matchedInputs}/${totalInputs}). This reduces the reliability of comparative analysis.`,
        impact: coveragePercentage < 50 ? 'high' : 'medium',
        confidence: 0.9,
        metrics: ['alignment_coverage'],
        data: { coveragePercentage, totalInputs, matchedInputs }
      });
    } else if (coveragePercentage > 95) {
      insights.push({
        type: 'coverage',
        title: 'Excellent Data Alignment',
        description: `High coverage achieved (${coveragePercentage.toFixed(1)}%). Reliable comparative analysis is possible with ${matchedInputs} aligned data points.`,
        impact: 'low',
        confidence: 0.8,
        metrics: ['alignment_coverage'],
        data: { coveragePercentage, totalInputs, matchedInputs }
      });
    }

    return insights;
  }

  private generateQualityInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];
    
    // Analyze entropy patterns
    const entropyMetrics = this.metrics.filter(m => m.name.toLowerCase().includes('entropy'));
    if (entropyMetrics.length > 0) {
      const avgEntropyDiff = entropyMetrics.reduce((sum, m) => 
        sum + Math.abs(m.dataset_a_value - m.dataset_b_value), 0) / entropyMetrics.length;
      
      if (avgEntropyDiff > 1.0) {
        insights.push({
          type: 'quality',
          title: 'Significant Output Diversity Differences',
          description: `Average entropy difference of ${avgEntropyDiff.toFixed(2)} suggests models produce outputs with different levels of diversity and creativity.`,
          impact: 'medium',
          confidence: 0.7,
          metrics: entropyMetrics.map(m => m.name)
        });
      }
    }

    // Analyze token/length patterns
    const lengthMetrics = this.metrics.filter(m => 
      m.name.toLowerCase().includes('length') || m.name.toLowerCase().includes('token')
    );
    
    if (lengthMetrics.length > 0) {
      const significantLengthDiffs = lengthMetrics.filter(m => m.statistical_significance < this.significanceThreshold);
      if (significantLengthDiffs.length > 0) {
        const avgLengthEffect = significantLengthDiffs.reduce((sum, m) => sum + Math.abs(m.effect_size), 0) / significantLengthDiffs.length;
        insights.push({
          type: 'quality',
          title: 'Consistent Output Length Patterns',
          description: `Significant differences in output length detected (avg effect: ${avgLengthEffect.toFixed(2)}). Consider if length variations align with your requirements.`,
          impact: avgLengthEffect > 0.5 ? 'medium' : 'low',
          confidence: this.calculateConfidence(significantLengthDiffs),
          metrics: significantLengthDiffs.map(m => m.name)
        });
      }
    }

    return insights;
  }

  private generateConsistencyInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];
    
    if (!this.alignment?.alignedRows) return insights;

    // Analyze output consistency across inputs
    const consistencyAnalysis = this.analyzeOutputConsistency();
    
    if (consistencyAnalysis.highVariabilityInputs > 0) {
      insights.push({
        type: 'consistency',
        title: 'Inconsistent Performance on Some Inputs',
        description: `${consistencyAnalysis.highVariabilityInputs} inputs show high variability in output quality between models. These may be challenging edge cases.`,
        impact: 'medium',
        confidence: 0.6,
        metrics: ['output_consistency'],
        data: consistencyAnalysis
      });
    }

    return insights;
  }

  private generateOutlierInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];
    
    if (!this.alignment?.alignedRows) return insights;

    const outliers = this.detectOutliers();
    
    if (outliers.length > 0) {
      insights.push({
        type: 'outlier',
        title: 'Outlier Inputs Detected',
        description: `${outliers.length} inputs show unusual patterns that may warrant individual investigation. These represent potential edge cases or data quality issues.`,
        impact: 'low',
        confidence: 0.5,
        metrics: ['outlier_detection'],
        data: { outliers: outliers.slice(0, 5) } // Include top 5 outliers
      });
    }

    return insights;
  }

  private generateRecommendationInsights(): GeneratedInsight[] {
    const insights: GeneratedInsight[] = [];
    
    const significantMetrics = this.metrics.filter(m => m.statistical_significance < this.significanceThreshold);
    const largeEffectMetrics = significantMetrics.filter(m => Math.abs(m.effect_size) >= 0.8);
    const coverageOk = this.alignment?.coverageStats.coveragePercentage > 80;

    if (largeEffectMetrics.length > 0 && coverageOk) {
      insights.push({
        type: 'recommendation',
        title: 'Sufficient Evidence for Decision Making',
        description: 'High data coverage and clear performance differences detected. You have sufficient statistical evidence to make an informed model selection decision.',
        impact: 'high',
        confidence: 0.85,
        metrics: []
      });
    } else if (significantMetrics.length === 0) {
      insights.push({
        type: 'recommendation',
        title: 'Consider Additional Metrics or Data',
        description: 'No statistically significant differences detected. Consider collecting more data, testing different metrics, or evaluating other model aspects.',
        impact: 'medium',
        confidence: 0.7,
        metrics: []
      });
    } else if (!coverageOk) {
      insights.push({
        type: 'recommendation',
        title: 'Improve Data Alignment',
        description: 'Low data coverage limits analysis reliability. Ensure consistent input identifiers across datasets or collect additional aligned samples.',
        impact: 'medium',
        confidence: 0.8,
        metrics: ['alignment_coverage']
      });
    }

    return insights;
  }

  private getDominantDataset(metrics: StatisticalMetric[]): { name: string; avgEffect: number } {
    const aWins = metrics.filter(m => m.dataset_a_value > m.dataset_b_value).length;
    const bWins = metrics.length - aWins;
    
    const avgEffectA = metrics.reduce((sum, m) => sum + (m.dataset_a_value > m.dataset_b_value ? m.effect_size : -m.effect_size), 0) / metrics.length;
    
    return {
      name: aWins > bWins ? 'Dataset A' : 'Dataset B',
      avgEffect: Math.abs(avgEffectA)
    };
  }

  private calculateConfidence(metrics: StatisticalMetric[]): number {
    if (metrics.length === 0) return 0;
    
    const avgPValue = metrics.reduce((sum, m) => sum + m.statistical_significance, 0) / metrics.length;
    const avgEffectSize = metrics.reduce((sum, m) => sum + Math.abs(m.effect_size), 0) / metrics.length;
    
    // Confidence based on p-values and effect sizes
    let confidence = 0.5;
    if (avgPValue < 0.001) confidence += 0.3;
    else if (avgPValue < 0.01) confidence += 0.2;
    else if (avgPValue < 0.05) confidence += 0.1;
    
    if (avgEffectSize > 0.8) confidence += 0.2;
    else if (avgEffectSize > 0.5) confidence += 0.15;
    else if (avgEffectSize > 0.2) confidence += 0.1;
    
    return Math.min(confidence, 1.0);
  }

  private analyzeOutputConsistency(): { highVariabilityInputs: number; avgConsistency: number } {
    if (!this.alignment?.alignedRows) return { highVariabilityInputs: 0, avgConsistency: 1 };

    let highVariabilityCount = 0;
    let totalConsistency = 0;

    for (const row of this.alignment.alignedRows) {
      const outputs = Object.values(row.outputs).filter(o => o !== null) as string[][];
      if (outputs.length < 2) continue;

      // Simple consistency measure based on output length variation
      const lengths = outputs.map(outputArray => outputArray.reduce((sum, text) => sum + text.length, 0));
      const avgLength = lengths.reduce((sum, len) => sum + len, 0) / lengths.length;
      const variance = lengths.reduce((sum, len) => sum + Math.pow(len - avgLength, 2), 0) / lengths.length;
      const cv = avgLength > 0 ? Math.sqrt(variance) / avgLength : 0; // coefficient of variation

      if (cv > 0.5) highVariabilityCount++; // High variability threshold
      totalConsistency += (1 - Math.min(cv, 1)); // Consistency score
    }

    return {
      highVariabilityInputs: highVariabilityCount,
      avgConsistency: this.alignment.alignedRows.length > 0 ? totalConsistency / this.alignment.alignedRows.length : 1
    };
  }

  private detectOutliers(): AlignedRow[] {
    if (!this.alignment?.alignedRows) return [];

    const outliers: AlignedRow[] = [];
    
    // Simple outlier detection based on output length
    const allLengths = this.alignment.alignedRows.map(row => {
      const outputs = Object.values(row.outputs).filter(o => o !== null) as string[][];
      return outputs.reduce((sum, outputArray) => sum + outputArray.reduce((s, text) => s + text.length, 0), 0);
    });

    if (allLengths.length === 0) return [];

    const mean = allLengths.reduce((sum, len) => sum + len, 0) / allLengths.length;
    const std = Math.sqrt(allLengths.reduce((sum, len) => sum + Math.pow(len - mean, 2), 0) / allLengths.length);
    
    const threshold = 2 * std; // 2 standard deviations

    this.alignment.alignedRows.forEach((row, index) => {
      if (Math.abs(allLengths[index] - mean) > threshold) {
        outliers.push(row);
      }
    });

    return outliers.slice(0, 10); // Return top 10 outliers
  }
}