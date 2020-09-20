from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import backtrader as bt
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from strategies import *
import pandas as pd

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000)
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'spy_2000-2020.csv')
    prices = pd.read_csv(datapath, index_col='Date', parse_dates=True)
    # Add a strategy
    cerebro.addstrategy(BuyAndHold)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere

    feed = bt.feeds.PandasData(
            dataname=prices,
            fromdate=datetime.datetime(2018, 1, 1),
            # Do not pass values before this date
            todate=datetime.datetime(2020, 1, 1),
        )

    cerebro.adddata(feed)
    initial_value = cerebro.broker.getvalue()
    cerebro.run() #will run our strategy defined in strategies
    final_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_value)
    percentage_increase = (((final_value - initial_value) / initial_value) * 100)
    print("Percentage increase: " + str(percentage_increase))
    #cerebro.plot()




