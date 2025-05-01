import { useEffect, useState } from 'react';
import API from '../api';
import '../utils/DashboardTecnico.css';  // Supondo que o CSS esteja em um arquivo separado

export default function DashboardTecnico() {
  const [materiais, setMateriais] = useState([]);
  const [serial, setSerial] = useState('');
  const [etapa, setEtapa] = useState('');
  const [observacao, setObservacao] = useState('');
  const [mensagem, setMensagem] = useState('');

  const [serialConsulta, setSerialConsulta] = useState('');
  const [etapasRealizadas, setEtapasRealizadas] = useState([]);
  const [statusAtual, setStatusAtual] = useState('');  // Status atual do material
  const [historicoEtapas, setHistoricoEtapas] = useState({}); // Histórico de quantas vezes passou por cada etapa

  const [nome, setNome] = useState('');
  const [tipo, setTipo] = useState('');
  const [dataValidade, setDataValidade] = useState('');

  useEffect(() => {
    buscarMateriais();
  }, []);

  const buscarMateriais = async () => {
    try {
      const res = await API.get('/materials/list/');
      setMateriais(res.data);
    } catch (err) {
      console.error('Erro ao buscar materiais:', err);
    }
  };

  const registrarEtapa = async () => {
    if (!serial || !etapa) {
      setMensagem('Preencha os campos de serial e etapa.');
      return;
    }

    try {
      const res = await API.post('/users/etapas/', {
        serial: serial,
        etapa: etapa,
        observacao: observacao || 'Sem observação',
      });

      setMensagem(`Etapa "${etapa}" registrada com sucesso para o material ${serial}.`);
      buscarMateriais();
      atualizarStatusAtualETemporizador();
    } catch (err) {
      console.error('Erro ao registrar etapa:', err.response?.data || err);
      if (err.response?.data?.etapa) {
        setMensagem(err.response.data.etapa[0]);
      } else if (err.response?.data?.serial) {
        setMensagem(err.response.data.serial[0]);
      } else {
        setMensagem('Erro ao registrar etapa. Verifique os dados.');
      }
    }
  };

  const buscarEtapasDoMaterial = async () => {
    if (!serialConsulta) {
      setMensagem('Informe um serial para buscar as etapas.');
      return;
    }

    try {
      const res = await API.get(`/users/etapas/${serialConsulta}/`);
      if (res.data && res.data.length > 0) {
        const procedimentosComEtapas = res.data.map((proc) => ({
          procedimento_id: proc.procedimento_id,
          data_inicio: proc.data_inicio,
          etapas: proc.etapas.sort(
            (a, b) => new Date(a.data_realizacao) - new Date(b.data_realizacao)
          ),
        }));

        setEtapasRealizadas(procedimentosComEtapas);
        setStatusAtual(res.data.status);
        setMensagem(`Etapas carregadas para o material ${serialConsulta}.`);
        atualizarHistoricoEtapas(procedimentosComEtapas);

        let ultimaEtapa = '';
        if (procedimentosComEtapas.length > 0) {
          const todasEtapas = procedimentosComEtapas.flatMap(p => p.etapas);
          if (todasEtapas.length > 0) {
            todasEtapas.sort((a, b) => new Date(a.data_realizacao) - new Date(b.data_realizacao));
            ultimaEtapa = todasEtapas[todasEtapas.length - 1].etapa;
          }
        }
        setStatusAtual(ultimaEtapa || 'Nenhuma etapa registrada');
      } else {
        setEtapasRealizadas([]);
        setMensagem('Nenhuma etapa encontrada para o material.');
      }
    } catch (err) {
      console.error('Erro ao buscar etapas:', err.response?.data || err);
      setMensagem('Erro ao buscar etapas do material.');
      setEtapasRealizadas([]);
    }
  };

  const atualizarHistoricoEtapas = (procedimentosComEtapas) => {
    const novoHistorico = {};
    procedimentosComEtapas.forEach((proc) => {
      proc.etapas.forEach((etapa) => {
        if (novoHistorico[etapa.etapa]) {
          novoHistorico[etapa.etapa]++;
        } else {
          novoHistorico[etapa.etapa] = 1;
        }
      });
    });
    setHistoricoEtapas(novoHistorico);
  };

  const formatarData = (dataIso) => {
    const data = new Date(dataIso);
    return `${data.toLocaleDateString()} ${data.toLocaleTimeString().slice(0, 5)}`;
  };

  const criarMaterial = async () => {
    if (!nome || !tipo || !dataValidade) {
      setMensagem('Preencha todos os campos para criar o material.');
      return;
    }

    try {
      const res = await API.post('/materials/', {
        nome,
        tipo,
        data_validade: dataValidade,
      });

      setMensagem(`Material "${nome}" criado com sucesso!`);
      buscarMateriais();
      setNome('');
      setTipo('');
      setDataValidade('');
    } catch (err) {
      console.error('Erro ao criar material:', err.response?.data || err);
      setMensagem('Erro ao criar material. Verifique os dados.');
    }
  };

  const logout = () => {
    // Limpar dados de autenticação
    localStorage.removeItem('authToken');  // Ou qualquer outro armazenamento utilizado
    
    // Redirecionar para a tela de login
    window.location.href = '/'; // Altere para a rota da sua página de login
  };

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Dashboard Técnico</h2>

      {/* Botão de Logout */}
      <div className="logout-button">
        <button className="button-primary" onClick={logout}>
          Sair
        </button>
      </div>

      {/* Criar Material */}
      <div className="card">
        <h3>Criar Novo Material</h3>
        <div className="input-group">
          <label>Nome:</label>
          <input
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            placeholder="Insira o nome do material"
          />
        </div>
        <div className="input-group">
          <label>Tipo:</label>
          <input
            value={tipo}
            onChange={(e) => setTipo(e.target.value)}
            placeholder="Insira o tipo do material"
          />
        </div>
        <div className="input-group">
          <label>Data de Validade:</label>
          <input
            value={dataValidade}
            onChange={(e) => setDataValidade(e.target.value)}
            type="date"
          />
        </div>
        <button onClick={criarMaterial} className="button-primary">Criar Material</button>
      </div>

      {/* Registrar Etapa */}
      <div className="card">
        <h3>Registrar Nova Etapa</h3>
        <div className="input-group">
          <label>Serial do Material:</label>
          <input
            value={serial}
            onChange={(e) => setSerial(e.target.value)}
            placeholder="Insira o serial"
          />
        </div>
        <div className="input-group">
          <label>Etapa:</label>
          <select
            value={etapa}
            onChange={(e) => setEtapa(e.target.value)}
          >
            <option value="">Selecione</option>
            <option value="recebimento">Recebimento</option>
            <option value="lavagem">Lavagem</option>
            <option value="esterilizacao">Esterilização</option>
            <option value="distribuicao">Distribuição</option>
          </select>
        </div>
        <div className="input-group">
          <label>Observação:</label>
          <input
            value={observacao}
            onChange={(e) => setObservacao(e.target.value)}
            placeholder="Observações"
          />
        </div>
        <button onClick={registrarEtapa} className="button-primary">Registrar Etapa</button>
      </div>

      {/* Consulta Etapas */}
      <div className="card">
        <h3>Consultar Etapas Realizadas</h3>
        <div className="input-group">
          <label>Serial do Material:</label>
          <input
            value={serialConsulta}
            onChange={(e) => setSerialConsulta(e.target.value)}
            placeholder="Digite o serial para consulta"
          />
        </div>
        <button onClick={buscarEtapasDoMaterial} className="button-primary">Buscar Etapas</button>

        {etapasRealizadas.length > 0 && (
          <div className="etapas-list">
            <h4>Histórico de Etapas para: {serialConsulta}</h4>
            <div className="scrollable"> {/* Aqui está a modificação */}
              {etapasRealizadas.map((proc, index) => (
                <div key={proc.procedimento_id || index} className="etapas-item">
                  <h5>Procedimento #{proc.procedimento_id}</h5>
                  <p><strong>Iniciado em:</strong> {formatarData(proc.data_inicio)}</p>
                  <ul>
                    {proc.etapas.map((etapa, idx) => (
                      <li key={idx}>
                        <strong>Etapa:</strong> {etapa.etapa} <br />
                        <strong>Status:</strong> {etapa.status} <br />
                        <strong>Data:</strong> {formatarData(etapa.data_realizacao)}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Status Atual */}
      <div className="card">
        <h3>Status Atual do Material</h3>
        <p>Status: {statusAtual || 'Nenhuma etapa registrada ainda'}</p>
      </div>

      {/* Histórico de Etapas */}
      <div className="card">
        <h3>Histórico de Etapas</h3>
        <ul>
          {Object.entries(historicoEtapas).map(([etapa, count]) => (
            <li key={etapa}>
              {etapa}: {count} vez(es)
            </li>
          ))}
        </ul>
      </div>

      {/* Lista de Materiais */}
      <div className="card">
        <h3>Materiais Cadastrados</h3>
        <ul>
          {materiais.map((mat) => (
            <li key={mat.id}>
              {mat.serial} - {mat.nome}
            </li>
          ))}
        </ul>
      </div>

      {/* Mensagem */}
      {mensagem && <p className="mensagem">{mensagem}</p>}
    </div>
  );
}
