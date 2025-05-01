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

Bibliotecas adicionais: pandas para manipulação de dados, reportlab para geração de PDFs
