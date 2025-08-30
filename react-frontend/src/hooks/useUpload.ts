import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../utils/api';
import { parseCSVFile, validateInputDataset, validateOutputDataset, generatePreview } from '../utils/dataProcessing';
import { UploadedFile, Dataset, OutputDataset } from '../types/comparison';

export const useUpload = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const queryClient = useQueryClient();

  const createDatasetMutation = useMutation({
    mutationFn: async (data: FormData) => {
      return apiClient.postFormData<Dataset>('/api/v1/datasets/upload', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['datasets'] });
    }
  });

  const createOutputDatasetMutation = useMutation({
    mutationFn: async ({ datasetId, formData }: { datasetId: string, formData: FormData }) => {
      return apiClient.postFormData<OutputDataset>(`/api/v1/datasets/${datasetId}/outputs/upload`, formData);
    },
    onSuccess: () => {
      // Invalidate and refetch relevant queries after output upload
      queryClient.invalidateQueries({ queryKey: ['datasets'] });
      queryClient.invalidateQueries({ queryKey: ['all-outputs'] });
      queryClient.refetchQueries({ queryKey: ['all-outputs'] });
    }
  });

  const processFiles = useCallback(async (acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = [];

    for (const file of acceptedFiles) {
      try {
        const parseResult = await parseCSVFile(file);
        
        if (parseResult.errors.length > 0) {
          newFiles.push({
            id: Math.random().toString(),
            file,
            name: file.name,
            preview: [],
            headers: [],
            rowCount: 0,
            type: 'input',
            status: 'error',
            error: parseResult.errors.join(', ')
          });
          continue;
        }

        // Detect file type based on headers
        const inputErrors = validateInputDataset(parseResult.headers);
        const outputErrors = validateOutputDataset(parseResult.headers);
        
        const isInput = inputErrors.length === 0;
        const isOutput = outputErrors.length === 0;
        
        let fileType: 'input' | 'output' = 'input';
        let validationErrors: string[] = [];
        
        if (isInput && !isOutput) {
          fileType = 'input';
        } else if (isOutput && !isInput) {
          fileType = 'output';
        } else if (isInput && isOutput) {
          // Both valid, default to input
          fileType = 'input';
        } else {
          // Neither valid
          validationErrors = [...inputErrors, ...outputErrors];
        }

        newFiles.push({
          id: Math.random().toString(),
          file,
          name: file.name,
          preview: [parseResult.headers, ...generatePreview(parseResult.data)],
          headers: parseResult.headers,
          rowCount: parseResult.rowCount,
          type: fileType,
          status: validationErrors.length > 0 ? 'error' : 'pending',
          error: validationErrors.length > 0 ? validationErrors.join(', ') : undefined
        });
      } catch (error) {
        newFiles.push({
          id: Math.random().toString(),
          file,
          name: file.name,
          preview: [],
          headers: [],
          rowCount: 0,
          type: 'input',
          status: 'error',
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }

    setFiles(prev => [...prev, ...newFiles]);
  }, []);

  const removeFile = useCallback((fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
  }, []);

  const updateFileType = useCallback((fileId: string, type: 'input' | 'output') => {
    setFiles(prev => prev.map(f => {
      if (f.id === fileId) {
        // Re-validate with new type
        const validationErrors = type === 'input' 
          ? validateInputDataset(f.headers)
          : validateOutputDataset(f.headers);
        
        return {
          ...f,
          type,
          status: validationErrors.length > 0 ? 'error' : 'pending',
          error: validationErrors.length > 0 ? validationErrors.join(', ') : undefined
        };
      }
      return f;
    }));
  }, []);

  const uploadFile = useCallback(async (fileId: string, inputDatasetId?: string) => {
    const file = files.find(f => f.id === fileId);
    if (!file) return;

    setFiles(prev => prev.map(f => 
      f.id === fileId ? { ...f, status: 'uploading' } : f
    ));

    try {
      const formData = new FormData();
      formData.append('file', file.file);
      formData.append('name', file.name.replace('.csv', ''));

      if (file.type === 'input') {
        const result = await createDatasetMutation.mutateAsync(formData);
        setFiles(prev => prev.map(f => 
          f.id === fileId ? { ...f, status: 'completed' } : f
        ));
        return result;
      } else {
        if (!inputDatasetId) throw new Error('Input dataset ID required for output upload');
        const result = await createOutputDatasetMutation.mutateAsync({
          datasetId: inputDatasetId,
          formData
        });
        setFiles(prev => prev.map(f => 
          f.id === fileId ? { ...f, status: 'completed' } : f
        ));
        return result;
      }
    } catch (error) {
      setFiles(prev => prev.map(f => 
        f.id === fileId ? { 
          ...f, 
          status: 'error',
          error: error instanceof Error ? error.message : 'Upload failed'
        } : f
      ));
      throw error;
    }
  }, [files, createDatasetMutation, createOutputDatasetMutation]);

  const clearFiles = useCallback(() => {
    setFiles([]);
  }, []);

  return {
    files,
    processFiles,
    removeFile,
    updateFileType,
    uploadFile,
    clearFiles,
    isUploading: createDatasetMutation.isPending || createOutputDatasetMutation.isPending
  };
};