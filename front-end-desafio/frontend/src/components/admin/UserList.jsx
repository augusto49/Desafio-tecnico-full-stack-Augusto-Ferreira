import { useEffect, useState } from 'react';
import API from '../../api';

export default function UserList() {
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState({});
  const [message, setMessage] = useState('');

  const fetchUsers = async () => {
    const res = await API.get('/users/list/');
    setUsers(res.data);

    const initialRoles = {};
    res.data.forEach((user) => {
      initialRoles[user.id] = user.role;
    });
    setRoles(initialRoles);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleRoleChange = (userId, newRole) => {
    setRoles((prev) => ({
      ...prev,
      [userId]: newRole,
    }));
  };

  const handleUpdateRole = async (userId) => {
    try {
      await API.patch(`/users/update-role/${userId}/`, { role: roles[userId] });
      setMessage('Função atualizada com sucesso');
      fetchUsers();
    } catch {
      setMessage('Erro ao atualizar função');
    }
  };

  return (
    <div>
      <h3>Lista de usuários</h3>
      {users.map((user) => (
        <div key={user.id} className="user-card">
          <span><strong>{user.username}</strong></span>
          <div className="select-role">
            <select
              value={roles[user.id] || user.role}
              onChange={(e) => handleRoleChange(user.id, e.target.value)}
            >
              <option value="administrativo">Administrador</option>
              <option value="tecnico">Técnico</option>
              <option value="enfermagem">Enfermagem</option>
            </select>
            <button onClick={() => handleUpdateRole(user.id)}>Atualizar</button>
          </div>
        </div>
      ))}
      {message && <p className="message">{message}</p>}
    </div>
  );
}
