// src/customer_health_dashboard/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import Dashboard from './Dashboard';
import './styles/index.css';

const root = document.getElementById('dashboard-root');
createRoot(root).render(
  <React.StrictMode>
    <Dashboard />
  </React.StrictMode>
);