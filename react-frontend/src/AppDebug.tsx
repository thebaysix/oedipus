import React from 'react';
import { useDatasets } from './hooks/useComparison';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';

function AppDebug() {
  console.log('AppDebug rendering...');
  
  const { data: datasets = [], error: datasetsError, isLoading, isError } = useDatasets();
  
  console.log('Datasets state:', { datasets, datasetsError, isLoading, isError });

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-600 mb-8">App Debug</h1>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4">useDatasets() Hook Debug</h2>
          
          <div className="grid grid-cols-1 gap-4">
            <div className="flex items-center gap-3">
              <strong>Loading:</strong>
              {isLoading ? (
                <><Loader className="w-5 h-5 animate-spin text-blue-500" /> Yes</>
              ) : (
                <><CheckCircle className="w-5 h-5 text-green-500" /> No</>
              )}
            </div>
            
            <div className="flex items-center gap-3">
              <strong>Error:</strong>
              {isError ? (
                <><AlertCircle className="w-5 h-5 text-red-500" /> Yes</>
              ) : (
                <><CheckCircle className="w-5 h-5 text-green-500" /> No</>
              )}
            </div>
            
            <div>
              <strong>Datasets Count:</strong> {datasets?.length || 0}
            </div>
            
            {datasetsError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <strong className="text-red-800">Error Details:</strong>
                <pre className="text-red-700 text-sm mt-2 whitespace-pre-wrap">
                  {JSON.stringify(datasetsError, null, 2)}
                </pre>
              </div>
            )}
            
            {datasets && datasets.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <strong className="text-green-800">Datasets:</strong>
                <pre className="text-green-700 text-sm mt-2 whitespace-pre-wrap">
                  {JSON.stringify(datasets, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-blue-800 mb-2">Debug Notes</h3>
          <ul className="text-blue-700 space-y-1">
            <li>• Check browser console for additional logs</li>
            <li>• This shows the exact state of the useDatasets hook</li>
            <li>• If this renders but main App doesn't, issue is in App component logic</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default AppDebug;