# Arquitetura — Bolão Copa 2026

Projeto educacional com arquitetura **simples e monolítica**. Sem API separada, sem autenticação complexa, sem filas ou microserviços.

## Visão geral

```
┌─────────────────────────────────────────┐
│           Navegador (cliente)           │
└──────────────────┬──────────────────────┘
                   │ HTTP
┌──────────────────▼──────────────────────┐
│  app.py (Streamlit — UI + lógica)       │
│    ├── pages/ ou seções com st.tabs     │
│    ├── components/ (opcional, se crescer)│
│    └── database.py (SQLite CRUD)        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  data/bolao.db (SQLite)                 │
└─────────────────────────────────────────┘
```

## Estrutura de pastas

```
BolaoCopa/
├── app.py                 # Entry point Streamlit
├── database.py            # Conexão, migrations, CRUD
├── data/
│   └── bolao.db           # Banco (gitignore)
├── groups.py              # Dados estáticos: grupos A–L e times
├── requirements.txt
├── README.md
├── picture/
│   └── pagina.png         # Referência visual
├── .llm/                  # Documentação do projeto
└── .cursor/
    ├── rules/             # Regras para o agente
    └── skills/            # Skills Streamlit + frontend
```

## Módulos e responsabilidades

| Módulo | Responsabilidade |
|--------|------------------|
| `app.py` | Páginas, formulários, validação na UI, fluxo do usuário |
| `groups.py` | Lista dos 12 grupos com 4 seleções cada (dados estáticos) |
| `database.py` | Criar tabelas, inserir participante, inserir apostas, consultar |

## Banco de dados (SQLite)

### Tabela `participantes`

| Coluna | Tipo | Observação |
|--------|------|------------|
| id | INTEGER PK | autoincrement |
| nome | TEXT | obrigatório |
| telefone | TEXT | obrigatório |
| email | TEXT | único, obrigatório |
| criado_em | TEXT | ISO datetime |

### Tabela `apostas`

| Coluna | Tipo | Observação |
|--------|------|------------|
| id | INTEGER PK | autoincrement |
| participante_id | INTEGER FK | → participantes.id |
| grupo | TEXT | A, B, … L |
| primeiro | TEXT | nome do time |
| segundo | TEXT | nome do time |

## Fluxo do usuário

```
1. Abrir app no navegador
2. Preencher nome, telefone, e-mail
3. Para cada grupo (A–L): escolher 1º e 2º colocado
4. Revisar resumo
5. Confirmar → salvar no SQLite
6. Ver mensagem de sucesso
```

## Regras de negócio

- Cada grupo tem exatamente 4 times
- Usuário escolhe **apenas** 1º e 2º (não simula placares)
- 1º e 2º devem ser times **diferentes** no mesmo grupo
- Todos os 12 grupos são obrigatórios
- E-mail não pode se repetir (1 participação por e-mail)

## O que NÃO fazer (escopo reduzido)

- Simulador de placares / mata-mata (referência visual apenas)
- Login/senha ou OAuth
- Backend REST separado do Streamlit
- ORM pesado (SQLAlchemy) — SQL direto com `sqlite3` basta
- Deploy complexo na v1 — local + Streamlit Cloud opcional depois

## Stack

| Camada | Tecnologia |
|--------|------------|
| App web | Streamlit ≥ 1.57 |
| Linguagem | Python 3.11+ |
| Banco | SQLite (stdlib) |
| Estilo | CSS customizado via `st.markdown(unsafe_allow_html=True)` |
