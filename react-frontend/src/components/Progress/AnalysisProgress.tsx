import React from 'react';
import { CheckCircle, Clock, AlertCircle, RefreshCw } from 'lucide-react';
import { clsx } from 'clsx';

interface AnalysisStep {
  id: string;
  label: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
}

interface AnalysisProgressProps {
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: {
    step: string;
    message: string;
  };
  className?: string;
}

export const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ status, progress, className }) => {
  const getCurrentStep = () => {
    if (status === 'pending') return 'alignment';
    if (status === 'running' && progress?.step) return progress.step;
    if (status === 'completed') return 'completed';
    if (status === 'failed') return 'failed';
    return 'alignment';
  };

  const currentStep = getCurrentStep();

  const steps: AnalysisStep[] = [
    {
      id: 'alignment',
      label: 'Data Alignment',
      description: 'Matching prompts across completion datasets',
      status: status === 'pending' ? 'pending' : 'completed'
    },
    {
      id: 'statistical_analysis',
      label: 'Statistical Analysis',
      description: 'Computing metrics and running statistical tests',
      status: currentStep === 'statistical_analysis' ? 'running' : 
              ['insights', 'visualization', 'completed'].includes(currentStep) ? 'completed' :
              status === 'failed' ? 'failed' : 'pending'
    },
    {
      id: 'insights',
      label: 'Generating Insights',
      description: 'Creating automated observations and recommendations',
      status: currentStep === 'insights' ? 'running' :
              ['visualization', 'completed'].includes(currentStep) ? 'completed' :
              status === 'failed' ? 'failed' : 'pending'
    },
    {
      id: 'visualization',
      label: 'Preparing Visualizations',
      description: 'Building charts and comparison tables',
      status: currentStep === 'visualization' ? 'running' :
              currentStep === 'completed' ? 'completed' :
              status === 'failed' ? 'failed' : 'pending'
    }
  ];

  const getStepIcon = (stepStatus: string) => {
    switch (stepStatus) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'running':
        return <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getProgressPercentage = () => {
    const completedSteps = steps.filter(step => step.status === 'completed').length;
    return (completedSteps / steps.length) * 100;
  };

  return (
    <div className={clsx('bg-white border border-gray-200 rounded-lg p-6', className)}>
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Analysis Progress</h3>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={clsx(
              'h-2 rounded-full transition-all duration-500',
              status === 'failed' ? 'bg-red-500' : 'bg-blue-500'
            )}
            style={{ width: `${getProgressPercentage()}%` }}
          />
        </div>
        <div className="flex justify-between text-sm text-gray-600 mt-1">
          <span>Progress</span>
          <span>{Math.round(getProgressPercentage())}%</span>
        </div>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-0.5">
              {getStepIcon(step.status)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <h4 className={clsx(
                  'text-sm font-medium',
                  step.status === 'completed' && 'text-green-700',
                  step.status === 'running' && 'text-blue-700',
                  step.status === 'failed' && 'text-red-700',
                  step.status === 'pending' && 'text-gray-500'
                )}>
                  {step.label}
                </h4>
                {step.status === 'running' && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    In Progress
                  </span>
                )}
                {step.status === 'completed' && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                    Complete
                  </span>
                )}
                {step.status === 'failed' && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                    Failed
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-600 mt-1">{step.description}</p>
            </div>
          </div>
        ))}
      </div>

      {status === 'running' && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />
            <span className="text-sm text-blue-700 font-medium">
              Analysis is running... This may take a few moments.
            </span>
          </div>
        </div>
      )}

      {status === 'failed' && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-red-500" />
            <span className="text-sm text-red-700 font-medium">
              Analysis failed. Please try creating a new comparison.
            </span>
          </div>
        </div>
      )}
    </div>
  );
};