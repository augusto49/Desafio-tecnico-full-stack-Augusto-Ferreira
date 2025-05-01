// src/components/PrivateRoute.jsx
import { Navigate } from 'react-router-dom';

export default function PrivateRoute({ children, role }) {
  const token = localStorage.getItem('access');
  const userRole = localStorage.getItem('role');

  // Se não tiver token ou role diferente, redireciona ao login
  if (!token || (role && userRole !== role)) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
