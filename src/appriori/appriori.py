import argparse
import itertools
import sys
import random


# Creates itemsets by selecting among letters provided
def create_itemsets(letters: str, num_of_itemsets: int, num_of_items_per_itemset: int):
    itemsets = set()

    while len(itemsets) != num_of_itemsets:
        current_set = set()

        # Select random letter from selected_letters until we reach num_of_items_per_itemset
        while len(current_set) != num_of_items_per_itemset:
            current_set.add(random.choice(letters))

        # Sorting the set and converting it into tuple for convenience in later stages
        sorted_set = sorted(current_set)
        itemsets.add(tuple(sorted_set))

    return itemsets


# k is used to represent number of elements in each itemset in itemsets
def generate_next_set_of_itemsets(itemsets: set[tuple], k: int):
    next_itemsets = set()
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
                next_itemsets.add(tuple(sorted_set_to_add))

    # Eliminate k+1 item itemsets which include non-frequent k item itemsets
    pruned_itemsets = set()
    for itemset in next_itemsets:
        is_infrequent = False
        for combination in itertools.combinations(itemset, k):
            if not (combination in itemsets):
                is_infrequent = True
                break
        if not is_infrequent:
            pruned_itemsets.add(itemset)
    return pruned_itemsets


def generate_next_set_of_naive_itemsets(itemsets: set[tuple]):
    next_itemsets = set()
    all_possible_characters = set()
    for itemset in itemsets:
        for element in itemset:
            all_possible_characters.add(element)
    for itemset in itemsets:
        current_itemset = list(itemset)
        for character in all_possible_characters:
            if character not in current_itemset:
                next_itemset = list(current_itemset)
                next_itemset.append(character)
                sorted_itemset = sorted(next_itemset)
                next_itemsets.add(tuple(sorted_itemset))
    return next_itemsets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--number_of_itemsets',
                        type=int,
                        default=50,
                        help='number of itemsets to initially create, default: 50')
    parser.add_argument('--k',
                        type=int,
                        default=2,
                        help='number of items in each itemset, default: 50')
    parser.add_argument('--loop_count',
                        type=int,
                        default=50,
                        help='how many times experiment should be done, default: 50')
    parser.add_argument('--selected_letters',
                        default='abcdefghijkl',
                        help='letters to create itemset elements from, default: abcdefghijkl')
    parser.add_argument('--print_itemsets',
                        action='store_true',
                        default=False,
                        help='do you want to print itemsets after each milestone, default: False')
    parser_args = parser.parse_args()

    for i in range(parser_args.loop_count):
        itemsets = create_itemsets(parser_args.selected_letters, parser_args.number_of_itemsets, parser_args.k)
        if parser_args.print_itemsets:
            print(itemsets)

        pruned_itemsets = generate_next_set_of_itemsets(itemsets, parser_args.k)
        if parser_args.print_itemsets:
            print(pruned_itemsets)

        naive_itemsets = generate_next_set_of_naive_itemsets(itemsets)
        if parser_args.print_itemsets:
            print(naive_itemsets)

        print("Number of elements in list of itemsets for candidate generation algorithm: ", len(pruned_itemsets))
        print("Number of elements in list of naive itemsets: ", len(naive_itemsets))

        reduction = float(len(pruned_itemsets)) / float(len(naive_itemsets))
        print("Calculated reduction in candidate generation is: ", reduction, "\n")


if __name__ == "__main__":
    main()
