import React from 'react';
import { clsx } from 'clsx';
import { Search, Filter, SortAsc, SortDesc, Eye, EyeOff } from 'lucide-react';

interface FilterControlsProps {
  searchQuery: string;
  onSearchChange: (query: string) => void;
  sortField: string;
  sortDirection: 'asc' | 'desc';
  onSortChange: (field: string, direction: 'asc' | 'desc') => void;
  showDifferencesOnly: boolean;
  onShowDifferencesToggle: (show: boolean) => void;
  availableFields: string[];
  selectedDatasets: string[];
  availableDatasets: string[];
  onDatasetToggle: (dataset: string) => void;
  significanceThreshold: number;
  onSignificanceThresholdChange: (threshold: number) => void;
  className?: string;
}

export const FilterControls: React.FC<FilterControlsProps> = ({
  searchQuery,
  onSearchChange,
  sortField,
  sortDirection,
  onSortChange,
  showDifferencesOnly,
  onShowDifferencesToggle,
  availableFields,
  selectedDatasets,
  availableDatasets,
  onDatasetToggle,
  significanceThreshold,
  onSignificanceThresholdChange,
  className
}) => {
  const significanceOptions = [
    { value: 0.1, label: '0.1 (90% confidence)' },
    { value: 0.05, label: '0.05 (95% confidence)' },
    { value: 0.01, label: '0.01 (99% confidence)' },
    { value: 0.001, label: '0.001 (99.9% confidence)' }
  ];

  return (
    <div className={clsx('space-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200', className)}>
      {/* Search and Basic Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex items-center gap-2 min-w-0 flex-1">
          <Search className="w-4 h-4 text-gray-400 flex-shrink-0" />
          <input
            type="text"
            placeholder="Search prompts and completions..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="flex-1 px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={sortField}
            onChange={(e) => onSortChange(e.target.value, sortDirection)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="">Sort by...</option>
            {availableFields.map(field => (
              <option key={field} value={field}>
                {field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </option>
            ))}
          </select>
          
          <button
            onClick={() => onSortChange(sortField, sortDirection === 'asc' ? 'desc' : 'asc')}
            disabled={!sortField}
            className={clsx(
              'p-1 rounded border transition-colors',
              sortField 
                ? 'border-gray-300 text-gray-700 hover:bg-gray-100' 
                : 'border-gray-200 text-gray-400 cursor-not-allowed'
            )}
          >
            {sortDirection === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Advanced Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={showDifferencesOnly}
            onChange={(e) => onShowDifferencesToggle(e.target.checked)}
            className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span className="text-gray-700">Show significant differences only</span>
        </label>

        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-600">Significance level:</span>
          <select
            value={significanceThreshold}
            onChange={(e) => onSignificanceThresholdChange(parseFloat(e.target.value))}
            className="px-2 py-1 border border-gray-300 rounded text-xs focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            {significanceOptions.map(option => (
              <option key={option.value} value={option.value}>
                p &lt; {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Dataset Selection */}
      {availableDatasets.length > 0 && (
        <div>
          <div className="text-sm text-gray-600 mb-2">Datasets to compare:</div>
          <div className="flex flex-wrap gap-2">
            {availableDatasets.map(dataset => (
              <button
                key={dataset}
                onClick={() => onDatasetToggle(dataset)}
                className={clsx(
                  'inline-flex items-center gap-1 px-3 py-1 rounded-md text-sm font-medium transition-colors border',
                  selectedDatasets.includes(dataset)
                    ? 'bg-primary-100 text-primary-700 border-primary-200'
                    : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
                )}
              >
                {selectedDatasets.includes(dataset) ? (
                  <Eye className="w-3 h-3" />
                ) : (
                  <EyeOff className="w-3 h-3" />
                )}
                {dataset}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Active Filters Summary */}
      {(searchQuery || sortField || showDifferencesOnly || selectedDatasets.length < availableDatasets.length) && (
        <div className="pt-2 border-t border-gray-200">
          <div className="text-xs text-gray-600">
            Active filters: 
            {searchQuery && <span className="ml-1 px-1 bg-blue-100 text-blue-700 rounded">Search: "{searchQuery}"</span>}
            {sortField && <span className="ml-1 px-1 bg-green-100 text-green-700 rounded">Sort: {sortField} ({sortDirection})</span>}
            {showDifferencesOnly && <span className="ml-1 px-1 bg-yellow-100 text-yellow-700 rounded">Differences only</span>}
            {selectedDatasets.length < availableDatasets.length && (
              <span className="ml-1 px-1 bg-purple-100 text-purple-700 rounded">
                {selectedDatasets.length}/{availableDatasets.length} datasets
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};