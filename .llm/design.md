# Design — Referência Visual

Base: `picture/pagina.png` (simulador ge.globo — Copa 2026).

> **Importante:** usamos o **layout e a estética** da referência. O bolão **não** simula placares — apenas seleção de 1º e 2º colocado por grupo.

## Direção visual

Inspirado no portal esportivo brasileiro: limpo, denso em dados, verde como cor de ação, amarelo no topo.

| Elemento | Referência ge | Adaptação no bolão |
|----------|---------------|-------------------|
| Header | Faixa amarela + título | Título "Bolão Copa do Mundo 2026" |
| Tabs | Fase de grupos / Mata-mata | **Só fase de grupos** (escopo do PRD) |
| Grid de grupos | 12 grupos em colunas | Mesmo grid: 3 colunas desktop, 1 coluna mobile |
| Card de grupo | Tabela + times com bandeira | Card com nome do grupo + 2 selectboxes (1º, 2º) |
| Botões | Verde primário | "Participar" / "Confirmar aposta" |
| Feed de notícias | Lista abaixo | **Não incluir** (fora do escopo) |

## Paleta sugerida

```css
--header-bg:    #FFD700;   /* amarelo header */
--primary:      #00843D;   /* verde ação (estilo ge) */
--bg:           #F5F5F5;
--card-bg:      #FFFFFF;
--border:       #E0E0E0;
--text:         #1A1A1A;
--text-muted:   #666666;
--error:        #D32F2F;
--success:      #2E7D32;
```

## Layout da página principal

```
┌──────────────────────────────────────────────────────┐
│  HEADER — Bolão Copa do Mundo 2026                   │
├──────────────────────────────────────────────────────┤
│  Seus dados: [Nome] [Telefone] [E-mail]              │
├──────────────────────────────────────────────────────┤
│  GRUPO A    │  GRUPO B    │  GRUPO C                 │
│  1º [▼]     │  1º [▼]     │  1º [▼]                  │
│  2º [▼]     │  2º [▼]     │  2º [▼]                  │
├─────────────┼─────────────┼──────────────────────────┤
│  GRUPO D    │  ...        │  ...                     │
│  ...        │             │                          │
├──────────────────────────────────────────────────────┤
│              [ Revisar aposta ]  [ Participar ]      │
└──────────────────────────────────────────────────────┘
```

## Componentes Streamlit

| Componente | Widget | Notas |
|------------|--------|-------|
| Dados pessoais | `st.text_input` | 3 campos em `st.columns(3)` |
| Card de grupo | `st.container` + CSS | Borda, padding, título "Grupo X" |
| Seleção 1º/2º | `st.selectbox` | Opções = times do grupo |
| Resumo | `st.expander` ou modal | Lista 12 grupos antes de confirmar |
| Feedback | `st.success` / `st.error` | Validação inline |
| Admin (opcional) | `st.dataframe` | Listagem de participantes |

## Responsividade

- **Desktop (≥1024px):** 3 colunas de grupos (`st.columns(3)`)
- **Tablet (768–1023px):** 2 colunas
- **Mobile (<768px):** 1 coluna, campos empilhados

Usar skill `frontend-design` para refinar tipografia e detalhes visuais.
Usar skill `developing-with-streamlit` para CSS customizado e layout.

## Validação visual

- Grupo incompleto: borda vermelha no card
- Grupo completo: borda verde sutil
- Botão "Participar" desabilitado até todos os grupos + dados preenchidos

## Assets

- Bandeiras: emoji de bandeira por país (ex.: 🇧🇷) — simples, sem CDN externo na v1
- Logo: texto estilizado no header (sem logo ge — projeto independente)
