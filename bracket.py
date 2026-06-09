"""Chaveamento eliminatório a partir das seleções classificadas (1º e 2º de cada grupo)."""

from groups import GRUPOS

# Cruzamentos da primeira fase eliminatória: (grupo_a, pos_a) x (grupo_b, pos_b)
RODADA_1 = [
    ("A", 1, "B", 2),
    ("C", 1, "D", 2),
    ("E", 1, "F", 2),
    ("G", 1, "H", 2),
    ("I", 1, "J", 2),
    ("K", 1, "L", 2),
    ("B", 1, "A", 2),
    ("D", 1, "C", 2),
    ("F", 1, "E", 2),
    ("H", 1, "G", 2),
    ("J", 1, "I", 2),
    ("L", 1, "K", 2),
]

# Nome da rodada de acordo com o número de seleções que entram nela
NOMES_POR_TIMES = {
    2: "Final",
    3: "Semifinal",
    4: "Semifinal",
    6: "Quartas de final",
    8: "Quartas de final",
    12: "Oitavas de final",
    16: "Oitavas de final",
    24: "Primeira fase eliminatória",
    32: "Rodada de 32",
}


def flag_pos(selecoes: dict[str, dict], grupo: str, pos: int) -> str | None:
    chave = "primeiro" if pos == 1 else "segundo"
    return selecoes.get(grupo, {}).get(chave)


def jogos_iniciais(selecoes: dict[str, dict]) -> list[tuple[str, str]]:
    jogos: list[tuple[str, str]] = []
    for g1, p1, g2, p2 in RODADA_1:
        t1 = flag_pos(selecoes, g1, p1)
        t2 = flag_pos(selecoes, g2, p2)
        if t1 and t2:
            jogos.append((t1, t2))
    return jogos


def nome_rodada(n_times: int) -> str:
    return NOMES_POR_TIMES.get(n_times, f"Fase ({n_times} seleções)")


def vencedores(jogos: list[dict]) -> list[str]:
    return [j["vencedor"] for j in jogos if j.get("vencedor")]


def emparelhar(classificados: list[str]) -> tuple[list[str], list[tuple[str, str]]]:
    """Retorna (byes, jogos) para a próxima rodada. Se ímpar, o 1º passa direto."""
    if len(classificados) <= 1:
        return classificados, []
    byes: list[str] = []
    times = list(classificados)
    if len(times) % 2 == 1:
        byes = [times[0]]
        times = times[1:]
    jogos = [(times[i], times[i + 1]) for i in range(0, len(times), 2)]
    return byes, jogos


def montar_chaveamento(selecoes: dict[str, dict], picks: dict[str, str]) -> list[dict]:
    rodadas: list[dict] = []
    jogos_atuais = jogos_iniciais(selecoes)
    byes_pendentes: list[str] = []
    idx = 0

    while jogos_atuais:
        n_times = len(jogos_atuais) * 2 + len(byes_pendentes)
        jogos_info = []
        for i, (a, b) in enumerate(jogos_atuais):
            key = f"r{idx:02d}_m{i:02d}"
            jogos_info.append({"key": key, "a": a, "b": b, "vencedor": picks.get(key)})

        rodadas.append(
            {"nome": nome_rodada(n_times), "n_times": n_times, "jogos": jogos_info, "byes": list(byes_pendentes)}
        )

        vencs = vencedores(jogos_info)
        if len(vencs) < len(jogos_info):  # rodada incompleta
            break

        classificados = byes_pendentes + vencs
        if len(classificados) <= 1:
            break

        byes_pendentes, jogos_atuais = emparelhar(classificados)
        idx += 1

    return rodadas


def limpar_picks_invalidos(selecoes: dict[str, dict], picks: dict[str, str]) -> dict[str, str]:
    """Remove palpites de jogos que deixaram de existir ou cujo vencedor não está no confronto."""
    while True:
        chave = montar_chaveamento(selecoes, picks)
        validos: dict[str, set[str]] = {}
        for rodada in chave:
            for jogo in rodada["jogos"]:
                validos[jogo["key"]] = {jogo["a"], jogo["b"]}

        remover = [k for k, v in picks.items() if k not in validos or v not in validos[k]]
        if not remover:
            return picks
        for k in remover:
            del picks[k]


def campeao(picks: dict[str, str], selecoes: dict[str, dict]) -> str | None:
    chave = montar_chaveamento(selecoes, picks)
    if not chave:
        return None
    ultima = chave[-1]
    if ultima["n_times"] == 2 and len(ultima["jogos"]) == 1:
        return ultima["jogos"][0].get("vencedor")
    return None


def grupos_completos(selecoes: dict[str, dict]) -> bool:
    for grupo in GRUPOS:
        sel = selecoes.get(grupo, {})
        if not sel.get("primeiro") or not sel.get("segundo"):
            return False
    return True


def rodada_atual(selecoes: dict[str, dict], picks: dict[str, str]) -> dict | None:
    for rodada in montar_chaveamento(selecoes, picks):
        if any(not j.get("vencedor") for j in rodada["jogos"]):
            return rodada
    return None


def mata_mata_completo(selecoes: dict[str, dict], picks: dict[str, str]) -> bool:
    return campeao(picks, selecoes) is not None
