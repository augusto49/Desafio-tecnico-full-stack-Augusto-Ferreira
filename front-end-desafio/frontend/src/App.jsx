// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import PrivateRoute from './components/PrivateRoute';

import AdminDashboard from './pages/AdminDashboard';
import DashboardTecnico from './pages/DashboardTecnico';
import DashboardEnfermagem from './pages/DashboardEnfermagem';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota de login */}
        <Route path="/login" element={<LoginPage />} />

        {/* Redireciona a raiz ao login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Dashboards protegidas por role */}
        <Route
          path="/admin/dashboard"
          element={
            <PrivateRoute role="administrativo">
              <AdminDashboard />
            </PrivateRoute>
          }
        />

        <Route
          path="/tecnico/dashboard"
          element={
            <PrivateRoute role="tecnico">
              <DashboardTecnico />
            </PrivateRoute>
          }
        />

        <Route
          path="/enfermagem/dashboard"
          element={
            <PrivateRoute role="enfermagem">
              <DashboardEnfermagem />
            </PrivateRoute>
          }
        />

        {/* Qualquer outra rota → redireciona ao login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
