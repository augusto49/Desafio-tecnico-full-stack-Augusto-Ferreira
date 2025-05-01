import { useState, useEffect } from 'react';
import API from '../api';
import '../utils/DashboardEnfermagem.css'; // Adicionando o arquivo CSS

export default function DashboardEnfermagem() {
  const [serial, setSerial] = useState('');
  const [materiais, setMateriais] = useState([]);
  const [etapas, setEtapas] = useState([]);
  const [falhas, setFalhas] = useState([]);
  const [processos, setProcessos] = useState(0);
  const [mensagem, setMensagem] = useState('');
  const [novaFalha, setNovaFalha] = useState('');

  useEffect(() => {
    const fetchMateriais = async () => {
      try {
        const res = await API.get('/materials/list/');
        setMateriais(res.data);
      } catch (err) {
        console.error('Erro ao carregar materiais:', err);
      }
    };

    fetchMateriais();
  }, []);

  const buscarDados = async () => {
    if (!serial) {
      setMensagem('Selecione um serial');
      return;
    }

    try {
      const res = await API.get(`/users/rastreabilidade/?serial=${serial}`);
      setEtapas(res.data.etapas || []);
      setFalhas(res.data.falhas || []);
      setProcessos(res.data.total_processos || 0);
      setMensagem('');
    } catch (err) {
      setMensagem('Erro ao buscar dados do serial');
      setEtapas([]);
      setFalhas([]);
      setProcessos(0);
    }
  };

  const exportar = async (formato) => {
    try {
      // Importante: use /users/relatorio/ conforme definido em users/urls.py
      const res = await API.get(
        `/relatorio/?format=${formato}&serial=${serial}`,
        { responseType: 'blob' }
      );

      const blob = new Blob([res.data], {
        type:
          formato === 'pdf'
            ? 'application/pdf'
            : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `relatorio_serial_${serial}.${formato}`;
      link.click();
    } catch {
      setMensagem('Erro ao exportar relatório');
    }
  };

  const registrarFalha = async () => {
    if (!novaFalha.trim()) {
      setMensagem('Informe a descrição da falha');
      return;
    }

    try {
      // Use /users/falhas/ conforme definido em users/urls.py
      await API.post('/falhas/', {
        serial,
        descricao: novaFalha,
      });
      setNovaFalha('');
      setMensagem('Falha registrada com sucesso');
      buscarDados(); // Atualiza a lista de falhas
    } catch (err) {
      setMensagem('Erro ao registrar falha');
    }
  };

  // Função de logout
  const logout = () => {
    // Limpar dados de autenticação (localStorage, cookies, etc.)
    localStorage.removeItem('authToken'); // ou qualquer item que esteja armazenando o token
    
    // Redirecionar o usuário para a tela de login
    window.location.href = '/login'; // ou qualquer rota de login no seu projeto
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-title">
        <h2>Dashboard da Enfermagem</h2>
      </div>

      {/* Botão de Logout */}
      <div className="logout-button">
        <button className="button-primary" onClick={logout}>
          Sair
        </button>
      </div>

      <div className="card">
        <div className="input-group">
          <label htmlFor="serial">Selecionar Serial:</label>
          <select
            id="serial"
            value={serial}
            onChange={(e) => setSerial(e.target.value)}
          >
            <option value="">-- Escolha um serial --</option>
            {materiais.map((mat) => (
              <option key={mat.id} value={mat.serial}>
                {mat.serial}
              </option>
            ))}
          </select>
        </div>

        <div className="input-group">
          <button className="button-primary" onClick={buscarDados}>
            Buscar
          </button>
        </div>

        {mensagem && <p className="mensagem">{mensagem}</p>}

        {serial && (
          <>
            {etapas.length > 0 && (
              <>
                <h3>Etapas processadas:</h3>
                <ul className="etapas-list">
                  {etapas.map((etapa, i) => (
                    <li className="etapas-item" key={i}>
                      {etapa.nome} - {etapa.data} - Responsável: {etapa.usuario}
                    </li>
                  ))}
                </ul>
                <p>
                  <strong>Total de vezes processado:</strong> {processos}
                </p>
              </>
            )}

            {falhas.length > 0 && (
              <>
                <h3>Falhas detectadas:</h3>
                <ul className="etapas-list">
                  {falhas.map((falha, i) => (
                    <li className="etapas-item" key={i}>
                      {falha.descricao} - {falha.data}
                    </li>
                  ))}
                </ul>
              </>
            )}

            {/* Formulário para registrar nova falha */}
            <div style={{ marginTop: '20px' }}>
              <h4>Registrar nova falha:</h4>
              <textarea
                value={novaFalha}
                onChange={(e) => setNovaFalha(e.target.value)}
                placeholder="Descrição da falha"
                rows={3}
                style={{ width: '100%', padding: '8px', fontSize: '14px' }}
              />
              <br />
              <button
                className="button-primary"
                onClick={registrarFalha}
                style={{ marginTop: '8px' }}
              >
                Enviar falha
              </button>
            </div>

            {/* Botões de exportação */}
            <div style={{ marginTop: '20px' }}>
              <button
                className="button-primary"
                onClick={() => exportar('pdf')}
              >
                Exportar PDF
              </button>
              <button
                className="button-primary"
                onClick={() => exportar('xlsx')}
                style={{ marginLeft: '10px' }}
              >
                Exportar XLSX
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
