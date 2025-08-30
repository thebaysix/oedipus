import React from 'react';
import { BarChart3 } from 'lucide-react';

function AppSimple() {
  console.log('AppSimple is rendering');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Oedipus</h1>
              <p className="text-gray-600">Comparative Analysis Platform</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Simple App Test</h2>
            <p className="text-gray-600 mb-6">
              This is a simplified version of the main App to test basic rendering.
            </p>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-green-800 mb-2">✅ App Rendering Successfully</h3>
              <p className="text-green-700">
                The basic app structure is working. The issue is likely with React Query hooks or complex components.
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">🔧 Debug Information</h3>
              <ul className="text-left text-blue-700 space-y-1">
                <li>• React rendering: Working</li>
                <li>• Tailwind CSS: Working</li>
                <li>• Component structure: Working</li>
                <li>• Issue: Likely in React Query hooks or complex components</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default AppSimple;