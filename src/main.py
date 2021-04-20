from mlxtend.preprocessing import TransactionEncoder
import AssociationRuleMining as arm


if __name__ == "__main__":
    # Question 1 / Implementing part of apriori algorithm
    print("-------------------------- Question 1 --------------------------")

    number_of_itemsets = 55
    current_k = 2

    for i in range(50):
        if 20 <= i < 40:
            current_k = 3
        elif i > 40:
            current_k = 4

        itemsets = arm.create_itemsets(number_of_itemsets, current_k)
        # print(itemsets)

        pruned_itemsets = arm.generate_next_set_of_itemsets(itemsets, current_k)
        # print(pruned_itemsets)

        naive_itemsets = arm.generate_next_set_of_naive_itemsets(itemsets, current_k)
        # print(naive_itemsets)

        print("Number of elements in list of itemsets for candidate generation algorithm: ", len(pruned_itemsets))
        print("Number of elements in list of naive itemsets: ", len(naive_itemsets))

        reduction = float(len(pruned_itemsets)) / float(len(naive_itemsets))
        print("Calculated reduction in candidate generation is: ", reduction, "\n")
    # End of Question 1

    # Question 2 / Experimenting with SON algorithm
    print("\n-------------------------- Question 2 --------------------------")

    te = TransactionEncoder()
    dataset, dataframe = arm.prepare_dataset("../resources/groceries.csv", te)
    # print(len(dataframe))

    arm.calculate_apriori_with_mlxtend(dataset, dataframe, te)
    # End of Question 2
