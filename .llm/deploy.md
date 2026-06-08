# Deploy — Streamlit Community Cloud

Guia rápido para publicar o Bolão Copa 2026.

## Checklist antes do deploy

- [ ] Código no GitHub (branch `main`)
- [ ] `app.py` na raiz do repositório
- [ ] `requirements.txt` na raiz
- [ ] `.streamlit/config.toml` commitado
- [ ] `data/` no `.gitignore` (banco criado em runtime)

## Configuração no Streamlit Cloud

| Campo | Valor |
|-------|-------|
| Repository | `seu-usuario/BolaoCopa` |
| Branch | `main` |
| Main file path | `app.py` |
| Python version | 3.11 (padrão do Cloud) |

Não é necessário `packages.txt` nem secrets para a versão atual.

## Após o deploy

A URL será algo como:

```
https://bolao-copa.streamlit.app
```

(você escolhe o subdomínio ao criar o app)

## Persistência

SQLite em `data/bolao.db` funciona no Cloud, mas o disco é **ephemeral**. Dados podem sumir em:

- Novo deploy (push no GitHub)
- Reinício do container por inatividade

Para bolão educacional isso é aceitável. Para persistência real, migrar para Supabase/PostgreSQL depois.

## Comandos locais (testar antes de subir)

```bash
pip install -r requirements.txt
streamlit run app.py
```
