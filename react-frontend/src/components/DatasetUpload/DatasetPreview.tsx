import React from 'react';
import { clsx } from 'clsx';
import { CheckCircle, XCircle, Clock, Trash2, Database, FileOutput } from 'lucide-react';
import { UploadedFile } from '../../types/comparison';
import { formatFileSize } from '../../utils/dataProcessing';

interface DatasetPreviewProps {
  file: UploadedFile;
  onRemove: (fileId: string) => void;
  onTypeChange: (fileId: string, type: 'input' | 'output') => void;
  onUpload: (fileId: string, inputDatasetId?: string) => void;
  inputDatasets?: Array<{ id: string; name: string }>;
  disabled?: boolean;
}

export const DatasetPreview: React.FC<DatasetPreviewProps> = ({
  file,
  onRemove,
  onTypeChange,
  onUpload,
  inputDatasets = [],
  disabled = false
}) => {
  const getStatusIcon = () => {
    switch (file.status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'uploading':
        return <Clock className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = () => {
    switch (file.status) {
      case 'completed':
        return 'border-green-200 bg-green-50';
      case 'error':
        return 'border-red-200 bg-red-50';
      case 'uploading':
        return 'border-blue-200 bg-blue-50';
      default:
        return 'border-gray-200 bg-white';
    }
  };

  const canUpload = file.status === 'pending' && !file.error;
  const needsInputDataset = file.type === 'output' && inputDatasets.length > 0;

  const handleUpload = () => {
    if (needsInputDataset) {
      // For now, use the first available input dataset
      // In a full implementation, you'd want a selection UI
      onUpload(file.id, inputDatasets[0]?.id);
    } else {
      onUpload(file.id);
    }
  };

  return (
    <div className={clsx('border rounded-lg p-4', getStatusColor())}>
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-start gap-3">
          {getStatusIcon()}
          <div>
            <h4 className="font-medium text-gray-900">{file.name}</h4>
            <p className="text-sm text-gray-500">
              {formatFileSize(file.file.size)} • {file.rowCount.toLocaleString()} rows
            </p>
          </div>
        </div>
        <button
          onClick={() => onRemove(file.id)}
          disabled={disabled || file.status === 'uploading'}
          className="p-1 text-gray-400 hover:text-red-500 transition-colors disabled:opacity-50"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {/* Type Selection */}
      <div className="flex items-center gap-2 mb-3">
        <span className="text-sm text-gray-600">Type:</span>
        <div className="flex gap-2">
          <button
            onClick={() => onTypeChange(file.id, 'input')}
            disabled={disabled || file.status !== 'pending'}
            className={clsx(
              'px-3 py-1 rounded-md text-xs font-medium transition-colors',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              file.type === 'input'
                ? 'bg-blue-100 text-blue-700 border border-blue-200'
                : 'bg-gray-100 text-gray-600 border border-gray-200 hover:bg-blue-50'
            )}
          >
            <Database className="w-3 h-3 inline mr-1" />
            Input Dataset
          </button>
          <button
            onClick={() => onTypeChange(file.id, 'output')}
            disabled={disabled || file.status !== 'pending'}
            className={clsx(
              'px-3 py-1 rounded-md text-xs font-medium transition-colors',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              file.type === 'output'
                ? 'bg-green-100 text-green-700 border border-green-200'
                : 'bg-gray-100 text-gray-600 border border-gray-200 hover:bg-green-50'
            )}
          >
            <FileOutput className="w-3 h-3 inline mr-1" />
            Output Dataset
          </button>
        </div>
      </div>

      {/* Error Message */}
      {file.error && (
        <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
          {file.error}
        </div>
      )}

      {/* Preview Table */}
      {file.preview.length > 0 && (
        <div className="mb-3">
          <div className="overflow-x-auto">
            <table className="min-w-full text-xs">
              <thead>
                <tr className="bg-gray-50">
                  {file.preview[0]?.map((header, index) => (
                    <th key={index} className="px-2 py-1 text-left font-medium text-gray-700 border">
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {file.preview.slice(1, 4).map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex} className="px-2 py-1 border text-gray-600">
                        <div className="truncate max-w-24">
                          {cell}
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between">
        <div className="text-xs text-gray-500">
          {file.headers.length > 0 && `${file.headers.length} columns`}
        </div>
        
        {canUpload && (
          <button
            onClick={handleUpload}
            disabled={disabled || (needsInputDataset && inputDatasets.length === 0)}
            className={clsx(
              'px-3 py-1 rounded-md text-xs font-medium transition-colors',
              'bg-primary-500 text-white hover:bg-primary-600',
              'disabled:opacity-50 disabled:cursor-not-allowed'
            )}
          >
            {file.status === 'uploading' ? 'Uploading...' : 'Upload'}
          </button>
        )}
      </div>
    </div>
  );
};