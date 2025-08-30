import Papa from 'papaparse';

export interface ParseResult {
  data: string[][];
  headers: string[];
  rowCount: number;
  errors: string[];
}

export const parseCSVFile = (file: File): Promise<ParseResult> => {
  return new Promise((resolve) => {
    Papa.parse(file, {
      header: false,
      skipEmptyLines: true,
      complete: (results) => {
        const data = results.data as string[][];
        const errors = results.errors.map(e => e.message);
        
        if (data.length === 0) {
          resolve({
            data: [],
            headers: [],
            rowCount: 0,
            errors: ['File is empty']
          });
          return;
        }

        const headers = data[0] || [];
        const dataRows = data.slice(1);

        resolve({
          data: dataRows,
          headers,
          rowCount: dataRows.length,
          errors
        });
      }
    });
  });
};

export const validateInputDataset = (headers: string[]): string[] => {
  const errors: string[] = [];
  
  if (!headers.includes('input_id')) {
    errors.push('Missing required column: input_id');
  }
  
  if (!headers.includes('input_text')) {
    errors.push('Missing required column: input_text');
  }
  
  return errors;
};

export const validateOutputDataset = (headers: string[]): string[] => {
  const errors: string[] = [];
  
  if (!headers.includes('input_id')) {
    errors.push('Missing required column: input_id');
  }
  
  if (!headers.includes('output_text')) {
    errors.push('Missing required column: output_text');
  }
  
  return errors;
};

export const generatePreview = (data: string[][], maxRows: number = 5): string[][] => {
  return data.slice(0, maxRows);
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

export const calculateStatistics = (values: number[]) => {
  if (values.length === 0) return { mean: 0, std: 0, min: 0, max: 0 };
  
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;
  const std = Math.sqrt(variance);
  const min = Math.min(...values);
  const max = Math.max(...values);
  
  return { mean, std, min, max };
};