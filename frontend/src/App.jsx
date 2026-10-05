import React, { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Loader2 } from 'lucide-react';

const Login = lazy(() => import('./pages/Login').then(m => ({ default: m.Login })));
const Dashboard = lazy(() => import('./pages/Dashboard').then(m => ({ default: m.Dashboard })));
const SubmitComplaint = lazy(() => import('./pages/SubmitComplaint').then(m => ({ default: m.SubmitComplaint })));
const ComplaintHistory = lazy(() => import('./pages/ComplaintHistory').then(m => ({ default: m.ComplaintHistory })));
const ComplaintDetails = lazy(() => import('./pages/ComplaintDetails').then(m => ({ default: m.ComplaintDetails })));
const FeatureCatalog = lazy(() => import('./pages/FeatureCatalog').then(m => ({ default: m.FeatureCatalog })));
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage').then(m => ({ default: m.AnalyticsPage })));

const PageLoader = () => (
  <div className="flex items-center justify-center min-h-[60vh] text-slate-400">
    <div className="flex flex-col items-center gap-3">
      <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      <span className="text-xs font-semibold text-slate-400">Loading module...</span>
    </div>
  </div>
);

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
        <Suspense fallback={<PageLoader />}>
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
        </Suspense>
      </BrowserRouter>
    </AuthProvider>
  );
}

