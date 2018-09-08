This program is to find the stock portfolio with maximum sharpe ratio using 
brute force. It will try different sets and weights of stocks/index and 
find the one with the highest sharpe ratio.

Originally this is an assignment of a class focus on Excel. But when my classmates
and I was doing this assignment, we found it takes a lot of time to adjust the
combination and weight, so I made a python program that automates this process. 
By using Pandas package, I made it very efficient, although it still takes some
time since there are so many combinations (sets of stocks * sets of weights) I need
to try.

Something to pay attention:

The format of the stock data should be like the example. There is no time column, and
the risk-free column should be put as the last column.

The result file is the one record the best result. 

I think I may implement multi-thread if I have time.

Enjoy!