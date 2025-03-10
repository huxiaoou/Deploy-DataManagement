import pandas as pd
from typing import Union


def fetch(lib: str, table: str, names: Union[list[str], str], conds: str) -> pd.DataFrame:
    from transmatrix.data_api import Database

    var_str = ",".join(names) if isinstance(names, list) else names
    cmd_sql = f"SELECT {var_str} FROM {table}{f' WHERE {conds}' if conds else ''}"
    print(f"[INF] {cmd_sql}")
    db = Database(lib)
    _df = db.query(query=cmd_sql)
    return _df


def fetch_data(
        trade_date: str,
        lib: str,
        table: str,
        names: Union[list[str], str],
) -> pd.DataFrame:
    conds = f"datetime == '{trade_date[0:4]}-{trade_date[4:6]}-{trade_date[6:8]} 15:00:00'"
    df = fetch(lib=lib, table=table, names=names, conds=conds)
    return df


def validate_price_volume(df: pd.DataFrame, qty: int) -> bool:
    return len(df) >= qty


def validate_fund(df: pd.DataFrame, qty: int) -> bool:
    return len(df) == qty


def validate_macro(df: pd.DataFrame, qty: int) -> bool:
    return len(df) == qty
