import os
import datetime
import csv
import MetaTrader5 as mt5

class MT5:
    def initialize(self):
        if not mt5.initialize():
            mt5.shutdown()
            return 0, "Cannot connect to MT5"
        return 1, "Connected to MT5"
    
    def shutdown(self):
        mt5.shutdown()

    def __CreateFile(self, orders):
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
        return filename

    def Export(self):
        orders = mt5.orders_get()
        if len(orders) == 0:
            return(0, "There is no orders!")
        else:
            filename = self.__CreateFile(orders)
            return(filename, "!!!Export Successful!!!")

    def __SendOrder(self, row):
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
            return f"Failed to send order for {row[0]}: No response from MT5"
        elif result.retcode != mt5.TRADE_RETCODE_DONE:
            return f"Failed to recreate order for {row[0]}: {result.comment}"
        else:
            return f"Order recreated for {row[0]}"

    def Import(self, filename):
        log_list = []
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar='|')
            for row in reader:
                if row[0] != "Symbol":
                    check_order_exist = mt5.orders_get(symbol=row[0])
                    if len(check_order_exist) == 0:
                        log_list.append(self.__SendOrder(row))
                    else:
                        flag_exist = True
                        for item in check_order_exist:
                            if float(item.price_open) == float(row[3]):
                                flag_exist = False
                                break
                        if flag_exist:
                            log_list.append(self.__SendOrder(row))

        log_list.append("Restore completed!")
        return log_list