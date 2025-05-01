import { useState } from 'react';
import API from '../../api';

export default function UserForm() {
  const [form, setForm] = useState({ username: '', password: '', role: 'tecnico' });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Remove espaços apenas do campo username
    const sanitizedValue = name === 'username' ? value.replace(/\s/g, '') : value;
    setForm({ ...form, [name]: sanitizedValue });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post('/users/register/', form);
      setMessage('Usuário criado com sucesso');
      setForm({ username: '', password: '', role: 'tecnico' });
    } catch (err) {
      setMessage('Erro ao criar usuário');
    }
  };

  return (
    <div>
      <h3>Cadastrar novo usuário</h3>
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          placeholder="Usuário (sem espaços)"
          value={form.username}
          onChange={handleChange}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Senha"
          value={form.password}
          onChange={handleChange}
          required
        />
        <select name="role" value={form.role} onChange={handleChange}>
          <option value="administrativo">Administrador</option>
          <option value="tecnico">Técnico</option>
          <option value="enfermagem">Enfermagem</option>
        </select>
        <button type="submit">Criar</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}
