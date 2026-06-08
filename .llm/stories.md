# User Stories — Bolão Copa 2026

Formato: **Como** [persona], **quero** [ação], **para** [benefício].

---

## Épico 1 — Setup do app web

### US-01 — Rodar o projeto localmente
**Como** desenvolvedor, **quero** subir o app com um comando, **para** testar no navegador.

**Critérios de aceite**
- [ ] `requirements.txt` com streamlit
- [ ] `streamlit run app.py` abre em `http://localhost:8501`
- [ ] README com instruções

### US-02 — Estrutura mínima de código
**Como** desenvolvedor, **quero** arquivos separados por responsabilidade, **para** manter o projeto simples e legível.

**Critérios de aceite**
- [ ] `app.py`, `database.py`, `groups.py` existem
- [ ] Pasta `data/` para o banco

---

## Épico 2 — Dados e persistência

### US-03 — Grupos da Copa 2026
**Como** sistema, **quero** ter os 12 grupos (A–L) com 4 times cada, **para** popular os selectboxes.

**Critérios de aceite**
- [ ] `groups.py` exporta dict/lista com todos os grupos
- [ ] Cada time tem `nome` e `bandeira` (emoji)

### US-04 — Salvar participação
**Como** participante, **quero** que minha aposta seja salva, **para** minha escolha ficar registrada.

**Critérios de aceite**
- [ ] Tabelas criadas automaticamente na 1ª execução
- [ ] Insert de participante + 12 linhas de aposta em transação
- [ ] Dados persistem após fechar o navegador

### US-05 — Bloquear e-mail duplicado
**Como** administrador, **quero** impedir o mesmo e-mail duas vezes, **para** evitar apostas duplicadas.

**Critérios de aceite**
- [ ] Verificação antes do insert
- [ ] Mensagem clara se e-mail já existe

---

## Épico 3 — Interface do bolão

### US-06 — Cadastro de dados pessoais
**Como** participante, **quero** informar nome, telefone e e-mail, **para** me identificar no bolão.

**Critérios de aceite**
- [ ] 3 campos obrigatórios no topo da página
- [ ] Validação de e-mail (@ e domínio)
- [ ] Telefone: apenas dígitos, mín. 10 caracteres

### US-07 — Selecionar 1º e 2º por grupo
**Como** participante, **quero** escolher 1º e 2º de cada grupo, **para** registrar minha aposta.

**Critérios de aceite**
- [ ] 12 cards de grupo visíveis
- [ ] 2 selectboxes por grupo (1º, 2º)
- [ ] Opções limitadas aos 4 times do grupo
- [ ] 1º ≠ 2º no mesmo grupo

### US-08 — Feedback de validação
**Como** participante, **quero** ver o que falta preencher, **para** completar minha aposta sem erro.

**Critérios de aceite**
- [ ] Grupos incompletos destacados
- [ ] Mensagem ao tentar enviar com campos vazios
- [ ] Botão bloqueado ou aviso enquanto incompleto

### US-09 — Layout inspirado na referência
**Como** participante, **quero** uma interface familiar de copa do mundo, **para** navegar com facilidade.

**Critérios de aceite**
- [ ] Header amarelo + título
- [ ] Grid de grupos em colunas
- [ ] Botão verde de ação
- [ ] Responsivo (mobile ok)

---

## Épico 4 — Confirmação e admin

### US-10 — Resumo antes de enviar
**Como** participante, **quero** revisar minhas escolhas, **para** confirmar antes de salvar.

**Critérios de aceite**
- [ ] Expander ou seção com 12 grupos + escolhas
- [ ] Dados pessoais visíveis no resumo
- [ ] Botão confirmar e voltar

### US-11 — Confirmação de sucesso
**Como** participante, **quero** ver confirmação após enviar, **para** saber que deu certo.

**Critérios de aceite**
- [ ] `st.success` com nome do participante
- [ ] Indicação 12/12 grupos
- [ ] Opção de nova participação (limpar form)

### US-12 — Ver participantes (admin)
**Como** administrador, **quero** listar quem participou, **para** acompanhar o bolão.

**Critérios de aceite**
- [ ] Aba ou sidebar "Admin"
- [ ] Tabela: nome, e-mail, telefone, data
- [ ] Expandir para ver apostas do participante

---

## Mapa story → arquivo

| Story | Arquivo principal |
|-------|-------------------|
| US-01, US-02 | `requirements.txt`, `README.md`, `app.py` |
| US-03 | `groups.py` |
| US-04, US-05 | `database.py` |
| US-06–US-09 | `app.py` + CSS |
| US-10–US-11 | `app.py` |
| US-12 | `app.py` (aba admin) |
