import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "bolao.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                criado_em TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS apostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participante_id INTEGER NOT NULL,
                grupo TEXT NOT NULL,
                primeiro TEXT NOT NULL,
                segundo TEXT NOT NULL,
                FOREIGN KEY (participante_id) REFERENCES participantes(id)
            );

            CREATE TABLE IF NOT EXISTS mata_mata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participante_id INTEGER NOT NULL,
                jogo_key TEXT NOT NULL,
                vencedor TEXT NOT NULL,
                FOREIGN KEY (participante_id) REFERENCES participantes(id)
            );
            """
        )
        cols = conn.execute("PRAGMA table_info(participantes)").fetchall()
        if not any(c[1] == "campeao" for c in cols):
            conn.execute("ALTER TABLE participantes ADD COLUMN campeao TEXT")


def email_existe(email: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM participantes WHERE LOWER(email) = LOWER(?)",
            (email.strip(),),
        ).fetchone()
    return row is not None


def salvar_participacao(
    nome: str,
    telefone: str,
    email: str,
    apostas: list[dict[str, str]],
    mata_mata: dict[str, str] | None = None,
    campeao: str | None = None,
) -> int:
    criado_em = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO participantes (nome, telefone, email, criado_em, campeao)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome.strip(), telefone.strip(), email.strip().lower(), criado_em, campeao),
        )
        participante_id = cursor.lastrowid
        conn.executemany(
            """
            INSERT INTO apostas (participante_id, grupo, primeiro, segundo)
            VALUES (?, ?, ?, ?)
            """,
            [
                (participante_id, a["grupo"], a["primeiro"], a["segundo"])
                for a in apostas
            ],
        )
        if mata_mata:
            conn.executemany(
                """
                INSERT INTO mata_mata (participante_id, jogo_key, vencedor)
                VALUES (?, ?, ?)
                """,
                [(participante_id, k, v) for k, v in mata_mata.items()],
            )
        conn.commit()
    return participante_id


def listar_participantes() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, nome, telefone, email, criado_em, campeao
            FROM participantes
            ORDER BY criado_em DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def listar_apostas(participante_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT grupo, primeiro, segundo
            FROM apostas
            WHERE participante_id = ?
            ORDER BY grupo
            """,
            (participante_id,),
        ).fetchall()
    return [dict(row) for row in rows]
