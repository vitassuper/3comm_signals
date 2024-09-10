import sqlite3
from typing import Any, List, Tuple

conn = sqlite3.connect('signals.sqlite3')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_candlesticks_table() -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candlesticks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol VARCHAR(64) NOT NULL,
            opened_at TIMESTAMP NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL
        )
    """)
    conn.commit()


def fetch_candles(
    symbol: str, since: int = None, limit: int = None
) -> List[dict]:
    query = """
        SELECT opened_at, open, high, low, close, volume 
        FROM candlesticks 
        WHERE symbol = ?
    """

    params = [symbol]

    if since is not None:
        query += 'AND opened_at >= ? '
        params.append(since)

    query += 'ORDER BY opened_at ASC'

    if limit is not None:
        query += ' LIMIT ?'
        params.append(limit)

    cursor.execute(query, params)

    return cursor.fetchall()


def fetch_first_and_last_candles(
    symbol: str,
) -> Tuple[Any, Any] | Tuple[None, None]:
    query = """SELECT *
    FROM (
        SELECT opened_at, open, high, low, close, volume
        FROM candlesticks
        WHERE symbol = ?
        ORDER BY opened_at ASC
        LIMIT 1
    ) AS first_candle
    UNION ALL
    SELECT *
    FROM (
        SELECT opened_at, open, high, low, close, volume
        FROM candlesticks
        WHERE symbol = ?
        ORDER BY opened_at DESC
        LIMIT 1
    ) AS last_candle"""
    cursor.execute(query, (symbol, symbol))

    rows = cursor.fetchall()

    match len(rows):
        case 2:
            candles = rows[0], rows[1]
        case 1:
            candles = rows[0], rows[0]
        case _:
            candles = None, None

    return candles


def insert_candles(symbol: str, candles: List[dict] | dict) -> None:
    if isinstance(candles, dict):
        candles = [candles]

    for candle in candles:
        cursor.execute(
            """
        INSERT INTO candlesticks (symbol, opened_at, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            [symbol] + candle,
        )

    conn.commit()
