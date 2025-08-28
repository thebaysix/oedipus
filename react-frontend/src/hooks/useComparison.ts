import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../utils/api';
import { Dataset, OutputDataset, Comparison, ComparisonCreate } from '../types/comparison';

export const useDatasets = () => {
  return useQuery({
    queryKey: ['datasets'],
    queryFn: () => apiClient.get<Dataset[]>('/api/v1/datasets/'),
    retry: false, // Don't retry failed requests
    staleTime: 0, // Always attempt fresh data
  });
};

export const useOutputDatasets = (datasetId: string) => {
  return useQuery({
    queryKey: ['outputs', datasetId],
    queryFn: () => apiClient.get<OutputDataset[]>(`/api/v1/datasets/${datasetId}/outputs`),
    enabled: !!datasetId,
  });
};

export const useComparisons = () => {
  return useQuery({
    queryKey: ['comparisons'],
    queryFn: () => apiClient.get<Comparison[]>('/api/v1/comparisons/'),
  });
};

export const useComparison = (comparisonId: string) => {
  return useQuery({
    queryKey: ['comparison', comparisonId],
    queryFn: () => apiClient.get<Comparison>(`/api/v1/comparisons/${comparisonId}`),
    enabled: !!comparisonId,
    refetchInterval: (data) => {
      // Poll while status is pending or running
      return data?.status === 'pending' || data?.status === 'running' ? 2000 : false;
    },
  });
};

export const useCreateComparison = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: ComparisonCreate) => 
      apiClient.post<Comparison>('/api/v1/comparisons/create', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comparisons'] });
    },
  });
};

export const useDeleteComparison = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (comparisonId: string) => 
      apiClient.delete(`/api/v1/comparisons/${comparisonId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comparisons'] });
    },
  });
};