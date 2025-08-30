import React, { useMemo, useState } from 'react';
import { clsx } from 'clsx';
import { ChevronUp, ChevronDown, Search, Filter } from 'lucide-react';
import { AlignedRow } from '../../types/comparison';

interface AlignedDataTableProps {
  rows: AlignedRow[];
  datasetNames: string[];
  className?: string;
}

type SortField = 'inputId' | 'inputText' | string;
type SortDirection = 'asc' | 'desc';
type ViewMode = 'text' | 'metrics';

export const AlignedDataTable: React.FC<AlignedDataTableProps> = ({
  rows,
  datasetNames,
  className
}) => {
  const [sortField, setSortField] = useState<SortField>('inputId');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDatasets, setSelectedDatasets] = useState<string[]>(datasetNames);
  const [viewMode, setViewMode] = useState<ViewMode>('text');
  const [showOnlyDifferences, setShowOnlyDifferences] = useState(false);

  // Process and filter data
  const processedRows = useMemo(() => {
    return rows.map(row => {
      const processed = { ...row };
      
      // Add computed metrics for each dataset
      for (const dsName of datasetNames) {
        const outputs = row.outputs[dsName] || [];
        if (Array.isArray(outputs)) {
          const lengths = outputs.map(o => o?.length || 0);
          const avgLength = lengths.reduce((a, b) => a + b, 0) / lengths.length || 0;
          
          processed.metadata = {
            ...processed.metadata,
            [dsName]: {
              ...processed.metadata[dsName],
              outputCount: outputs.length,
              avgLength: Math.round(avgLength),
              totalLength: lengths.reduce((a, b) => a + b, 0)
            }
          };
        }
      }
      
      return processed;
    });
  }, [rows, datasetNames]);

  const filteredAndSortedRows = useMemo(() => {
    let filtered = processedRows;

    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(row => 
        row.inputId.toLowerCase().includes(query) ||
        row.inputText.toLowerCase().includes(query) ||
        datasetNames.some(dsName => {
          const outputs = row.outputs[dsName];
          return Array.isArray(outputs) && outputs.some(output => 
            output?.toLowerCase().includes(query)
          );
        })
      );
    }

    // Apply difference filter
    if (showOnlyDifferences && datasetNames.length >= 2) {
      filtered = filtered.filter(row => {
        const outputs = datasetNames.map(dsName => row.outputs[dsName]);
        const lengths = outputs.map(output => 
          Array.isArray(output) ? output.reduce((sum, o) => sum + (o?.length || 0), 0) : 0
        );
        const minLength = Math.min(...lengths);
        const maxLength = Math.max(...lengths);
        return (maxLength - minLength) > 50; // Significant difference threshold
      });
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aVal: string | number = '';
      let bVal: string | number = '';

      if (sortField === 'inputId') {
        aVal = a.inputId;
        bVal = b.inputId;
      } else if (sortField === 'inputText') {
        aVal = a.inputText;
        bVal = b.inputText;
      } else if (sortField.endsWith('_length')) {
        const dsName = sortField.replace('_length', '');
        aVal = a.metadata[dsName]?.totalLength || 0;
        bVal = b.metadata[dsName]?.totalLength || 0;
      }

      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortDirection === 'asc' 
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal);
      } else {
        return sortDirection === 'asc' 
          ? (aVal as number) - (bVal as number)
          : (bVal as number) - (aVal as number);
      }
    });

    return filtered;
  }, [processedRows, searchQuery, showOnlyDifferences, sortField, sortDirection, datasetNames]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const getSortIcon = (field: SortField) => {
    if (sortField !== field) return null;
    return sortDirection === 'asc' 
      ? <ChevronUp className="w-4 h-4" />
      : <ChevronDown className="w-4 h-4" />;
  };

  const toggleDataset = (dsName: string) => {
    setSelectedDatasets(prev => 
      prev.includes(dsName)
        ? prev.filter(name => name !== dsName)
        : [...prev, dsName]
    );
  };

  return (
    <div className={clsx('space-y-4', className)}>
      {/* Controls */}
      <div className="flex flex-wrap gap-4 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-2">
          <Search className="w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search rows..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={viewMode}
            onChange={(e) => setViewMode(e.target.value as ViewMode)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            <option value="text">Text View</option>
            <option value="metrics">Metrics View</option>
          </select>
        </div>

        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={showOnlyDifferences}
            onChange={(e) => setShowOnlyDifferences(e.target.checked)}
            className="rounded"
          />
          Show only differences
        </label>
      </div>

      {/* Dataset Selection */}
      <div className="flex flex-wrap gap-2">
        {datasetNames.map(dsName => (
          <button
            key={dsName}
            onClick={() => toggleDataset(dsName)}
            className={clsx(
              'px-3 py-1 rounded-md text-sm font-medium transition-colors',
              selectedDatasets.includes(dsName)
                ? 'bg-primary-100 text-primary-700 border border-primary-200'
                : 'bg-gray-100 text-gray-600 border border-gray-200'
            )}
          >
            {dsName}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="overflow-auto max-h-96 border rounded-lg">
        <table className="w-full text-sm">
          <thead className="sticky top-0 bg-white border-b">
            <tr>
              <th 
                className="px-4 py-3 text-left cursor-pointer hover:bg-gray-50"
                onClick={() => handleSort('inputId')}
              >
                <div className="flex items-center gap-2">
                  Input ID
                  {getSortIcon('inputId')}
                </div>
              </th>
              <th 
                className="px-4 py-3 text-left cursor-pointer hover:bg-gray-50"
                onClick={() => handleSort('inputText')}
              >
                <div className="flex items-center gap-2">
                  Input Text
                  {getSortIcon('inputText')}
                </div>
              </th>
              {selectedDatasets.map(dsName => (
                <th 
                  key={dsName}
                  className="px-4 py-3 text-left cursor-pointer hover:bg-gray-50"
                  onClick={() => handleSort(`${dsName}_length`)}
                >
                  <div className="flex items-center gap-2">
                    {dsName}
                    {getSortIcon(`${dsName}_length`)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedRows.map((row, index) => (
              <tr key={row.inputId} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-4 py-3 text-xs font-mono">
                  {row.inputId}
                </td>
                <td className="px-4 py-3">
                  <div className="max-w-xs truncate">
                    {row.inputText}
                  </div>
                </td>
                {selectedDatasets.map(dsName => (
                  <td key={dsName} className="px-4 py-3">
                    {viewMode === 'text' ? (
                      <div className="max-w-xs">
                        {Array.isArray(row.outputs[dsName]) && row.outputs[dsName]!.length > 0 ? (
                          <div className="truncate">
                            {row.outputs[dsName]![0]}
                            {row.outputs[dsName]!.length > 1 && (
                              <span className="text-gray-400 text-xs ml-2">
                                +{row.outputs[dsName]!.length - 1} more
                              </span>
                            )}
                          </div>
                        ) : (
                          <span className="text-gray-400 italic">No output</span>
                        )}
                      </div>
                    ) : (
                      <div className="space-y-1 text-xs">
                        <div>Count: {row.metadata[dsName]?.outputCount || 0}</div>
                        <div>Avg Length: {row.metadata[dsName]?.avgLength || 0}</div>
                        <div>Total: {row.metadata[dsName]?.totalLength || 0}</div>
                      </div>
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <div className="text-sm text-gray-600">
        Showing {filteredAndSortedRows.length} of {rows.length} rows
      </div>
    </div>
  );
};