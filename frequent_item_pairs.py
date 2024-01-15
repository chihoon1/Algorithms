'''
Frequent itemset mining algorithm

Assumed each basekt does not contain more than one item of the same item
'''


'''
Steps
n is the total number of item in the data set
Iteration(pass) i=1:n
    step1: create candidate sets(for pairs of frequent i-th number of elements in i-th pass)
    step2: count pairs with k-tuple
    step3: save the pairs if a pair count >= threshold
'''
def frequent_item_mining(transactions_data, k, **kwargs):
    # param: transcations_data (2d lists) where each row represents a basket of items and the basket size can vary
    # param: k = total number of items
    # return a 2d list of frequent item pairs
    #       where each row(outer list) represents number of items in a pair(index 0: 1 item, index 1: 2 items, etc.)
    min_support = kwargs.get('min_support', 3)  # threshold where count >= min_support considered frequent
    frequent_pairs = []  # data type is list of lists
    i = 1
    while i <= k:
        # step1: create cadidate sets
        L_i = frequent_pairs[i - 2] if i != 1 else transactions_data  # frequent pairs from the last pass
        candidate_item_set = set()
        for ind_j in range(len(L_i)):
            if i == 1:
                for basket in L_i[ind_j]:
                    for item in basket:
                        candidate_item_set.add(item)
                k = len(candidate_item_set)
            else:  # generating combinations of pairs
                curr_pair = set(L_i[ind_j])
                for ind_k in range(len(L_i)):
                    if ind_j != ind_k:
                        another_pair = set(L_i[ind_k])
                        new_items = another_pair.difference(curr_pair)
                        for item in new_items:
                            candidate_item_set.add(frozenset(curr_pair.union(set(item))))
        candidates_lst = []
        for elem in list(candidate_item_set):
            # converting candidate set into list of pairs(set data type)
            pair = set()
            for item in elem:
                pair.add(item)
            candidates_lst.append(pair)
        # print(f"Candidates Set:\n{candidates_lst}\nThe Size of Candidates Set: {len(candidates_lst)}")  # debug
        # step2: count pairs with k-tuple
        count_tuples_dict = {}  # dict. Key: pair(tuple), Value: count(int)
        for ind in range(len(transactions_data)):
            basket = set(transactions_data[ind])
            for candidate in candidates_lst:
                if candidate.issubset(basket):
                    try:
                        count_tuples_dict[tuple(candidate)] += 1
                    except KeyError:
                        count_tuples_dict[tuple(candidate)] = 1
        # print(f"Counts:\n{count_tuples_dict}")  # debug
        # step3: check which pairs are frequent
        frequent_i_th_pairs = []
        for key, val in count_tuples_dict.items():
            if val >= min_support:
                pair_str = ""
                for item in key:
                    pair_str += item
                frequent_i_th_pairs.append(pair_str)
        frequent_pairs.append(frequent_i_th_pairs)
        # print(f"Frequent Pairs:\n{frequent_i_th_pairs}\n")  # debug
        i += 1
    return frequent_pairs


if __name__ == '__main__':
    # test the function
    transactions_data = [['A', 'B', 'C', 'D'],
                         ['B', 'E'],
                         ['A', 'B', 'C', 'E'],
                         ['A', 'B', 'F'],
                         ['A', 'C', 'F'],
                         ['B', 'C', 'D', 'E'],
                         ['A', 'C'],
                         ['A', 'B', 'C', 'D', 'E'],
                         ['A', 'B', 'F'],
                         ['C', 'D']]
    items = set([elem for basket in transactions_data for elem in basket])
    freqeunt_pairs_list = frequent_item_mining(transactions_data, k=len(items))
    print(f"Frequent Item Pairs:{freqeunt_pairs_list}")