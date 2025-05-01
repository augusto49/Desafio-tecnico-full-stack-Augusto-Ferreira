import { useState } from 'react';
import UserList from '../components/admin/UserList';
import UserForm from '../components/admin/UserForm';
import '../utils/adminDashboard.css';

export default function AdminDashboard() {
  // Função de logout
  const logout = () => {
    // Limpar dados de autenticação (localStorage, cookies, etc.)
    localStorage.removeItem('authToken'); // ou qualquer item que esteja armazenando o token
    
    // Redirecionar o usuário para a tela de login
    window.location.href = '/'; // ou qualquer rota de login no seu projeto
  };

  return (
    <div className="admin-dashboard-container">
      <div className="logout-button">
        <button className="button-primary" onClick={logout}>
          Sair
        </button>
      </div>

      <div className="admin-card">
        <h2>Dashboard do Administrador</h2>
        <UserForm />
      </div>

      <div className="admin-card">
        <UserList />
      </div>
    </div>
  );
}
