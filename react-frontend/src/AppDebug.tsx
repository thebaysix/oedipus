import React, { useState } from 'react';
import { useDatasets, useAllOutputDatasets } from './hooks/useComparison';
import { AlertCircle, CheckCircle, Loader, RefreshCw } from 'lucide-react';

function AppDebug() {
  console.log('AppDebug rendering...');
  const [testApiResults, setTestApiResults] = useState<string>('');
  
  const { data: datasets = [], error: datasetsError, isLoading, isError } = useDatasets();
  const { data: allOutputDatasets = [], error: outputDatasetsError, isLoading: isLoadingOutputs, refetch: refetchOutputs } = useAllOutputDatasets(datasets.map(d => d.id));
  
  console.log('Datasets state:', { datasets, datasetsError, isLoading, isError });
  console.log('Output datasets state:', { allOutputDatasets, outputDatasetsError, isLoadingOutputs });

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
              <strong>Prompts Count:</strong> {datasets?.length || 0}
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
                <strong className="text-green-800">Prompt Datasets:</strong>
                <pre className="text-green-700 text-sm mt-2 whitespace-pre-wrap">
                  {JSON.stringify(datasets, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4">useAllOutputDatasets() Hook Debug</h2>
          
          <div className="grid grid-cols-1 gap-4">
            <div className="flex items-center gap-3">
              <strong>Loading:</strong>
              {isLoadingOutputs ? (
                <><Loader className="w-5 h-5 animate-spin text-blue-500" /> Yes</>
              ) : (
                <><CheckCircle className="w-5 h-5 text-green-500" /> No</>
              )}
            </div>
            
            <div className="flex items-center gap-3">
              <strong>Error:</strong>
              {outputDatasetsError ? (
                <><AlertCircle className="w-5 h-5 text-red-500" /> Yes</>
              ) : (
                <><CheckCircle className="w-5 h-5 text-green-500" /> No</>
              )}
            </div>
            
            <div>
              <strong>Completions Count:</strong> {allOutputDatasets?.length || 0}
            </div>
            
            <div className="flex gap-2 mt-2">
              <button
                onClick={() => refetchOutputs()}
                className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded text-sm hover:bg-blue-200"
              >
                <RefreshCw className="w-4 h-4" />
                Refetch Completions
              </button>
              
              <button
                onClick={async () => {
                  if (datasets.length > 0) {
                    const datasetId = datasets[0].id;
                    try {
                      const response = await fetch(`http://localhost:8000/api/v1/datasets/${datasetId}/outputs`);
                      const data = await response.json();
                      setTestApiResults(`Direct API: Found ${data.length} completions for dataset ${datasetId}`);
                    } catch (error) {
                      setTestApiResults(`Direct API failed: ${error.message}`);
                    }
                  } else {
                    setTestApiResults('No prompt datasets available to test');
                  }
                }}
                className="px-3 py-1 bg-green-100 text-green-800 rounded text-sm hover:bg-green-200"
                disabled={datasets.length === 0}
              >
                Test Direct API
              </button>
            </div>

            {testApiResults && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <div className="text-blue-800 font-medium">API Test Results:</div>
                <div className="text-blue-700 text-sm mt-1">{testApiResults}</div>
              </div>
            )}
            
            {outputDatasetsError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <strong className="text-red-800">Error Details:</strong>
                <pre className="text-red-700 text-sm mt-2 whitespace-pre-wrap">
                  {JSON.stringify(outputDatasetsError, null, 2)}
                </pre>
              </div>
            )}
            
            {allOutputDatasets && allOutputDatasets.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <strong className="text-green-800">Completion Datasets:</strong>
                <pre className="text-green-700 text-sm mt-2 whitespace-pre-wrap">
                  {JSON.stringify(allOutputDatasets, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <h3 className="text-xl font-semibold text-blue-800 mb-2">Debug Notes</h3>
          <ul className="text-blue-700 space-y-1">
            <li>• Check browser console for additional logs</li>
            <li>• This shows the exact state of React Query hooks</li>
            <li>• Use "Refetch Completions" if data appears stale</li>
            <li>• Use "Test Direct API" to bypass React Query caching</li>
          </ul>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-green-800 mb-2">Recent Bug Fixes</h3>
          <div className="text-green-700 space-y-2">
            <div className="font-medium">✅ Fixed: Automatic Completion Loading</div>
            <div className="text-sm">
              <strong>Issue:</strong> After uploading completions, the Create Comparison page showed "Completions: 0" instead of the correct count, requiring manual refresh.
            </div>
            <div className="text-sm">
              <strong>Root Cause:</strong> React Query was caching empty results and not refetching when new completions were uploaded.
            </div>
            <div className="text-sm">
              <strong>Solution:</strong> Added <code className="bg-green-100 px-1 rounded">queryClient.invalidateQueries(['all-outputs'])</code> to the upload success callback in <code className="bg-green-100 px-1 rounded">useUpload.ts</code>.
            </div>
            <div className="text-sm">
              <strong>Result:</strong> Completions now load automatically after upload without manual intervention.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AppDebug;