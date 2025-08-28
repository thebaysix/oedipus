import React, { useState } from 'react';
import { clsx } from 'clsx';
import { Download, FileText, Share2, Copy, ExternalLink } from 'lucide-react';
import { StatisticalMetric, Comparison, AlignmentResult } from '../../types/comparison';

interface ReportGeneratorProps {
  comparison: Comparison;
  metrics: StatisticalMetric[];
  alignment: AlignmentResult | null;
  className?: string;
}

type ExportFormat = 'json' | 'csv' | 'pdf' | 'summary';

interface ExportConfig {
  format: ExportFormat;
  includeRawData: boolean;
  includeStatistics: boolean;
  includeInsights: boolean;
  includeVisualizations: boolean;
}

export const ReportGenerator: React.FC<ReportGeneratorProps> = ({
  comparison,
  metrics,
  alignment,
  className
}) => {
  const [exportConfig, setExportConfig] = useState<ExportConfig>({
    format: 'summary',
    includeRawData: false,
    includeStatistics: true,
    includeInsights: true,
    includeVisualizations: false
  });
  const [isExporting, setIsExporting] = useState(false);
  const [shareUrl, setShareUrl] = useState<string>('');
  const [showShareDialog, setShowShareDialog] = useState(false);

  const exportOptions: Array<{ value: ExportFormat; label: string; description: string }> = [
    { value: 'summary', label: 'Executive Summary', description: 'Key findings and recommendations (PDF)' },
    { value: 'json', label: 'JSON Data', description: 'Complete dataset for programmatic access' },
    { value: 'csv', label: 'CSV Export', description: 'Aligned data table for spreadsheet analysis' },
    { value: 'pdf', label: 'Full Report', description: 'Comprehensive analysis report (PDF)' }
  ];

  const generateReport = async () => {
    setIsExporting(true);
    
    try {
      // This would call the backend API to generate the report
      const reportData = {
        comparison_id: comparison.id,
        format: exportConfig.format,
        include_raw_data: exportConfig.includeRawData,
        include_statistics: exportConfig.includeStatistics,
        include_insights: exportConfig.includeInsights,
        include_visualizations: exportConfig.includeVisualizations
      };

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // In a real implementation, this would download the file
      const fileName = `oedipus-comparison-${comparison.id}-${exportConfig.format}`;
      console.log('Generating report:', fileName, reportData);
      
      // Create a mock download
      const mockData = JSON.stringify(reportData, null, 2);
      const blob = new Blob([mockData], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${fileName}.json`;
      a.click();
      URL.revokeObjectURL(url);

    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const shareComparison = async () => {
    try {
      // Generate shareable link
      const shareToken = `share_${comparison.id}_${Date.now()}`;
      const url = `${window.location.origin}/shared/${shareToken}`;
      setShareUrl(url);
      setShowShareDialog(true);
    } catch (error) {
      console.error('Share failed:', error);
    }
  };

  const copyShareUrl = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      // Could show a toast notification here
    } catch (error) {
      console.error('Copy failed:', error);
    }
  };

  const getEstimatedSize = () => {
    const baseSize = 50; // KB
    let size = baseSize;
    
    if (exportConfig.includeRawData && alignment) {
      size += alignment.alignedRows.length * 2; // ~2KB per row
    }
    if (exportConfig.includeStatistics) {
      size += metrics.length * 0.5; // ~0.5KB per metric
    }
    if (exportConfig.includeVisualizations) {
      size += 500; // ~500KB for charts
    }
    
    return size > 1024 ? `${(size/1024).toFixed(1)}MB` : `${Math.round(size)}KB`;
  };

  return (
    <div className={clsx('space-y-6', className)}>
      {/* Export Configuration */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <FileText className="w-5 h-5" />
          Export Configuration
        </h3>

        {/* Format Selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Export Format</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {exportOptions.map(option => (
              <div
                key={option.value}
                className={clsx(
                  'p-3 border rounded-lg cursor-pointer transition-colors',
                  exportConfig.format === option.value
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                )}
                onClick={() => setExportConfig(prev => ({ ...prev, format: option.value }))}
              >
                <div className="font-medium text-gray-900">{option.label}</div>
                <div className="text-sm text-gray-600">{option.description}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Content Options */}
        <div className="space-y-3">
          <label className="block text-sm font-medium text-gray-700">Include in Export</label>
          
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={exportConfig.includeRawData}
              onChange={(e) => setExportConfig(prev => ({ ...prev, includeRawData: e.target.checked }))}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="text-sm text-gray-700">Raw aligned data</span>
          </label>
          
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={exportConfig.includeStatistics}
              onChange={(e) => setExportConfig(prev => ({ ...prev, includeStatistics: e.target.checked }))}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="text-sm text-gray-700">Statistical analysis</span>
          </label>
          
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={exportConfig.includeInsights}
              onChange={(e) => setExportConfig(prev => ({ ...prev, includeInsights: e.target.checked }))}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="text-sm text-gray-700">Auto-generated insights</span>
          </label>
          
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={exportConfig.includeVisualizations}
              onChange={(e) => setExportConfig(prev => ({ ...prev, includeVisualizations: e.target.checked }))}
              disabled={exportConfig.format === 'json' || exportConfig.format === 'csv'}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500 disabled:opacity-50"
            />
            <span className="text-sm text-gray-700">Charts and visualizations</span>
            {(exportConfig.format === 'json' || exportConfig.format === 'csv') && (
              <span className="text-xs text-gray-500">(not available for this format)</span>
            )}
          </label>
        </div>

        {/* Size Estimate */}
        <div className="mt-4 text-sm text-gray-600">
          Estimated size: {getEstimatedSize()}
        </div>
      </div>

      {/* Export Actions */}
      <div className="flex flex-wrap gap-4">
        <button
          onClick={generateReport}
          disabled={isExporting}
          className={clsx(
            'flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors',
            'bg-primary-500 text-white hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed'
          )}
        >
          <Download className="w-4 h-4" />
          {isExporting ? 'Generating...' : 'Download Report'}
        </button>

        <button
          onClick={shareComparison}
          className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          <Share2 className="w-4 h-4" />
          Share Analysis
        </button>
      </div>

      {/* Share Dialog */}
      {showShareDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h4 className="text-lg font-semibold mb-4">Share Comparison</h4>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Shareable Link
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={shareUrl}
                  readOnly
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm bg-gray-50"
                />
                <button
                  onClick={copyShareUrl}
                  className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                >
                  <Copy className="w-4 h-4" />
                </button>
                <button
                  onClick={() => window.open(shareUrl, '_blank')}
                  className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="text-sm text-gray-600 mb-4">
              This link provides read-only access to your comparison results. 
              No sensitive data is exposed.
            </div>
            
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowShareDialog(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h4 className="font-medium text-gray-900 mb-3">Quick Actions</h4>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => {
              setExportConfig({
                format: 'summary',
                includeRawData: false,
                includeStatistics: true,
                includeInsights: true,
                includeVisualizations: false
              });
              generateReport();
            }}
            className="text-sm px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
          >
            Quick Summary
          </button>
          
          <button
            onClick={() => {
              setExportConfig({
                format: 'csv',
                includeRawData: true,
                includeStatistics: true,
                includeInsights: false,
                includeVisualizations: false
              });
              generateReport();
            }}
            className="text-sm px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
          >
            Data Export
          </button>
          
          <button
            onClick={() => {
              setExportConfig({
                format: 'pdf',
                includeRawData: false,
                includeStatistics: true,
                includeInsights: true,
                includeVisualizations: true
              });
              generateReport();
            }}
            className="text-sm px-3 py-1 bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition-colors"
          >
            Full Report
          </button>
        </div>
      </div>
    </div>
  );
};