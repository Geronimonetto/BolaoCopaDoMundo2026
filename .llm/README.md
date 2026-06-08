# Documentação do Projeto — Bolão Copa 2026

App web educacional em Python + Streamlit. O participante escolhe 1º e 2º de cada grupo (A–L), informa nome/telefone/e-mail e a aposta é salva em SQLite.

## Documentos

| Arquivo | Conteúdo |
|---------|----------|
| [prd.md](./prd.md) | Requisitos de produto (fonte da verdade) |
| [architecture.md](./architecture.md) | Arquitetura simples e estrutura de pastas |
| [design.md](./design.md) | Referência visual baseada em `picture/pagina.png` |
| [stories.md](./stories.md) | User stories e critérios de aceite |
| [implementation-plan.md](./implementation-plan.md) | Plano de desenvolvimento por fases |
| [deploy.md](./deploy.md) | Deploy no Streamlit Community Cloud |

## Skills do projeto (`.cursor/skills/`)

| Skill | Quando usar |
|-------|-------------|
| `developing-with-streamlit` | Toda implementação Streamlit: layout, widgets, session state, CSS, deploy |
| `frontend-design` | Decisões visuais: cores, tipografia, grid de grupos, polish da UI |

## Como desenvolver

1. Ler `prd.md` e a story da fase atual em `stories.md`
2. Consultar `design.md` antes de mexer na UI
3. Seguir `implementation-plan.md` na ordem das fases
4. Ativar a skill correspondente em `.cursor/skills/` durante a implementação

## Comando para rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Acesso: `http://localhost:8501`
