"""Grupos oficiais — Copa do Mundo 2026."""

GRUPOS: dict[str, list[dict[str, str]]] = {
    "A": [
        {"nome": "México", "codigo": "mx"},
        {"nome": "África do Sul", "codigo": "za"},
        {"nome": "República da Coreia", "codigo": "kr"},
        {"nome": "Tchéquia", "codigo": "cz"},
    ],
    "B": [
        {"nome": "Canadá", "codigo": "ca"},
        {"nome": "Bósnia e Herzegovina", "codigo": "ba"},
        {"nome": "Catar", "codigo": "qa"},
        {"nome": "Suíça", "codigo": "ch"},
    ],
    "C": [
        {"nome": "Brasil", "codigo": "br"},
        {"nome": "Marrocos", "codigo": "ma"},
        {"nome": "Haiti", "codigo": "ht"},
        {"nome": "Escócia", "codigo": "gb-sct"},
    ],
    "D": [
        {"nome": "EUA", "codigo": "us"},
        {"nome": "Paraguai", "codigo": "py"},
        {"nome": "Austrália", "codigo": "au"},
        {"nome": "Turquia", "codigo": "tr"},
    ],
    "E": [
        {"nome": "Alemanha", "codigo": "de"},
        {"nome": "Curaçau", "codigo": "cw"},
        {"nome": "Costa do Marfim", "codigo": "ci"},
        {"nome": "Equador", "codigo": "ec"},
    ],
    "F": [
        {"nome": "Holanda", "codigo": "nl"},
        {"nome": "Japão", "codigo": "jp"},
        {"nome": "Suécia", "codigo": "se"},
        {"nome": "Tunísia", "codigo": "tn"},
    ],
    "G": [
        {"nome": "Bélgica", "codigo": "be"},
        {"nome": "Egito", "codigo": "eg"},
        {"nome": "RI do Irã", "codigo": "ir"},
        {"nome": "Nova Zelândia", "codigo": "nz"},
    ],
    "H": [
        {"nome": "Espanha", "codigo": "es"},
        {"nome": "Cabo Verde", "codigo": "cv"},
        {"nome": "Arábia Saudita", "codigo": "sa"},
        {"nome": "Uruguai", "codigo": "uy"},
    ],
    "I": [
        {"nome": "França", "codigo": "fr"},
        {"nome": "Senegal", "codigo": "sn"},
        {"nome": "Iraque", "codigo": "iq"},
        {"nome": "Noruega", "codigo": "no"},
    ],
    "J": [
        {"nome": "Argentina", "codigo": "ar"},
        {"nome": "Argélia", "codigo": "dz"},
        {"nome": "Áustria", "codigo": "at"},
        {"nome": "Jordânia", "codigo": "jo"},
    ],
    "K": [
        {"nome": "Portugal", "codigo": "pt"},
        {"nome": "RD do Congo", "codigo": "cd"},
        {"nome": "Uzbequistão", "codigo": "uz"},
        {"nome": "Colômbia", "codigo": "co"},
    ],
    "L": [
        {"nome": "Inglaterra", "codigo": "gb-eng"},
        {"nome": "Croácia", "codigo": "hr"},
        {"nome": "Gana", "codigo": "gh"},
        {"nome": "Panamá", "codigo": "pa"},
    ],
}

TEAM_INDEX: dict[str, dict[str, str]] = {
    team["nome"]: team for teams in GRUPOS.values() for team in teams
}


def flag_url(codigo: str) -> str:
    return f"https://flagcdn.com/w80/{codigo.lower()}.png"


def get_team(nome: str) -> dict[str, str] | None:
    return TEAM_INDEX.get(nome)
