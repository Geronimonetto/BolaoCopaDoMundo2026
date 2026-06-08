"""Dados estáticos dos grupos da Copa do Mundo 2026 (48 seleções, 12 grupos)."""

GRUPOS: dict[str, list[dict[str, str]]] = {
    "A": [
        {"nome": "Estados Unidos", "bandeira": "🇺🇸"},
        {"nome": "México", "bandeira": "🇲🇽"},
        {"nome": "Canadá", "bandeira": "🇨🇦"},
        {"nome": "Equador", "bandeira": "🇪🇨"},
    ],
    "B": [
        {"nome": "Brasil", "bandeira": "🇧🇷"},
        {"nome": "Marrocos", "bandeira": "🇲🇦"},
        {"nome": "Croácia", "bandeira": "🇭🇷"},
        {"nome": "Japão", "bandeira": "🇯🇵"},
    ],
    "C": [
        {"nome": "Argentina", "bandeira": "🇦🇷"},
        {"nome": "França", "bandeira": "🇫🇷"},
        {"nome": "Senegal", "bandeira": "🇸🇳"},
        {"nome": "Austrália", "bandeira": "🇦🇺"},
    ],
    "D": [
        {"nome": "Inglaterra", "bandeira": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
        {"nome": "Dinamarca", "bandeira": "🇩🇰"},
        {"nome": "Colômbia", "bandeira": "🇨🇴"},
        {"nome": "Costa Rica", "bandeira": "🇨🇷"},
    ],
    "E": [
        {"nome": "Alemanha", "bandeira": "🇩🇪"},
        {"nome": "Espanha", "bandeira": "🇪🇸"},
        {"nome": "Uruguai", "bandeira": "🇺🇾"},
        {"nome": "Coreia do Sul", "bandeira": "🇰🇷"},
    ],
    "F": [
        {"nome": "Portugal", "bandeira": "🇵🇹"},
        {"nome": "Holanda", "bandeira": "🇳🇱"},
        {"nome": "Suíça", "bandeira": "🇨🇭"},
        {"nome": "Gana", "bandeira": "🇬🇭"},
    ],
    "G": [
        {"nome": "Bélgica", "bandeira": "🇧🇪"},
        {"nome": "Itália", "bandeira": "🇮🇹"},
        {"nome": "Chile", "bandeira": "🇨🇱"},
        {"nome": "Nigéria", "bandeira": "🇳🇬"},
    ],
    "H": [
        {"nome": "Polônia", "bandeira": "🇵🇱"},
        {"nome": "Suécia", "bandeira": "🇸🇪"},
        {"nome": "Peru", "bandeira": "🇵🇪"},
        {"nome": "Irã", "bandeira": "🇮🇷"},
    ],
    "I": [
        {"nome": "Ucrânia", "bandeira": "🇺🇦"},
        {"nome": "Sérvia", "bandeira": "🇷🇸"},
        {"nome": "Paraguai", "bandeira": "🇵🇾"},
        {"nome": "Camarões", "bandeira": "🇨🇲"},
    ],
    "J": [
        {"nome": "Turquia", "bandeira": "🇹🇷"},
        {"nome": "Áustria", "bandeira": "🇦🇹"},
        {"nome": "Egito", "bandeira": "🇪🇬"},
        {"nome": "Panamá", "bandeira": "🇵🇦"},
    ],
    "K": [
        {"nome": "Escócia", "bandeira": "🏴󠁧󠁢󠁳󠁣󠁴󠁿"},
        {"nome": "Noruega", "bandeira": "🇳🇴"},
        {"nome": "Argélia", "bandeira": "🇩🇿"},
        {"nome": "Jamaica", "bandeira": "🇯🇲"},
    ],
    "L": [
        {"nome": "Catar", "bandeira": "🇶🇦"},
        {"nome": "Tunísia", "bandeira": "🇹🇳"},
        {"nome": "Venezuela", "bandeira": "🇻🇪"},
        {"nome": "Nova Zelândia", "bandeira": "🇳🇿"},
    ],
}


def label_time(time: dict[str, str]) -> str:
    return f"{time['bandeira']} {time['nome']}"


def opcoes_grupo(grupo: str) -> list[str]:
    return [label_time(t) for t in GRUPOS[grupo]]
