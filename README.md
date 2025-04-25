# InfraGuardian

🚀 Produto: InfraGuardian (nome provisório)
Diagnóstico inteligente e correção automatizada de performance e segurança para servidores Linux, containers e infraestrutura cloud/híbrida.

🎯 Proposta de Valor
Automatize a detecção e resolução de problemas de performance e segurança em servidores, containers e serviços com um agente leve e um painel central.
Tenha uma equipe sênior 24/7 monitorando, diagnosticando e corrigindo automaticamente falhas críticas.

🧩 Funcionalidades principais (MVP)
🔍 Módulo de Diagnóstico:
Coleta de métricas de CPU, RAM, I/O, disco, rede, containers

Verificação de anomalias com regras baseadas em heurísticas + IA leve (ex: regressões de comportamento)

Detecção de erros em logs (syslog, dmesg, docker logs etc.)

Verificação de configurações incorretas ou perigosas (ex: swap mal configurado, permissões abertas, etc.)

🛠️ Módulo de Correção Automatizada:
Scripts Ansible para corrigir problemas comuns

Integração com Vault para correção segura de configurações sensíveis

Correções propostas vs. Correções aplicadas (com modo “manual”, “semi-automático” e “auto”)

Playbooks prontos para performance tuning (ex: PostgreSQL, NGINX, Nomad, Docker)

🧠 Assistente de Performance (opcional no roadmap):
Chatbot (Typebot + Langflow) que responde “como resolver X” com base nos dados reais da sua infra

Sugestões de melhorias contínuas com histórico e comparativos

🛡️ Diferenciais
Baseado na experiência real de um sysadmin + DevOps sênior

Capacidade de rodar on-premises ou em edge (ex: Raspberry Pi monitorando localmente)

Correções seguras e auditáveis com integração a ferramentas como Vault e Nomad

Pronto para ambientes híbridos, containers e legados

Reduz necessidade de mão de obra altamente técnica em suporte de N2/N3

🔧 Tecnologias recomendadas para MVP
Backend: Python (API, diagnósticos), Ansible, Shell

Frontend: Next.js ou React + Tailwind (dashboard)

Monitoramento: Agente em Bash/Python (estilo telegraf), ou adaptação do Prometheus Node Exporter

Banco: SQLite (MVP) ou PostgreSQL (scalável)

IA: Regras heurísticas + integração opcional com modelos locais (Ollama) para sugestões


🚧 Roadmap de Evolução
MVP: Diagnóstico + Correções básicas automatizadas com Ansible

Integração com Vault e Nomad para ajustes seguros

Módulo de IA com chatbot para explicações e orientação técnica

Exportação de relatórios de auditoria e compliance

Integração com Git para versionar correções e histórico de alterações na infra


🏗️ Estrutura de Pastas

infraguardian/
│
├── agent/                   # Agente leve que roda no host monitorado
│   ├── collectors/          # Scripts para coletar métricas (CPU, RAM, logs, etc.)
│   ├── detectors/           # Heurísticas e checagens de anomalias
│   ├── fixers/              # Correções automatizadas (scripts Shell/Ansible)
│   └── main.py              # Entrada principal do agente

├── api/                     # Backend Python (FastAPI)
│   ├── models/              # Modelos de dados (pydantic)
│   ├── routers/             # Endpoints da API
│   ├── services/            # Lógica de negócios
│   ├── database/            # Configuração do banco (SQLite inicialmente)
│   └── main.py              # Inicialização do FastAPI

├── ui/                      # Frontend React (Next.js)
│   ├── components/          # Componentes reutilizáveis
│   ├── pages/               # Rotas do app (Next.js)
│   ├── services/            # Consumo da API
│   └── tailwind.config.js   # Configuração do Tailwind

├── ansible/                 # Playbooks usados para correção automática
│   ├── playbooks/           # Scripts reutilizáveis (ex: fixar swap, ajustar sysctl)
│   └── inventory/           # Hosts controlados via Ansible

├── vault/                   # Integração com Vault (mock inicialmente)
│   └── vault_helper.py      # Armazenamento e recuperação segura de secrets

├── docs/                    # Documentação, fluxogramas e specs
│
├── .env                     # Configurações do projeto
├── docker-compose.yml       # Para rodar local (API + UI)
├── requirements.txt         # Dependências do backend
└── README.md







✅ Como rodar localmente
Crie um ambiente virtual e instale dependências:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Sair: deactivate


Suba o backend:
'''
uvicorn api.main:app --reload
'''

Em outro terminal, execute o agente:
'''
python agent/main.py
'''


Você verá as métricas sendo enviadas e armazenadas em memória no backend.


PS.: 
- aconselhavel o uso de chave ssh sem autenticação apra laboratorios
- hosts ficam no inventário hosts.ini