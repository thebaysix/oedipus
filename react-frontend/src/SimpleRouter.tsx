import React, { useState, useEffect } from 'react';
import App from './App';
import AppSimple from './AppSimple';
import AppDebug from './AppDebug';
import DiagnosticApp from './DiagnosticApp';

function SimpleRouter() {
  const [route, setRoute] = useState('/');

  useEffect(() => {
    // Get route from URL hash or pathname
    const updateRoute = () => {
      const hash = window.location.hash.slice(1) || window.location.pathname;
      setRoute(hash || '/');
    };

    updateRoute();
    
    window.addEventListener('hashchange', updateRoute);
    window.addEventListener('popstate', updateRoute);
    
    return () => {
      window.removeEventListener('hashchange', updateRoute);
      window.removeEventListener('popstate', updateRoute);
    };
  }, []);

  console.log('SimpleRouter rendering, route:', route);

  const renderRoute = () => {
    switch (route) {
      case '/diagnostic':
        return <DiagnosticApp />;
      case '/simple':
        return <AppSimple />;
      case '/debug':
        return <AppDebug />;
      case '/':
      default:
        return <App />;
    }
  };

  return (
    <div>
      {/* Navigation */}
      <div className="bg-gray-100 border-b p-2">
        <div className="max-w-7xl mx-auto flex gap-4 text-sm">
          <a href="#/" className={`px-3 py-1 rounded ${route === '/' ? 'bg-blue-500 text-white' : 'text-blue-600 hover:underline'}`}>
            Main App
          </a>
          <a href="#/diagnostic" className={`px-3 py-1 rounded ${route === '/diagnostic' ? 'bg-blue-500 text-white' : 'text-blue-600 hover:underline'}`}>
            Diagnostic
          </a>
          <a href="#/simple" className={`px-3 py-1 rounded ${route === '/simple' ? 'bg-blue-500 text-white' : 'text-blue-600 hover:underline'}`}>
            Simple Test
          </a>
          <a href="#/debug" className={`px-3 py-1 rounded ${route === '/debug' ? 'bg-blue-500 text-white' : 'text-blue-600 hover:underline'}`}>
            Debug Hooks
          </a>
        </div>
      </div>
      
      {/* Content */}
      <div>
        {renderRoute()}
      </div>
    </div>
  );
}

export default SimpleRouter;