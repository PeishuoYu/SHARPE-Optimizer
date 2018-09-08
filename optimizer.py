import pandas as pd
import itertools


def rf_process(data):
    for name in list(data)[:-1]:
        data[name] = data[name] - data.iloc[:,-1]


def get_mean_return(data):
    return data.sum(axis=0) / data.shape[0]

def get_weight_combination(number_of_asset):
    numbers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] * 5
    result = [seq for i in [number_of_asset] for seq in itertools.combinations(numbers, i) if sum(seq) == 1]
    real_result = []
    for i in range(len(result)):
        real_result += list(itertools.permutations(list(result[i]), len(result[i])))
    real_result = list(set(real_result))
    for i in range(len(real_result)):
        real_result[i] = list(real_result[i])
    return real_result



def get_sharpe(combination, matrix, mean_returns, weight_combination):
    weight_combination = pd.Series(data=weight_combination, index=combination)
    exp_return = mean_returns.multiply(weight_combination).sum()
    std = matrix.multiply(weight_combination, axis=0).multiply(weight_combination, axis=1).values.sum() ** (1/2)
    return exp_return / std


def main(length_of_data, min_number_of_stocks_in_portfolio, max_number_of_stocks_in_portfolio, result_name):
    old_sharpe = 0
    stocks = pd.read_csv('stock_data.csv').iloc[:length_of_data,:]
    rf_process(stocks)
    stock_names = list(stocks)[:-1]
    for number_of_stocks in range(min_number_of_stocks_in_portfolio, max_number_of_stocks_in_portfolio + 1):
        combination = [list(i) for i in list(itertools.combinations(stock_names, number_of_stocks))]
        print(combination)
        weight_combinations = get_weight_combination(len(combination[0]))
        for stock_combination in combination:
            mean_returns = get_mean_return(stocks.loc[:,stock_combination])
            matrix = stocks.loc[:, stock_combination].cov()
            for weight_combination in weight_combinations:
                sharpe = get_sharpe(stock_combination, matrix, mean_returns, weight_combination)
                print(str(stock_combination) + ' ' + str(weight_combination) + ' ' + str(sharpe))
                if sharpe > old_sharpe:
                    print('Better Portfolio: ' + str(stock_combination) + ' ' + str(weight_combination) + ' ' + str(sharpe))
                    old_sharpe = sharpe
                    old_combination = stock_combination.copy()
                    file = open(result_name + '.txt', 'w')
                    file.write('[' + str(stock_combination) + ', ' + str(weight_combination) + '] ' + str(sharpe))
                    file.close()

def get_return(asset, weight, length_of_data):
    print(asset, weight)
    stocks = pd.read_csv('stock_data.csv').iloc[:length_of_data, :]
    rf_process(stocks)
    matrix = stocks.loc[:, asset].cov()
    weight_combination = pd.Series(data=weight, index=asset)
    mean_returns = get_mean_return(stocks.loc[:, asset])
    exp_return = mean_returns.multiply(weight_combination).sum()
    std = matrix.multiply(weight_combination, axis=0).multiply(weight_combination, axis=1).values.sum() ** (1/2)
    print('exp_return: ' + str(1.4 * (1 + exp_return) ** 60))
    print('std: ' + str(std))
    print('Sharpe: ' + str(exp_return / std))

main(length_of_data=215, min_number_of_stocks_in_portfolio = 2, max_number_of_stocks_in_portfolio=3, result_name='Best_portfilio')
get_return(['FFY'], [1], 215)
