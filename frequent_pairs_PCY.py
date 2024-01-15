'''
Frequent itemset mining algorithm based on PCY(Park-Chen-Yu) algorithm

Assumed each basekt does not contain more than one item of the same item
'''
from itertools import combinations
import numpy as np

def mod_hash_func(*args, **kwargs):
    # return a hashed value of integer arguments(args)
    hash_table_size = kwargs.get('hash_table_size', 19)  # hash function is based on mod of this
    return int(np.prod(args)) % hash_table_size

def PCY(basket_collection, candidate_pairs, **kwargs):
    # param: basket_collection(2D array) where outer array represent a basekt
    #           and elem in inner array must be an integer representing an item
    # param: candidate_pairs(set) is a set of candidate item pairs to be checked whether it is a frquent item pair
    # return new candidate pairs(array of tuples) which need to be counted in the next pass
    support_threshold = kwargs.get('support_threshold', 4)  # threshold where count >= min_support considered frequent
    hash_table_size = kwargs.get('hash_table_size', 13)  # size of hash table
    r = kwargs.get('num_items_in_pair', 2)  # number of items in a pair for frequent item pair
    hash_func = kwargs.get('hash_func', mod_hash_func)
    # PCY counting for the first pass
    r_minus_one_counts = {}  # count occurences of a candiate pair in the basket_collection. key: pair, val: counts
    pair_counts = {}  # dictionary. Key: pair(tuple). Value: hashed value
    hash_table_arr = [0] * hash_table_size  # frequent bucket
    for basket in basket_collection:
        # counting the occurence of one item
        candidate_pairs_in_basket = []
        for item in candidate_pairs:
            if set(item).issubset(set(basket)):
                if r_minus_one_counts.get(item): r_minus_one_counts[item] += 1
                else: r_minus_one_counts[item] = 1  # initialize a key
                candidate_pairs_in_basket.append(item)  # this candidate pair exists in the basket
        # counting pairs in the hashed bucket
        all_pairs_in_a_basket = get_bigger_pairs(basket, candidate_pairs_in_basket)
        for pair in all_pairs_in_a_basket:
            hashed_val = hash_func(pair, hash_table_size=hash_table_size)
            if pair_counts.get(hashed_val) is not None:
                pair_counts[hashed_val].add(pair)
            else:
                pair_counts[hashed_val] = {pair}
            hash_table_arr[hashed_val] += 1
    new_candidate_pairs = set()
    for i in range(len(hash_table_arr)):  # convert hash table to a bit vector where elem = 1 when count >= support
        if hash_table_arr[i] >= support_threshold:  # condition 1: pair mapped to the frequent bucket
            for pair in pair_counts[i]:
                sub_pairs = combinations(pair, r-1)
                for sub_pair in sub_pairs:  # condition 2: each sub_pair in pair is frequent
                    if r_minus_one_counts[sub_pair] < support_threshold: break  # a sub_pair not frequent
                else:  # condition 1 and 2 met
                    new_candidate_pairs.add(tuple(sorted(pair)))
    return list(new_candidate_pairs)


def get_bigger_pairs(basket, candidate_pairs_in_basket):
    # get new pairs with one more item than a candiate pair but including one candidate pair in the new pair
    # basket(1d array) is a basket of items
    # candidate_pairs_in_basket(array) representing candidate pairs(tuple) that found in the basket
    unique_pairs = set()
    for candidate_pair in candidate_pairs_in_basket:
        for item in basket:
            new_pair = frozenset(candidate_pair + (item,))
            if new_pair != frozenset(candidate_pair):  # if new pair is same as candidate pair, then discard it
                unique_pairs.add(new_pair)
    new_pairs = []
    for pair in unique_pairs:  # chnage new_pair as a tuple not frozenset type
        new_pairs.append(tuple(pair))
    return new_pairs


def count_pairs_occurrences(pairs, basket_collection):
    # count occurrences of a pair in pairs list in the basket_collection
    # param: basket_collection(2D array) where outer array represent a basekt
    #               and elem in inner array must be an integer representing an item
    # param: pairs(list of tuples) to be counted for their occurrences
    # return a dictionary where key=pair, val=count(occurrence)
    counts = {}
    for basket in basket_collection:
        for pair in pairs:
            if set(pair).issubset(set(basket)):
                if counts.get(pair): counts[pair] += 1
                else: counts[pair] = 1
    return counts


if __name__ == '__main__':
    basket_collection = [[1, 2, 3],
                         [2, 3, 6],
                         [1, 3, 4],
                         [3, 4, 6],
                         [1, 5, 6],
                         [2, 4, 6],
                         [1, 2, 5],
                         [2, 4, 5],
                         [1, 3, 5],
                         [2, 3, 4],
                         [4, 5, 6],
                         [3, 5, 6]]
    # generating set of all items
    items_set = set()
    for basket in basket_collection:  # create a set containing all the unique items
        for item in basket:
            items_set.add((item,))
    pairs = PCY(basket_collection, items_set)
    print(f"pairs to be considered in the next pass:\n{pairs}")
    counts = count_pairs_occurrences(pairs, basket_collection)
    print(f"occurences of pairs: {counts}")