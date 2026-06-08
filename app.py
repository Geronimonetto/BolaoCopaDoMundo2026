import re

import streamlit as st

from database import email_existe, init_db, listar_apostas, listar_participantes, salvar_participacao
from groups import GRUPOS, opcoes_grupo

PLACEHOLDER = "Selecione..."

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

CSS = """
<style>
    .block-container { padding-top: 1rem; max-width: 1200px; }
    .header-banner {
        background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .header-banner h1 {
        margin: 0;
        color: #1A1A1A;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .header-banner p {
        margin: 0.3rem 0 0;
        color: #333;
        font-size: 0.95rem;
    }
    div[data-testid="stForm"] {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
        background: #FFFFFF;
    }
    .stButton > button[kind="primary"] {
        background-color: #00843D;
        border: none;
        font-weight: 600;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #006B32;
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def validar_email(email: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email.strip()))


def validar_telefone(telefone: str) -> bool:
    digitos = re.sub(r"\D", "", telefone)
    return len(digitos) >= 10


def validar_apostas(selecoes: dict[str, tuple[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    apostas: list[dict[str, str]] = []
    erros: list[str] = []

    for grupo in GRUPOS:
        primeiro, segundo = selecoes[grupo]
        if primeiro == PLACEHOLDER or segundo == PLACEHOLDER:
            erros.append(f"Grupo {grupo}: selecione 1º e 2º colocado.")
            continue
        if primeiro == segundo:
            erros.append(f"Grupo {grupo}: 1º e 2º não podem ser o mesmo time.")
            continue
        apostas.append({"grupo": grupo, "primeiro": primeiro, "segundo": segundo})

    return apostas, erros


def render_grupo(grupo: str) -> tuple[str, str]:
    opcoes = [PLACEHOLDER] + opcoes_grupo(grupo)
    st.markdown(f"**Grupo {grupo}**")
    primeiro = st.selectbox("1º colocado", opcoes, key=f"{grupo}_primeiro")
    segundo = st.selectbox("2º colocado", opcoes, key=f"{grupo}_segundo")
    return primeiro, segundo


def render_bolao() -> None:
    st.markdown(
        """
        <div class="header-banner">
            <h1>⚽ Bolão Copa do Mundo 2026</h1>
            <p>Escolha o 1º e 2º colocado de cada grupo e participe!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("form_bolao"):
        st.subheader("Seus dados")
        c1, c2, c3 = st.columns(3)
        nome = c1.text_input("Nome completo *")
        telefone = c2.text_input("Telefone *")
        email = c3.text_input("E-mail *")

        st.divider()
        st.subheader("Fase de grupos — 1º e 2º colocado")

        selecoes: dict[str, tuple[str, str]] = {}
        grupos = list(GRUPOS.keys())
        for i in range(0, len(grupos), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(grupos):
                    grupo = grupos[i + j]
                    with col:
                        with st.container(border=True):
                            selecoes[grupo] = render_grupo(grupo)

        st.divider()
        enviar = st.form_submit_button("Participar do bolão", type="primary", use_container_width=True)

    if enviar:
        erros: list[str] = []

        if not nome.strip():
            erros.append("Informe seu nome.")
        if not validar_telefone(telefone):
            erros.append("Telefone inválido (mínimo 10 dígitos).")
        if not validar_email(email):
            erros.append("E-mail inválido.")

        apostas, erros_grupos = validar_apostas(selecoes)
        erros.extend(erros_grupos)

        if erros:
            for msg in erros:
                st.error(msg)
            return

        if email_existe(email):
            st.error("Este e-mail já participou do bolão.")
            return

        participante_id = salvar_participacao(nome, telefone, email, apostas)
        st.success(f"Aposta registrada com sucesso, {nome.strip()}! Boa sorte! 🎉")
        st.balloons()

        with st.expander("Resumo da sua aposta", expanded=True):
            for aposta in apostas:
                st.write(f"**Grupo {aposta['grupo']}:** 1º {aposta['primeiro']} · 2º {aposta['segundo']}")
            st.caption(f"ID da participação: {participante_id}")


def render_admin() -> None:
    st.subheader("Participantes")
    participantes = listar_participantes()

    if not participantes:
        st.info("Nenhum participante cadastrado ainda.")
        return

    st.dataframe(
        [
            {
                "Nome": p["nome"],
                "E-mail": p["email"],
                "Telefone": p["telefone"],
                "Data": p["criado_em"],
            }
            for p in participantes
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("Apostas por participante")
    for p in participantes:
        apostas = listar_apostas(p["id"])
        with st.expander(f"{p['nome']} — {p['email']}"):
            for a in apostas:
                st.write(f"Grupo {a['grupo']}: 1º {a['primeiro']} · 2º {a['segundo']}")


tab_bolao, tab_admin = st.tabs(["Bolão", "Admin"])

with tab_bolao:
    render_bolao()

with tab_admin:
    render_admin()
