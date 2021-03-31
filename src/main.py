from mlxtend.preprocessing import TransactionEncoder
import AssociationRuleMining as arm


if __name__ == "__main__":
    # Question 1 / Implementing part of apriori algorithm
    print("-------------------------- Question 1 --------------------------")

    itemsets = arm.create_itemset(50, 2)
    #print(itemsets)

    pruned_itemsets = arm.generate_next_set_of_itemsets(itemsets, 2)
    #print(pruned_itemsets)

    naive_itemsets = arm.generate_next_set_of_naive_itemsets(itemsets, 2)
    #print(naive_itemsets)

    print("Number of elements in naive itemsets: ", len(naive_itemsets))
    print("Number of elements in itemsets after pruning: ", len(pruned_itemsets))

    reduction = float(len(pruned_itemsets)) / float(len(naive_itemsets))
    print("Calculated reduction after pruning is: ", reduction)
    # End of Question 1

    # Question 2 / Experimenting with SON algorithm
    print("\n-------------------------- Question 2 --------------------------")

    te = TransactionEncoder()
    dataset, dataframe = arm.prepare_dataset("../resources/groceries.csv", te)
    #print(len(dataframe))

    arm.calculate_apriori_with_mlxtend(dataset, dataframe, te)
    # End of Question 2
