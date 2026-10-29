
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import './styles/global.css';

const redirectRoute = sessionStorage.getItem('spa-route');
if (redirectRoute) {
  sessionStorage.removeItem('spa-route');
  window.history.replaceState(null, '', redirectRoute);
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter basename="/Cloud-Based-Assignment-Submission-Portal">
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
