import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Loader, RefreshCw } from 'lucide-react';

function DiagnosticApp() {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'failed'>('checking');
  const [error, setError] = useState<string>('');

  const checkBackendConnection = async () => {
    setBackendStatus('checking');
    setError('');
    
    try {
      console.log('Testing backend connection...');
      const response = await fetch('http://localhost:8000/health', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Backend response:', data);
        setBackendStatus('connected');
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (err) {
      console.error('Backend connection failed:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      setBackendStatus('failed');
    }
  };

  useEffect(() => {
    console.log('DiagnosticApp mounted - checking backend...');
    checkBackendConnection();
  }, []);

  const getStatusIcon = () => {
    switch (backendStatus) {
      case 'checking':
        return <Loader className="w-8 h-8 animate-spin text-blue-500" />;
      case 'connected':
        return <CheckCircle className="w-8 h-8 text-green-500" />;
      case 'failed':
        return <AlertCircle className="w-8 h-8 text-red-500" />;
    }
  };

  const getStatusMessage = () => {
    switch (backendStatus) {
      case 'checking':
        return 'Checking backend connection...';
      case 'connected':
        return '✅ Backend connected successfully!';
      case 'failed':
        return `❌ Backend connection failed: ${error}`;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-600 mb-8 text-center">
          🔍 Oedipus React Diagnostic
        </h1>

        {/* React App Status */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
            <CheckCircle className="w-6 h-6 text-green-500" />
            React Application Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              <span>React Rendering: ✅</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              <span>Tailwind CSS: ✅</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              <span>JavaScript Execution: ✅</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              <span>Component Mounting: ✅</span>
            </div>
          </div>
        </div>

        {/* Backend Connection Status */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
            {getStatusIcon()}
            Backend Connection Test
          </h2>
          
          <div className="mb-4">
            <p className="text-lg">{getStatusMessage()}</p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <p className="font-medium mb-2">Connection Details:</p>
            <ul className="text-sm space-y-1">
              <li>• Frontend: http://localhost:3000</li>
              <li>• Backend Target: http://localhost:8000/health</li>
              <li>• Backend Server: http://0.0.0.0:8000 (may cause connection issues)</li>
            </ul>
          </div>

          <button
            onClick={checkBackendConnection}
            disabled={backendStatus === 'checking'}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 flex items-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${backendStatus === 'checking' ? 'animate-spin' : ''}`} />
            Retry Connection
          </button>
        </div>

        {/* Browser Environment */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4">Browser Environment</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <strong>User Agent:</strong>
              <div className="mt-1 p-2 bg-gray-100 rounded text-xs break-all">
                {navigator.userAgent}
              </div>
            </div>
            <div>
              <strong>Console Check:</strong>
              <div className="mt-1 p-2 bg-gray-100 rounded">
                Open DevTools (F12) → Console tab to check for errors
              </div>
            </div>
          </div>
        </div>

        {/* Solution Steps */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-yellow-800 mb-4">Next Steps</h3>
          <ol className="list-decimal list-inside space-y-2 text-yellow-700">
            <li>If backend connection failed, try accessing: <a href="http://localhost:8000/health" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">http://localhost:8000/health</a></li>
            <li>Check browser console (F12) for JavaScript errors</li>
            <li>If backend is on 0.0.0.0:8000, we may need to update API configuration</li>
            <li>If everything looks good, switch back to main App component</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default DiagnosticApp;