import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(description="aaa")
    arg_parser.add_argument("-d", "--date", type=str, required=True, help="date to check, format='YYYYMMDD'")
    arg_parser.add_argument("--switch", type=str, required=True, choices=("vp", "fund", "macro", "pos", "tab"),
                            help="which type of data to validate")
    arg_parser.add_argument("--tab0", type=str,
                            help="The first table to read, only used when argument 'switch' is 'tab', format like 'meta_data.future_bar_1day_aft'")
    arg_parser.add_argument("--tab1", type=str,
                            help="The second table to read, only used when argument 'switch' is 'tab', format like 'meta_data.future_bar_1day_aft'")
    arg_parser.add_argument("--vars", type=str, help="vars to check, only used when argument 'switch' is 'tab'.")
    return arg_parser.parse_args()


if __name__ == "__main__":
    import sys
    import datetime as dt
    from qtools_sxzq.qwidgets import SFG, SFY, SFR
    from solutions.validators import fetch_data

    args = parse_args()

    if args.switch == "vp":
        from solutions.validators import validate_price_volume

        data = fetch_data(
            trade_date=args.date,
            lib="meta_data",
            table="future_bar_1day_aft",
            names=["datetime", "code", "real_code",
                   "`open`", "high", "low", "`close`",
                   "volume", "open_interest", "turnover"],
        )
        if validate_price_volume(data, qty=67):
            print(
                f"[OK ] [{dt.datetime.now()}] {SFG('Successfully')} validate {SFY('price and volume')} data @ {args.date}")
            sys.exit(0)
        else:
            print(
                f"[ERR] [{dt.datetime.now()}] {SFR('Failed')} to validate {SFY('price and volume')} data @ {args.date}")
            sys.exit(1)
    elif args.switch == "fund":
        from solutions.validators import validate_fund

        data = fetch_data(
            trade_date=args.date,
            lib="basic",
            table="fundamental_data",
            names=["datetime", "date", "code", "basis", "basis_rate", "stock"],
        )
        if validate_fund(data, qty=67):
            print(f"[OK ] [{dt.datetime.now()}] {SFG('Successfully')} validate {SFY('fundamental')} data @ {args.date}")
            sys.exit(0)
        else:
            print(f"[ERR] [{dt.datetime.now()}] {SFR('Failed')} to validate {SFY('fundamental')} data @ {args.date}")
            sys.exit(1)
    elif args.switch == "macro":
        from solutions.validators import validate_macro

        data = fetch_data(
            trade_date=args.date,
            lib="basic",
            table="macro_data",
            names=["datetime", "code",
                   "usdcny_close", "`close`", "m_881001_close",
                   "m0000612", "m0001227", "m0001385", "m0017126"],
        )
        if validate_macro(data, qty=1):
            print(f"[OK ] [{dt.datetime.now()}] {SFG('Successfully')} validate {SFY('macro')} data @ {args.date}")
            sys.exit(0)
        else:
            print(f"[ERR] [{dt.datetime.now()}] {SFR('Failed')} to validate {SFY('macro')} data @ {args.date}")
            sys.exit(1)
    elif args.switch == "pos":
        from solutions.validators import read_pos, validate_pos

        data = read_pos(
            trade_date=args.date,
            lib="/root/workspace/Data/huxo/input/by_date",
            name_tmpl="tushare_futures_pos_{}.csv.gz",
        )
        if validate_pos(data, qty=7000):
            print(f"[OK ] [{dt.datetime.now()}] {SFG('Successfully')} validate {SFY('position')} data @ {args.date}")
            sys.exit(0)
        else:
            print(f"[ERR] [{dt.datetime.now()}] {SFR('Failed')} to validate {SFY('position')} data @ {args.date}")
            sys.exit(1)
    elif args.switch == "tab":
        from solutions.validators import check_var

        lib, table = args.tab0.split(".")
        data0 = fetch_data(trade_date=args.date, lib=lib, table=table, names="datetime,code," + args.vars)
        data0 = data0.set_index(["datetime", "code"]).sort_index()
        lib, table = args.tab1.split(".")
        data1 = fetch_data(trade_date=args.date, lib=lib, table=table, names="datetime,code," + args.vars)
        data1 = data1.set_index(["datetime", "code"]).sort_index()
        check_vars = args.vars.split(",")
        for cvar in check_vars:
            check_var(
                s0=data0[cvar],
                s1=data1[cvar],
                src0=args.tab0,
                src1=args.tab1,
                var_name=cvar,
            )
    else:
        print(f"[ERR] Invalid switch {args.switch}")
        sys.exit(1)
