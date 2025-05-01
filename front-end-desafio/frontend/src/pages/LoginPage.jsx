import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../utils/LoginPage.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/token/', form);
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      const userInfo = await axios.get('http://localhost:8000/api/users/me/', {
        headers: { Authorization: `Bearer ${response.data.access}` }
      });

      const role = userInfo.data.role;
      localStorage.setItem('role', role);

      if (role === 'administrativo') navigate('/admin/dashboard');
      else if (role === 'tecnico') navigate('/tecnico/dashboard');
      else if (role === 'enfermagem') navigate('/enfermagem/dashboard');
      else navigate('/login');
    } catch (err) {
      setError('Credenciais inválidas');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Login</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            name="username"
            className="login-input"
            placeholder="Usuário"
            onChange={handleChange}
            required
          />
          <input
            name="password"
            type="password"
            className="login-input"
            placeholder="Senha"
            onChange={handleChange}
            required
          />
          <button type="submit" className="login-button">Entrar</button>
        </form>
        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}
