# TRIARB PYTHON PROJECT
import json

import func_arbitrage

# Global Variables

coin_price_url = "https://poloniex.com/public?command=returnTicker"



# Extracting coin prices from exchange
def step0():
    coin_json = func_arbitrage.get_tickers(coin_price_url)
    print(coin_json)

    # Looping through json to find tradeable pairs

    coin_list = func_arbitrage.collect_tradeables(coin_json)


    return coin_list

# Sort coin pairs into triangular options
def step1(coin_list):

    #structure list of tradeable pairs
    structured_list = func_arbitrage.structure_pairs(coin_list)
    with open("structured_triangular_pairs.json", "w") as fp:
        json.dump(structured_list, fp)

def step2():

    with open("structured_triangular_pairs.json") as json_file:
        structured_pairs = json.load(json_file)


    prices_json = func_arbitrage.get_tickers(coin_price_url)

    for t_pair in structured_pairs:
        prices_dict = func_arbitrage.get_price_for_pair(t_pair, prices_json)
        profit = func_arbitrage.calculate_surface_rate(t_pair, prices_dict)


""" MAIN """

if __name__ == "__main__":

    coin_list = step0()
    #step0()
    step1(coin_list)
    step2()










