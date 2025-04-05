import csv
import datetime
import MetaTrader5 as mt5

if not mt5.initialize():
    print("Cannot connect to mt5")
    mt5.shutdown()
else:
    err_list = []
    filename = input("Enter the file name : ").replace("\n", "")
    filename = "Exports/" + filename
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] != "Symbol":
                if row[6] != "0":
                    expiration = datetime.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S")
                else:
                    expiration = 0
                request = {
                    "action": mt5.TRADE_ACTION_PENDING,
                    "symbol": row[0],
                    "volume": float(row[2]),
                    "type": mt5.ORDER_TYPE_SELL_LIMIT if row[1] == "SELL_LIMIT" else mt5.ORDER_TYPE_BUY_LIMIT,
                    "price": float(row[3]),
                    "sl": float(row[4]),
                    "tp": float(row[5]),
                    "type_time": mt5.ORDER_TIME_SPECIFIED if row[6] != "0" else mt5.ORDER_TIME_GTC,
                    "expiration": int(expiration) if row[6] != "0" else 0,
                    "comment": row[7]
                }
                result = mt5.order_send(request)
                if result is None:
                    print(f"Failed to send order for {row[0]}: No response from MT5")
                    err_list.append(row[0])
                elif result.retcode != mt5.TRADE_RETCODE_DONE:
                    print(f"Failed to recreate order for {row[0]}: {result.comment}")
                    err_list.append(row[0])
                else:
                    print(f"Order recreated for {row[0]}")

    for item in err_list:
        print("This Symbol is not recreated : " + item)
    print("Restore completed!")

mt5.shutdown()