import os, math
import sys
import pandas as pd
import backtrader as bt



class GoldenCross(bt.Strategy):
    params = {
        'fast': 50,
        'slow': 200,
        'order_pct': 0.95,
        'ticker': 'SPY'
    }

    # params = (('fast', 50),
    #           ('slow', 200),
    #           ('order_pct', 0.95),
    #           ('ticker', 'SPY'))

    def __init__(self):
        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.fast,
            plotname='50 day'
        )
        print("\n===Golden Cross===\n")
        print('Initial Portfolio Value: %.2f' % self.broker.getvalue())

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.slow,
            plotname='200 day'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma,
            self.slowma
        )

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close[0])
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if (self.crossover < 0):
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()

class BuyAndHold(bt.Strategy):
    # params = (('fast', 15),
    #         ('slow', 50),
    #         ('order_pct', 0.95),
    #         ('ticker', 'SPY'))

    params = {
        'fast': 15,
        'slow': 50,
        'order_pct': 0.95,
        'ticker': 'SPY'
    }

    def __init__(self):
        amount_to_invest = (self.params.order_pct * self.broker.cash)
        self.lastDay = self.data.datetime.date(-1) #Refers to last trading day

        self.size = math.floor(amount_to_invest / self.data.close[0]) #Number of shares to invest
        print("\n===Buy And Hold===\n")
        print('Initial Portfolio Value: %.2f' % self.broker.getvalue())

    def next(self):

        if(len(self) == 1):
            print("Buy {} shares of {} at {} on {}".format(self.size, self.params.ticker, self.data.close[0], self.data.datetime.date(0)))
            self.buy(size=self.size)
            return
        #Sell on last day of dataseries
        if (self.data.datetime.date(0) == self.lastDay):
            print("Sell {} shares of {} at {} on {}".format(self.size, self.params.ticker, self.data.close[0], self.data.datetime.date(0)))
            self.close()

##### === Dollar Cost Average === #####

class DollarCostAverage(bt.Strategy):
    # params = dict (
    #     weekly_add = 1000.0,
    #     frequency = 30, #days
    #     ticker = 'SPY'
    # )

    params = {
        'weekly_add':  1000.0,
        'frequency': 30, #days
        'ticker': 'SPY'
    }


    def __init__(self):
        #self.broker.set_cash(self.params.start_amount)
        self.cash = self.broker.get_cash()
        self.days_passed = 0


    def payday(self):
        print("I got paid ${}!".format(self.params.weekly_add))
        #Calcualte max number of shares to buy
        self.cash += self.params.weekly_add
        self.broker.add_cash(self.params.weekly_add)
        self.shares_to_buy = math.floor(self.cash / self.data.close[0])
        print("Buy {} shares of {} on {} ".format(self.shares_to_buy, self.params.ticker, self.data.datetime.date(0)))
        self.buy(size=self.shares_to_buy)
        self.subtract = self.shares_to_buy * self.data.close[0]
        self.cash = self.cash - self.subtract

    def next(self):
        self.days_passed += 1
        print("Broker value: " + str(self.broker.getcash()))
        print("Cash value: " + str(self.cash))
        if self.days_passed == self.params.frequency:
            self.payday()
            self.days_passed = 0
            print(self.broker.getcash())







    # def next(self):
    #     if len(self) == 1:
    #         print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
    #         self.buy(size=self.size)
    #     elif len(self) == 2:
    #         print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
    #         self.close()
    #     if (len(self)) > 1 and self.position.size == 0:
    #         print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
    #         self.buy(size=self.size)






# class TestStrategy(bt.Strategy):

#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.dataclose = self.datas[0].close
#         self.order = None

#     def log(self, txt, dt=None):
#         ''' Logging function fot this strategy'''
#         dt = dt or self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))

#     #Notify the order has been completed
#     def notify_order(self, order):
#         if order.status in [order.Submitted, order.Accepted]:
#             return
#         if order.status in [order.Completed]:
#             if order.isbuy():
#                 self.log('BUY EXECUTED:{}'.format(order.executed.price))
#             elif order.issell():
#                 self.log('SELL EXECUTED:{}'.format(order.executed.price))
#         self.bar_executed = len(self)
#         self.order = None

#     def next(self):
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])
#         #print(self.position)

#         if len(self) >= 3:
#             #we dont want this iteration of the line if there's already an order in
#             #once we do not have an order, we'll check to see if we have an open postion in the market, if not, create a buy order.
#             #If we do have an open position in the market, we're gonna check to see if there's been 5 closings since the buy was executed(The row in the dataseries that the buy was executed is logged right after the buy is executed)
            
#             if self.order:
#                 return
            
#             if not self.position:
#                 if self.dataclose[0] < self.dataclose[-1]:
#                     # current close less than previous close

#                     if self.dataclose[-1] < self.dataclose[-2]:
#                         # previous close less than the previous close

#                         # BUY, BUY, BUY!!! (with all possible default parameters)
#                         self.log('BUY CREATE, %.2f' % self.dataclose[0])
#                         self.order = self.buy()
                        
#             else:
#                 if len(self) >= (self.bar_executed + 5):
#                     self.log("SELL CREATED {}".format(self.dataclose[0]) )
#                     self.order = self.sell()
#         else:
#             print("Gathering data...")




# Create a simple Stratey
# class TestStrategy(bt.Strategy):

#     def log(self, txt, dt=None):
#         ''' Logging function for this strategy'''
#         dt = self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))

#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.sma = btind.rsi()
#         self.dataclose = self.datas[0].close
#         self.dataopen = self.datas[0].open

#     def next(self):
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])
#         self.log('Open, %.2f' % self.dataopen[0])
#         self.log('Moving Average, %.2f' % self.sma[0])