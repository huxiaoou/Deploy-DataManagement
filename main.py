import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(description="aaa")
    arg_parser.add_argument("-d", "--date", type=str, required=True, help="date to check, format='YYYYMMDD'")
    arg_parser.add_argument("--switch", type=str, required=True, choices=("vp", "fund", "macro"),
                            help="which type of data to validate")
    return arg_parser.parse_args()


if __name__ == "__main__":
    import sys
    import datetime as dt
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
            print(f"[OK][{dt.datetime.now()}] Successfully validate price and volume data @ {args.date}")
            sys.exit(0)
        else:
            print(f"[ERR][{dt.datetime.now()}] Failed to validate price and volume data @ {args.date}")
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
            print(f"[OK][{dt.datetime.now()}] Successfully validate fundamental data @ {args.date}")
            sys.exit(0)
        else:
            print(f"[ERR][{dt.datetime.now()}] Failed to validate fundamental data @ {args.date}")
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
            print(f"[OK][{dt.datetime.now()}] Successfully validate macro data @ {args.date}")
            sys.exit(0)
        else:
            print(f"[ERR][{dt.datetime.now()}] Failed to validate macro data @ {args.date}")
            sys.exit(1)
    else:
        print(f"[ERR] Invalid switch {args.switch}")
        sys.exit(1)
