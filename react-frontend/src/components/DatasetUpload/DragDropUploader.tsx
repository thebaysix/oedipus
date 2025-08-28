import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { clsx } from 'clsx';

interface DragDropUploaderProps {
  onFilesAdded: (files: File[]) => void;
  disabled?: boolean;
  className?: string;
}

export const DragDropUploader: React.FC<DragDropUploaderProps> = ({ 
  onFilesAdded, 
  disabled = false,
  className 
}) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    onFilesAdded(acceptedFiles);
  }, [onFilesAdded]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv']
    },
    multiple: true,
    disabled,
  });

  return (
    <div
      {...getRootProps()}
      className={clsx(
        'border-2 border-dashed rounded-lg p-8 text-center transition-all cursor-pointer',
        'hover:border-primary-400 hover:bg-primary-50',
        {
          'border-gray-300 bg-gray-50': !isDragActive && !isDragReject,
          'border-primary-500 bg-primary-100': isDragActive && !isDragReject,
          'border-red-500 bg-red-50': isDragReject,
          'opacity-50 cursor-not-allowed': disabled,
        },
        className
      )}
    >
      <input {...getInputProps()} />
      
      <div className="flex flex-col items-center gap-4">
        {isDragReject ? (
          <AlertCircle className="w-12 h-12 text-red-500" />
        ) : (
          <Upload className="w-12 h-12 text-gray-400" />
        )}
        
        <div>
          <p className="text-lg font-semibold text-gray-700">
            {isDragActive
              ? isDragReject
                ? 'Invalid file type'
                : 'Drop CSV files here'
              : 'Drag & drop CSV files here'
            }
          </p>
          <p className="text-sm text-gray-500 mt-1">
            or click to browse files
          </p>
        </div>
        
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <FileText className="w-4 h-4" />
          <span>Supports CSV files only</span>
        </div>
      </div>
    </div>
  );
};