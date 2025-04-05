import os
import datetime
import csv
import MetaTrader5 as mt5

if not mt5.initialize():
    print("Cannot connect to mt5")
    mt5.shutdown()

def CreateFile(orders):
    if not os.path.isdir("Exports"):
        os.makedirs("Exports")
    filename = "Exports/" + datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S') + " -- ExportMT5.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Symbol", "OrderType", "Volume", "Price", "StopLoss", "TakeProfit", "Expiration", "Comment"])
        for order in orders:
            writer.writerow([
                order.symbol, 
                "BUY_LIMIT" if order.type == mt5.ORDER_TYPE_BUY_LIMIT else "SELL_LIMIT",
                order.volume_current,
                order.price_open,
                order.sl,
                order.tp,
                order.time_expiration,
                order.comment
            ])

orders = mt5.orders_get()
if len(orders) == 0:
    print("There is no orders!")
else:
    CreateFile(orders)
    print("!!! Export successful !!!")

mt5.shutdown()