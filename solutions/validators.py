import os
import pandas as pd
from typing import Union
from qtools_sxzq.qdataviewer import fetch
from qtools_sxzq.qwidgets import SFG, SFY


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


def read_pos(trade_date: str, lib: str, name_tmpl: str) -> pd.DataFrame:
    src_file = name_tmpl.format(trade_date)
    src_path = os.path.join(lib, trade_date[0:4], trade_date, src_file)
    try:
        df = pd.read_csv(src_path)
    except FileNotFoundError:
        df = pd.DataFrame()
    return df


def validate_pos(df: pd.DataFrame, qty: int) -> bool:
    return len(df) >= qty


def check_var(
        s0: pd.Series, s1: pd.Series, src0: str, src1: str, var_name: str, dropna: bool, precision: float,
) -> bool:
    set0, set1 = set(s0.index), set(s1.index)
    if d01 := set0.difference(set1):
        print(f"[ERR] elements in {src0} but not in {src1}: {d01}")
    if d10 := set1.difference(set0):
        print(f"[ERR] elements in {src1} but not in {src0}: {d10}")

    id0, id1 = f"{var_name}0", f"{var_name}1"
    df = pd.DataFrame({id0: s0, id1: s1})
    if dropna:
        df = df.dropna(axis=0, how="all")
    diff = df[id0] - df[id1]
    diff_data = df.loc[~(diff.abs() <= precision)]
    if diff_data.empty:
        print(f"[INF] No errors are found between {SFG(id0)} and {SFG(id1)}")
    else:
        print(f"[{SFY('ERR')}] {SFY(len(diff_data))} errors are found between {SFY(id0)} and {SFY(id1)}, they are:")
        print(diff_data)
