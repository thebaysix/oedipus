import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import App from './App';
import AppSimple from './AppSimple';
import AppDebug from './AppDebug';
import DiagnosticApp from './DiagnosticApp';

function AppRouter() {
  console.log('AppRouter is rendering');

  return (
    <Router>
      <Routes>
        <Route path="/diagnostic" element={<DiagnosticApp />} />
        <Route path="/simple" element={<AppSimple />} />
        <Route path="/debug" element={<AppDebug />} />
        <Route path="/" element={<App />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;