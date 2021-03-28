import AssociationRuleMining as arm

if __name__ == "__main__":
    itemsets = arm.create_itemset(50, 2)
    #print(itemsets)

    extended_itemsets = arm.generate_next_set_of_candidates(itemsets, 2)
    #print(extended_itemsets)

    pruned_itemsets = arm.eliminate_itemsets_with_non_frequent_items(itemsets, extended_itemsets, 2)
    #print(pruned_itemsets)

    print("Number of elements in extended itemsets: ", len(extended_itemsets))
    print("Number of elements in extended itemsets after pruning: ", len(pruned_itemsets))

    reduction = float(len(pruned_itemsets)) / float(len(extended_itemsets))
    print("Calculated reduction after pruning is: ", reduction)
