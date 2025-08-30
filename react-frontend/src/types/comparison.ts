export interface Dataset {
  id: string;
  name: string;
  user_id: string;
  created_at: string;
  prompts: Record<string, string>; // mapping input_id -> input_text
  metadata: Record<string, any>;
  description?: string;
  input_count?: number; // computed field
}

export interface CompletionDataset {
  id: string;
  name: string;
  dataset_id: string;
  created_at: string;
  completions: Record<string, string[]>; // mapping input_id -> output_texts
  metadata: Record<string, any>;
  output_count?: number; // computed field
}

export interface ComparisonCreate {
  name: string;
  dataset_id: string;
  completion_dataset_ids: string[];
  alignment_key?: string;
  comparison_config?: Record<string, any>;
}

export interface Comparison {
  id: string;
  name: string;
  created_at: string;
  datasets: string[];
  alignment_key: string;
  comparison_config: Record<string, any>;
  statistical_results: Record<string, any>;
  automated_insights: string[];
  status: 'pending' | 'running' | 'completed' | 'failed';
}

export interface AlignmentResult {
  alignedRows: AlignedRow[];
  unmatchedInputs: string[];
  coverageStats: {
    totalInputs: number;
    matchedInputs: number;
    coveragePercentage: number;
  };
}

export interface AlignedRow {
  inputId: string;
  inputText: string;
  completions: Record<string, string[] | null>;
  metadata: Record<string, Record<string, any>>;
}

export interface UploadedFile {
  id: string;
  file: File;
  name: string;
  preview: string[][];
  headers: string[];
  rowCount: number;
  type: 'input' | 'output';
  status: 'pending' | 'uploading' | 'completed' | 'error';
  error?: string;
}

export interface StatisticalMetric {
  name: string;
  dataset_a_value: number;
  dataset_b_value: number;
  statistical_significance: number;
  effect_size: number;
  confidence_interval_lower: number;
  confidence_interval_upper: number;
}