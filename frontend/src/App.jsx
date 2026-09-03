import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { SubmitComplaint } from './pages/SubmitComplaint';
import { ComplaintHistory } from './pages/ComplaintHistory';
import { ComplaintDetails } from './pages/ComplaintDetails';
import { FeatureCatalog } from './pages/FeatureCatalog';
import { AnalyticsPage } from './pages/AnalyticsPage';

const ProtectedLayout = ({ children }) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 overflow-y-auto max-w-7xl mx-auto w-full">
          {children}
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedLayout>
                <Dashboard />
              </ProtectedLayout>
            }
          />
          <Route
            path="/submit-complaint"
            element={
              <ProtectedLayout>
                <SubmitComplaint />
              </ProtectedLayout>
            }
          />
          <Route
            path="/my-complaints"
            element={
              <ProtectedLayout>
                <ComplaintHistory />
              </ProtectedLayout>
            }
          />
          <Route
            path="/complaints/:id"
            element={
              <ProtectedLayout>
                <ComplaintDetails />
              </ProtectedLayout>
            }
          />
          <Route
            path="/features"
            element={
              <ProtectedLayout>
                <FeatureCatalog />
              </ProtectedLayout>
            }
          />
          <Route
            path="/analytics"
            element={
              <ProtectedLayout>
                <AnalyticsPage />
              </ProtectedLayout>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
