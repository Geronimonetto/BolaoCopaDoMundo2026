import re

import streamlit as st

from bracket import (
    campeao,
    grupos_completos,
    limpar_picks_invalidos,
    mata_mata_completo,
    montar_chaveamento,
)
from database import email_existe, init_db, listar_apostas, listar_participantes, salvar_participacao
from groups import GRUPOS, flag_url, get_team

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

if "picks" not in st.session_state:
    st.session_state.picks = {}
if "passo" not in st.session_state:
    st.session_state.passo = 1
for _g in GRUPOS:
    if f"sel_{_g}" not in st.session_state:
        st.session_state[f"sel_{_g}"] = {"primeiro": None, "segundo": None}


def selecoes() -> dict[str, dict]:
    return {g: st.session_state[f"sel_{g}"] for g in GRUPOS}


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root{
  --ink:#0a1f17; --gold:#F2C84B; --grass:#0FA968;
  --grass-dk:#0A7D4E; --line:rgba(255,255,255,.12);
  --txt:#EAF2EC; --txt-mut:#9fb4a8;
}
html,body,[class*="css"]{ font-family:'Inter',sans-serif; }
.stApp{
  background:
    radial-gradient(1200px 600px at 15% -10%, rgba(15,169,104,.30), transparent 60%),
    radial-gradient(900px 500px at 110% 10%, rgba(242,200,75,.20), transparent 55%),
    linear-gradient(170deg,#06140e 0%,#0a2117 45%,#0b2a1c 100%);
}
.block-container{ padding-top:1rem; max-width:1280px; }
#MainMenu, footer, header[data-testid="stHeader"]{ visibility:hidden; }

/* texto padrão claro no fundo escuro */
.stApp, .stMarkdown, .stMarkdown p, label, .stTextInput label, .stCaption,
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p{ color:var(--txt) !important; }

/* ---------- HERO ---------- */
.hero{
  position:relative; overflow:hidden; border-radius:22px; padding:2rem 2.2rem;
  margin-bottom:1.1rem;
  background:linear-gradient(120deg,#0FA968 0%,#0A7D4E 55%,#075c3a 100%);
  box-shadow:0 18px 50px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.12);
}
.hero::after{
  content:""; position:absolute; inset:0;
  background:repeating-linear-gradient(90deg,transparent 0 78px,rgba(255,255,255,.05) 78px 80px);
  pointer-events:none;
}
.hero h1{
  font-family:'Archivo',sans-serif; font-weight:800; letter-spacing:-.02em;
  font-size:2.5rem; line-height:1; margin:0; color:#fff;
  text-shadow:0 2px 12px rgba(0,0,0,.25);
}
.hero .tag{
  display:inline-block; background:rgba(0,0,0,.25); color:var(--gold);
  font-weight:700; font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
  padding:.35rem .8rem; border-radius:999px; margin-bottom:.8rem; border:1px solid rgba(242,200,75,.35);
}
.hero p{ margin:.5rem 0 0; color:rgba(255,255,255,.9); font-size:1.02rem; max-width:640px; }

/* ---------- STEPS ---------- */
.steps{ display:flex; gap:.6rem; margin:0 0 1.1rem; }
.step{
  flex:1; display:flex; align-items:center; gap:.6rem; padding:.7rem 1rem; border-radius:14px;
  background:rgba(255,255,255,.05); border:1px solid var(--line); color:rgba(255,255,255,.55);
  font-weight:600; font-size:.9rem;
}
.step .n{
  width:26px;height:26px;border-radius:50%;display:grid;place-items:center;
  background:rgba(255,255,255,.1); font-size:.8rem; font-weight:800; flex:none;
}
.step.active{ background:rgba(242,200,75,.14); border-color:rgba(242,200,75,.5); color:var(--gold); }
.step.active .n{ background:var(--gold); color:#3a2d00; }
.step.done{ background:rgba(15,169,104,.18); border-color:rgba(15,169,104,.5); color:#7ee2b0; }
.step.done .n{ background:var(--grass); color:#04130c; }

/* ---------- PANEL ---------- */
.panel{
  background:rgba(255,255,255,.06); border-radius:20px; padding:1.3rem 1.2rem;
  margin-bottom:1rem; box-shadow:0 10px 30px rgba(0,0,0,.30); border:1px solid var(--line);
  backdrop-filter:blur(6px);
}
.panel-title{ font-family:'Archivo',sans-serif; font-weight:700; color:#fff; font-size:1.25rem; margin:0 0 .2rem; }
.panel-sub{ color:var(--txt-mut); font-size:.85rem; margin:0 0 1rem; }

/* ---------- GROUP CARD ---------- */
.gcard{
  background:rgba(255,255,255,.05); border:1px solid var(--line); border-radius:16px;
  padding:.85rem .8rem .7rem; margin-bottom:.7rem; transition:.18s;
}
.gcard.ok{ border-color:var(--grass); box-shadow:inset 0 0 0 1px rgba(15,169,104,.35); background:rgba(15,169,104,.12); }
.gtag{
  display:inline-flex; align-items:center; gap:.4rem; background:var(--grass); color:#04130c;
  font-family:'Archivo',sans-serif; font-weight:700; font-size:.74rem; letter-spacing:.1em;
  padding:.22rem .6rem; border-radius:8px; margin-bottom:.55rem;
}
.gres{ font-size:.78rem; color:var(--txt-mut); margin-top:.5rem; display:flex; gap:.8rem; }
.gres b{ color:#fff; }

/* ---------- TEAM TILE ---------- */
.tile{ text-align:center; border-radius:13px; border:2px solid #e3e9e6; background:#fff; padding:.45rem .3rem .25rem; position:relative; }
.tile.t1{ border-color:var(--gold); background:linear-gradient(180deg,#FFFaE9,#fff); }
.tile.t2{ border-color:#9fb2c9; background:linear-gradient(180deg,#eef3f8,#fff); }
.mk{ position:absolute; top:-9px; left:50%; transform:translateX(-50%); font-size:.6rem; font-weight:800; padding:.06rem .4rem; border-radius:999px; box-shadow:0 2px 6px rgba(0,0,0,.15); }
.mk.m1{ background:var(--gold); color:#5a4500; }
.mk.m2{ background:#9fb2c9; color:#1e2b3a; }

/* small buttons inside grid columns */
div[data-testid="column"] .stButton>button{
  font-size:.72rem; font-weight:600; border-radius:9px; min-height:2.05rem; line-height:1.12;
  white-space:normal; border:1px solid #dde3e0; background:#fff; color:#1d2a24;
}
div[data-testid="column"] .stButton>button:hover{ border-color:var(--grass); color:var(--grass-dk); }

/* ---------- BRACKET ---------- */
.round-head{
  font-family:'Archivo',sans-serif; font-weight:700; color:#fff; font-size:1rem;
  display:flex; align-items:center; gap:.5rem; margin:.2rem 0 .6rem;
}
.round-pill{ background:var(--grass); color:#04130c; font-size:.66rem; font-weight:700; padding:.15rem .5rem; border-radius:999px; }
.round-head.live .round-pill{ background:var(--gold); color:#3a2d00; }
.match{
  background:rgba(255,255,255,.05); border:1px solid var(--line); border-radius:14px; padding:.7rem .7rem .5rem; margin-bottom:.6rem;
}
.match .winner-name{ color:#fff; font-weight:700; }
.bye{
  display:inline-flex; align-items:center; gap:.4rem; background:rgba(23,99,182,.18); color:#9cc4ef;
  border:1px dashed #4d7fb5; padding:.35rem .7rem; border-radius:10px; font-size:.78rem; font-weight:600; margin-bottom:.5rem;
}
.vs{ text-align:center; color:var(--txt-mut); font-weight:800; font-size:.8rem; padding-top:1.6rem; }
.champion{
  margin-top:.8rem; border-radius:18px; padding:1.4rem; text-align:center; color:#3a2d00;
  background:linear-gradient(135deg,#FFE38A,#F2C84B 45%,#E1A21f);
  box-shadow:0 12px 30px rgba(242,200,75,.35); border:1px solid rgba(255,255,255,.4);
}
.champion .lbl{ font-size:.78rem; font-weight:700; letter-spacing:.2em; text-transform:uppercase; opacity:.7; }
.champion .nm{ font-family:'Archivo',sans-serif; font-weight:800; font-size:1.8rem; line-height:1.1; margin-top:.2rem; }

.match .winner .stButton>button{ background:var(--grass)!important; color:#fff!important; border-color:var(--grass-dk)!important; }

/* primary buttons */
.stButton>button[kind="primary"]{
  background:linear-gradient(90deg,#0FA968,#13c47c)!important; border:none!important;
  font-weight:700; border-radius:12px; min-height:2.7rem; box-shadow:0 8px 20px rgba(15,169,104,.35);
}
.stButton>button[kind="primary"]:hover{ filter:brightness(1.05); }

/* inputs */
.stTextInput input{ border-radius:10px; }
.stTabs [data-baseweb="tab-list"]{ gap:.4rem; }
.stTabs [data-baseweb="tab"]{ background:rgba(255,255,255,.06); border-radius:10px 10px 0 0; color:#cfe; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------- validações
def validar_email(email: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email.strip()))


def validar_telefone(telefone: str) -> bool:
    return len(re.sub(r"\D", "", telefone)) >= 10


# ---------------------------------------------------------------- grupos
def slot_time(grupo: str, nome: str) -> int | None:
    sel = st.session_state[f"sel_{grupo}"]
    if sel["primeiro"] == nome:
        return 1
    if sel["segundo"] == nome:
        return 2
    return None


def clicar_time(grupo: str, nome: str) -> None:
    sel = st.session_state[f"sel_{grupo}"]
    if sel["primeiro"] == nome:
        sel["primeiro"], sel["segundo"] = sel["segundo"], None
    elif sel["segundo"] == nome:
        sel["segundo"] = None
    elif sel["primeiro"] is None:
        sel["primeiro"] = nome
    elif sel["segundo"] is None:
        sel["segundo"] = nome
    else:
        sel["segundo"] = nome
    st.session_state.picks = {}


def coletar_apostas() -> tuple[list[dict[str, str]], list[str]]:
    apostas, erros = [], []
    for grupo in GRUPOS:
        sel = st.session_state[f"sel_{grupo}"]
        if not sel["primeiro"]:
            erros.append(f"Grupo {grupo}: escolha o 1º colocado.")
        elif not sel["segundo"]:
            erros.append(f"Grupo {grupo}: escolha o 2º colocado.")
        else:
            apostas.append({"grupo": grupo, "primeiro": sel["primeiro"], "segundo": sel["segundo"]})
    return apostas, erros


# ---------------------------------------------------------------- mata-mata
def escolher_vencedor(key: str, nome: str) -> None:
    st.session_state.picks[key] = nome
    limpar_picks_invalidos(selecoes(), st.session_state.picks)


# ---------------------------------------------------------------- UI peças
def render_steps() -> None:
    sels = selecoes()
    g_ok = grupos_completos(sels)
    m_ok = mata_mata_completo(sels, st.session_state.picks)
    p = st.session_state.passo

    def cls(done, n):
        return "done" if done else ("active" if p == n else "")

    st.markdown(
        f"""
        <div class="steps">
          <div class="step {cls(g_ok,1)}"><span class="n">1</span> Fase de grupos</div>
          <div class="step {cls(m_ok,2)}"><span class="n">2</span> Mata-mata</div>
          <div class="step {cls(False,3)}"><span class="n">3</span> Confirmar</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tile(grupo: str, time: dict[str, str]) -> None:
    nome = time["nome"]
    slot = slot_time(grupo, nome)
    cls = f"tile t{slot}" if slot else "tile"
    mk = '<span class="mk m1">1º</span>' if slot == 1 else ('<span class="mk m2">2º</span>' if slot == 2 else "")
    st.markdown(f'<div class="{cls}">{mk}', unsafe_allow_html=True)
    st.image(flag_url(time["codigo"]), width=46)
    st.button(nome, key=f"btn_{grupo}_{time['codigo']}", on_click=clicar_time,
              args=(grupo, nome), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_grupo(grupo: str) -> None:
    sel = st.session_state[f"sel_{grupo}"]
    ok = sel["primeiro"] and sel["segundo"]
    st.markdown(f'<div class="gcard {"ok" if ok else ""}">', unsafe_allow_html=True)
    st.markdown(f'<span class="gtag">⚽ GRUPO {grupo}</span>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, time in zip(cols, GRUPOS[grupo], strict=True):
        with col:
            render_tile(grupo, time)
    st.markdown(
        f'<div class="gres"><span>🥇 <b>{sel["primeiro"] or "—"}</b></span>'
        f'<span>🥈 <b>{sel["segundo"] or "—"}</b></span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_match(jogo: dict, editavel: bool) -> None:
    key = jogo["key"]
    venc = st.session_state.picks.get(key)
    st.markdown('<div class="match">', unsafe_allow_html=True)
    c1, mid, c2 = st.columns([6, 1, 6])
    for col, nome, side in ((c1, jogo["a"], "a"), (c2, jogo["b"], "b")):
        with col:
            team = get_team(nome)
            if team:
                st.image(flag_url(team["codigo"]), width=38)
            wrap = "winner" if venc == nome else ""
            st.markdown(f'<div class="{wrap}">', unsafe_allow_html=True)
            if editavel:
                st.button(nome, key=f"win_{key}_{side}", on_click=escolher_vencedor,
                          args=(key, nome), use_container_width=True,
                          type="primary" if venc == nome else "secondary")
            else:
                st.markdown(f"**{nome}**" + (" 🏆" if venc == nome else ""))
            st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        st.markdown('<div class="vs">VS</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_mata_mata() -> None:
    sels = selecoes()
    chave = montar_chaveamento(sels, st.session_state.picks)
    if not chave:
        st.warning("Complete a fase de grupos primeiro.")
        return

    atual_idx = next(
        (i for i, r in enumerate(chave) if any(not j.get("vencedor") for j in r["jogos"])),
        None,
    )
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🏆 Mata-mata até a final</div>', unsafe_allow_html=True)
    st.markdown('<p class="panel-sub">Clique no vencedor de cada jogo. A próxima rodada abre automaticamente.</p>', unsafe_allow_html=True)

    for i, rodada in enumerate(chave):
        completa = all(j.get("vencedor") for j in rodada["jogos"])
        is_atual = i == atual_idx
        live = " live" if is_atual else ""
        pill = "JOGANDO" if is_atual else ("OK" if completa else "")
        st.markdown(
            f'<div class="round-head{live}">{rodada["nome"]}'
            + (f'<span class="round-pill">{pill}</span>' if pill else "")
            + "</div>",
            unsafe_allow_html=True,
        )
        for bye in rodada.get("byes", []):
            st.markdown(f'<div class="bye">⏩ {bye} passa direto</div>', unsafe_allow_html=True)
        for jogo in rodada["jogos"]:
            render_match(jogo, editavel=is_atual)

    camp = campeao(st.session_state.picks, sels)
    if camp:
        team = get_team(camp)
        flag = f'<br><img src="{flag_url(team["codigo"])}" width="56" style="margin-top:.5rem;border-radius:4px">' if team else ""
        st.markdown(
            f'<div class="champion"><div class="lbl">Campeão do mundo</div>'
            f'<div class="nm">{camp}</div>{flag}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------- páginas
def render_dados() -> tuple[str, str, str]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">👤 Seus dados</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    nome = c1.text_input("Nome completo *", key="input_nome")
    telefone = c2.text_input("Telefone *", key="input_telefone")
    email = c3.text_input("E-mail *", key="input_email")
    st.markdown("</div>", unsafe_allow_html=True)
    return nome, telefone, email


def render_bolao() -> None:
    st.markdown(
        """
        <div class="hero">
          <span class="tag">Estados Unidos · Canadá · México</span>
          <h1>Bolão Copa do Mundo 2026</h1>
          <p>Monte a classificação dos 12 grupos e cravar o caminho do seu campeão até a final.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_steps()
    nome, telefone, email = render_dados()

    if st.session_state.passo == 1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">① Fase de grupos</div>', unsafe_allow_html=True)
        st.markdown('<p class="panel-sub">1º toque = 🥇 ouro (1º lugar) · 2º toque = 🥈 prata (2º lugar) · toque de novo para desmarcar.</p>', unsafe_allow_html=True)
        grupos = list(GRUPOS.keys())
        for i in range(0, len(grupos), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(grupos):
                    with col:
                        render_grupo(grupos[i + j])
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Ir para o mata-mata →", type="primary", use_container_width=True):
            _, erros = coletar_apostas()
            if erros:
                st.error("Complete todos os grupos: " + erros[0])
            else:
                st.session_state.passo = 2
                st.rerun()

    elif st.session_state.passo == 2:
        render_mata_mata()
        c1, c2 = st.columns(2)
        if c1.button("← Voltar aos grupos", use_container_width=True):
            st.session_state.passo = 1
            st.rerun()
        if c2.button("Revisar e confirmar →", type="primary", use_container_width=True):
            if not mata_mata_completo(selecoes(), st.session_state.picks):
                st.error("Escolha o vencedor de todos os jogos até a final.")
            else:
                st.session_state.passo = 3
                st.rerun()

    elif st.session_state.passo == 3:
        render_confirmacao(nome, telefone, email)


def render_confirmacao(nome: str, telefone: str, email: str) -> None:
    sels = selecoes()
    camp = campeao(st.session_state.picks, sels)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">③ Revisão final</div>', unsafe_allow_html=True)
    if camp:
        st.markdown(f'<div class="champion"><div class="lbl">Seu campeão</div><div class="nm">🏆 {camp}</div></div>', unsafe_allow_html=True)
    st.write("")
    cols = st.columns(3)
    for idx, g in enumerate(GRUPOS):
        s = sels[g]
        with cols[idx % 3]:
            st.markdown(
                f'<div class="gcard ok"><span class="gtag">GRUPO {g}</span>'
                f'<div class="gres"><span>🥇 <b>{s["primeiro"]}</b></span>'
                f'<span>🥈 <b>{s["segundo"]}</b></span></div></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("← Editar mata-mata", use_container_width=True):
        st.session_state.passo = 2
        st.rerun()

    if c2.button("Enviar participação ✅", type="primary", use_container_width=True):
        erros = []
        if not nome.strip():
            erros.append("Informe seu nome.")
        if not validar_telefone(telefone):
            erros.append("Telefone inválido (mínimo 10 dígitos).")
        if not validar_email(email):
            erros.append("E-mail inválido.")
        apostas, erros_g = coletar_apostas()
        erros.extend(erros_g)
        if not mata_mata_completo(sels, st.session_state.picks):
            erros.append("Mata-mata incompleto.")

        if erros:
            for e in erros:
                st.error(e)
            return
        if email_existe(email):
            st.error("Este e-mail já participou do bolão.")
            return

        pid = salvar_participacao(nome, telefone, email, apostas,
                                  mata_mata=dict(st.session_state.picks), campeao=camp)
        st.balloons()
        st.success(f"Participação registrada, {nome.strip()}! Seu campeão: {camp}. (ID #{pid})")
        st.session_state.passo = 1
        st.session_state.picks = {}
        for g in GRUPOS:
            st.session_state[f"sel_{g}"] = {"primeiro": None, "segundo": None}


def render_admin() -> None:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📋 Participantes</div>', unsafe_allow_html=True)
    participantes = listar_participantes()
    if not participantes:
        st.info("Nenhum participante ainda.")
    else:
        st.dataframe(
            [{"Nome": p["nome"], "E-mail": p["email"], "Campeão": p.get("campeao") or "—", "Data": p["criado_em"][:10]} for p in participantes],
            use_container_width=True, hide_index=True,
        )
        for p in participantes:
            with st.expander(f"{p['nome']} — campeão: {p.get('campeao') or '—'}"):
                for a in listar_apostas(p["id"]):
                    st.write(f"Grupo {a['grupo']}: 🥇 {a['primeiro']} · 🥈 {a['segundo']}")
    st.markdown("</div>", unsafe_allow_html=True)


tab_bolao, tab_admin = st.tabs(["🎯 Bolão", "📋 Admin"])
with tab_bolao:
    render_bolao()
with tab_admin:
    render_admin()
