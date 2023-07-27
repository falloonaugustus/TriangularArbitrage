import requests
import json

#Below is the processes behind retrieving swap prices for crypto currency pairs and identifying profitable arbitrage routes
#This consists of reading all pair prices, finding all possible triangular arbitrage routes and then identifying ones which will result in a profit


# Extract json of information from exchange
def get_tickers(url):
    req = requests.get(url)
    json_response = json.loads(req.text)
    return json_response

def collect_tradeables(json_obj):
    coin_list = []
    for coin in json_obj:
        is_frozen = json_obj[coin]["isFrozen"]
        is_post_only = json_obj[coin]["postOnly"]
        if is_frozen == "0" and is_post_only == "0":
            coin_list.append(coin)

    return coin_list

def structure_pairs(coin_list):
    # Variables
    triangular_pairs_list = []
    r_list = []
    pairs_list = coin_list

    # Getting Pair A
    for pair_a in coin_list:
        pair_a_split = pair_a.split("_")

        a_b = pair_a_split[0]
        a_q = pair_a_split[1]

        for pair_b in coin_list:
            if pair_b != pair_a:
                pair_b_split = pair_b.split("_")
                b_b = pair_b_split[0]
                b_q = pair_b_split[1]

                if b_b in pair_a_split or b_q in pair_a_split:
                    ab_pair = [pair_a, pair_b]
                    ba_pair = [pair_b, pair_a]
                    if ab_pair in r_list or ba_pair in r_list:
                        pass
                    else:
                        for pair_c in coin_list:
                            if pair_c != pair_a and pair_c != pair_b:
                                pair_c_split = pair_c.split("_")
                                c_b = pair_c_split[0]
                                c_q = pair_c_split[1]

                                pair_box = [a_b, a_q, b_b, b_q, c_b, c_q]
                                count_b = 0
                                count_q = 0
                                for i in pair_box:
                                    if i == c_b:
                                        count_b += 1

                                for i in pair_box:
                                    if i == c_q:
                                        count_q += 1
                                if count_b == 2 and count_q == 2 and c_b != c_q:
                                    p1 = [pair_a, pair_b]
                                    p2 = [pair_b, pair_c]
                                    p3 = [pair_a, pair_c]
                                    r_list.append(p1)
                                    r_list.append(p2)
                                    r_list.append(p3)
                                    combined = pair_a + "," + pair_b + "," + pair_c
                                    my_dict = {
                                        "a_base": a_b,
                                        "a_quote": a_q,
                                        "b_base": b_b,
                                        "b_quote": b_q,
                                        "c_base": c_b,
                                        "c_quote": c_q,
                                        "pair_a": pair_a,
                                        "pair_b": pair_b,
                                        "pair_c": pair_c,
                                        "combine": combined
                                    }

                                    triangular_pairs_list.append(my_dict)

    return triangular_pairs_list



def get_price_for_pair(t_pair, prices_json):


    # Extract Pair Info

    pair_a = t_pair["pair_a"]
    pair_b = t_pair["pair_b"]
    pair_c = t_pair["pair_c"]

    # Extract Price Info
    float()
    pair_a_ask = float(prices_json[pair_a]["lowestAsk"])
    pair_a_bid = float(prices_json[pair_a]["highestBid"])
    pair_b_ask = float(prices_json[pair_b]["lowestAsk"])
    pair_b_bid = float(prices_json[pair_b]["highestBid"])
    pair_c_ask = float(prices_json[pair_c]["lowestAsk"])
    pair_c_bid = float(prices_json[pair_c]["highestBid"])

    return {
        "pair_a_ask": pair_a_ask,
        "pair_a_bid": pair_a_bid,
        "pair_b_ask": pair_b_ask,
        "pair_b_bid": pair_b_bid,
        "pair_c_ask": pair_c_ask,
        "pair_c_bid": pair_c_bid
    }



def calculate_surface_rate(t_pair, price_dict):

    # Variable Declaration

    starting_amount = 1
    min_surf_rate = 0
    surf_dict = {}
    contract_2 = ""
    contract_3 = ""
    dir_trade_1 = ""
    dir_trade_2 = ""
    dir_trade_3 = ""
    acq_coin_t2 = ""
    acq_coin_t3 = ""
    calculated = 0

    # Pair Variables

    a_b = t_pair["a_base"]
    a_q = t_pair["a_quote"]
    b_b = t_pair["b_base"]
    b_q = t_pair["b_quote"]
    c_b = t_pair["c_base"]
    c_q = t_pair["c_quote"]
    pair_a = t_pair["pair_a"]
    pair_b = t_pair["pair_b"]
    pair_c = t_pair["pair_c"]

    #Price Info

    a_ask = price_dict["pair_a_ask"]
    a_bid = price_dict["pair_a_bid"]
    b_ask = price_dict["pair_b_ask"]
    b_bid = price_dict["pair_b_bid"]
    c_ask = price_dict["pair_c_ask"]
    c_bid = price_dict["pair_c_bid"]

    initial_amount = 1
    amount = initial_amount
    price_list = [a_ask, a_bid, b_ask, b_bid, c_ask, c_bid]
    coin_list = [a_b, a_q, b_b, b_q, c_b, c_q]
    example = ["BTC", "ETH", "ETH", "LTC", "BTC", "LTC"]
    # Assume we are starting from a base
    amount = amount / a_ask
    curr_coin = a_q
    i = 2
    while curr_coin != a_b:
        if coin_list[i] == curr_coin:
            if i % 2 == 0:
                amount = amount / price_list[i]
                curr_coin = coin_list[i+1]
                if 1 < i < 4:
                    i = 4
                else:
                    i = 2
            else:
                amount = amount * price_list[i]
                curr_coin = coin_list[i - 1]
                if i > 3:
                    i = 2
                else:
                    i = 4
        else:
            i += 1


    if amount > initial_amount:
        profit_rate = amount / initial_amount
        print(pair_a, pair_b, pair_c, profit_rate)


    # Set Directions List


    """
    If we are swapping base to quote do Quantity/Ask
    If we are swapping quote to base do Quantity * bid
    """





























