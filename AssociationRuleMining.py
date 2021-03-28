import itertools
import string
import random


def create_itemset(num_of_itemsets: int, num_of_item_per_itemset: int):
    itemsets = set()
    while len(itemsets) != num_of_itemsets:
        current_set = set()
        while len(current_set) != num_of_item_per_itemset:
            current_set.add(random.choice(string.ascii_lowercase))
        sorted_set = sorted(current_set)
        itemsets.add(tuple(sorted_set))
    return itemsets


# k is used to represent number of elements in each itemset in itemsets
def generate_next_set_of_candidates(itemsets: set[tuple], k: int):
    next_candidates = set()
    itemsets_as_list = list(itemsets)
    is_candidate: bool
    for i in range(len(itemsets_as_list)):
        for j in range(i + 1, len(itemsets_as_list)):
            is_candidate = True
            for m in range(k - 1):
                if itemsets_as_list[i][m] != itemsets_as_list[j][m]:
                    is_candidate = False
                    break
            if is_candidate:
                itemset_to_add = list(itemsets_as_list[i])
                itemset_to_add.append(list(itemsets_as_list[j])[k - 1])
                sorted_set_to_add = sorted(itemset_to_add)
                next_candidates.add(tuple(sorted_set_to_add))
    return next_candidates


# k is used to represent number of elements in each itemset in original_itemsets
# Note that itemsets have k+1 number of items in each element
def eliminate_itemsets_with_non_frequent_items(original_itemsets: set[tuple], itemsets: set[tuple], k: int):
    next_candidates = set()
    for itemset in itemsets:
        is_infrequent = False
        for combination in itertools.combinations(itemset, k):
            if not(combination in original_itemsets):
                is_infrequent = True
                break
        if not is_infrequent:
            next_candidates.add(itemset)
    return next_candidates
