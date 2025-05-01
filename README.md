Sistema de Gerenciamento de Processos de CME
Este projeto é uma aplicação web desenvolvida para gerenciar os processos essenciais de uma Central de Material e Esterilização (CME) em um ambiente hospitalar. A aplicação é composta por um backend em Python (usando Django e Django REST Framework), um frontend em React, e um banco de dados PostgreSQL. Todos os componentes são executados dentro de containers Docker, utilizando Docker Compose para facilitar o desenvolvimento e implantação.

Funcionalidades
1. Cadastro de Usuários
A aplicação permite o cadastro e gerenciamento de usuários com três papéis distintos:

Usuário Técnico: Responsável por realizar as etapas do processo de esterilização.

Usuário Enfermagem: Responsável por verificar a rastreabilidade dos processos, consultar falhas e gerar relatórios.

Usuário Administrativo: Responsável por cadastrar novos usuários e atribuir funções.

2. Cadastro de Materiais
Os materiais a serem esterilizados são cadastrados com as seguintes informações:

Nome do material

Tipo do material

Data de validade

Serial (gerado automaticamente com base no nome do material)

3. Processo de Esterilização
Os materiais passam por 4 etapas:

Recebimento: Recebimento dos materiais dos diversos setores do hospital.

Lavagem: Lavagem dos materiais.

Esterilização: Esterilização dos materiais com alta temperatura.

Distribuição: Distribuição dos materiais esterilizados para os setores do hospital.

Após a finalização de todas as etapas, o material pode passar novamente por todo o processo.

4. Rastreabilidade
Visualize as etapas que um material passou, filtrando por serial ou visualizando todos os materiais.

Visualize as falhas ocorridas durante o processo de esterilização.

Gere relatórios em PDF ou XLSX de todos os materiais que passaram por todos os processos, assim como falhas associadas.

Tecnologias Utilizadas
Backend: Python, Django, Django REST Framework

Frontend: React

Banco de Dados: PostgreSQL

Docker: Docker Compose para containerização de todos os serviços

Como Iniciar o Projeto

Configuração do Banco de Dados

Abra o arquivo backend/cme_project/settings.py e localize a configuração do banco de dados. Altere a configuração para usar o PostgreSQL, conforme o padrão:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cme_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',  # Nome do serviço do banco no Docker Compose ou local
        'PORT': '5432',
    }
}

Criação do Ambiente Virtual

Na raiz do projeto (onde está localizado o arquivo manage.py), crie um ambiente virtual para o backend:

python -m venv venv
Ativando o Ambiente Virtual

Para ativar o ambiente virtual, use o seguinte comando:

No Windows:
venv\Scripts\activate

No Linux/Mac:
source venv/bin/activate

Instalação das Dependências
Com o ambiente virtual ativado, instale as dependências do projeto:

pip install -r backend/requirements.txt

Executando as Migrações do Banco de Dados
Execute as migrações para configurar o banco de dados:
python backend/manage.py migrate

Criando um Superusuário

Crie um superusuário para poder acessar o painel de administração do Django:

python backend/manage.py createsuperuser

Exemplo de superusuário:
Username: admin
Password: 123

Iniciando o Backend

Inicie o servidor backend com o seguinte comando:

python backend/manage.py runserver
O backend estará disponível em http://localhost:8000. Acesse o painel de administração do Django em http://localhost:8000/admin e faça login com o superusuário que você acabou de criar.

Alterando o Papel do Superusuário
No painel de administração, vá até a seção "Users".
Clique no usuário "admin" que você criou.
Modifique o campo Role para "administrativo", para que ele tenha permissão para acessar o frontend e realizar todas as ações administrativas.

Salve as alterações.

2. Configuração do Frontend
Instalação das Dependências do Frontend

Navegue até a pasta do frontend e instale as dependências do Node.js:
cd frontend
npm install
Iniciando o Frontend

Agora, inicie o servidor de desenvolvimento do React:
npm run dev

O frontend estará disponível em http://localhost:3000.

3. Testando a Aplicação

Login como Admin
Acesse o frontend em http://localhost:3000 e faça login com o superusuário (admin) criado no painel de administração.

Username: admin

Password: 123

Ao fazer login, você será redirecionado para o dashboard do admin, onde poderá criar novos usuários com as funções Técnico e Enfermagem.

Criando Usuários (Técnico e Enfermagem)

No dashboard do admin, você poderá:

Criar novos usuários com as funções Técnico e Enfermagem.

Modificar o papel de outros usuários, atribuindo o papel correto a eles.

Testando a Funcionalidade dos Usuários

Após criar o usuário Técnico e o usuário Enfermagem, faça login como cada um desses usuários no frontend.

Usuário Técnico: O técnico terá acesso ao processo de esterilização, realizando as etapas de Recebimento, Lavagem, Esterilização e Distribuição.

Usuário Enfermagem: O enfermeiro poderá visualizar a rastreabilidade dos materiais e gerar relatórios, além de consultar falhas nos processos.

Testando o Redirecionamento de Dashboards

Cada tipo de usuário será redirecionado para o seu respectivo dashboard após o login:

O admin será redirecionado para o dashboard administrativo.

O técnico será redirecionado para o dashboard técnico.
Assim entrar no técnico podera criar os materias para passar pelas etapas segue o exemplo abaixo
{
  "nome": "Faca",
  "tipo": "Cirúrgico",
  "data_validade": "2025-12-31"
}

User o serial que será gerado automaticamente ex: SERIAL-ECA4095C-PIN
para fazer as etapas que tem no deshboard do tecnico.

O enfermagem será redirecionado para o dashboard de rastreabilidade.

Bibliotecas adicionais: pandas para manipulação de dados, reportlab para geração de PDFs
