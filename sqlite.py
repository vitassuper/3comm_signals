import sqlite3
from typing import List

conn = sqlite3.connect('signals.sqlite3')
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


def fetch_candlesticks(symbol: str) -> List[dict]:
    query = 'SELECT opened_at, open, high, low, close, volume FROM candlesticks WHERE symbol = ? ORDER BY opened_at DESC'
    cursor.execute(query, (symbol,))

    return cursor.fetchall()


def insert_candlesticks(symbol: str, candlesticks: List[dict] | dict) -> None:
    if isinstance(candlesticks, dict):
        candlesticks = [candlesticks]

    for candlestick in candlesticks:
        cursor.execute(
            """
        INSERT INTO candlesticks (symbol, opened_at, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            [symbol] + candlestick,
        )

    conn.commit()
