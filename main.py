import AssociationRuleMining as arm

if __name__ == "__main__":
    itemsets = arm.create_itemset(50, 2)
    print(itemsets)

    next_itemsets = arm.generate_next_set_of_candidates(itemsets, 2)
    print(next_itemsets)