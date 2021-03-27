import string
import random


def create_itemset(num_of_itemsets, num_of_item_per_itemset):
    itemsets = set()
    while len(itemsets) != num_of_itemsets:
        current_list = list()
        for i in range(num_of_item_per_itemset):
            current_list.append(random.choice(string.ascii_lowercase))
        sorted_list = sorted(current_list)
        itemsets.add(tuple(sorted_list))
    return itemsets
