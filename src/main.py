import csv

import AssociationRuleMining as arm
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


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

    dataset = list()
    with open("../resources/groceries.csv", "r") as f:
        reader = csv.reader(f, delimiter="\n")
        for line in reader:
            current_line = list()
            for token in str(line[0]).split(";"):
                current_line.append(token)
            dataset.append(current_line)

    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # print(len(df))

    print(len(apriori(df, min_support=0.02, use_colnames=True)))

    for i in range(5, 10):
        print("For partitions of: ", i)
        partitioned_datasets = list()
        number_of_elements = int(len(dataset) / i)
        number_of_elements_in_last = number_of_elements + (len(dataset) - (i * number_of_elements))
        for j in range(i):
            current_dataset = list()
            for k in range((j) * number_of_elements, (j + 1) * number_of_elements):
                current_dataset.append(dataset[k])
            partitioned_datasets.append(current_dataset)
        for j in range(number_of_elements, number_of_elements_in_last):
            partitioned_datasets[i - 1].append(dataset[(number_of_elements * (i - 1)) + j])
        for j in range(i):
            part_te_ary = te.fit(partitioned_datasets[j]).transform(partitioned_datasets[j])
            part_df = pd.DataFrame(part_te_ary, columns=te.columns_)
            print(len(apriori(part_df, min_support=0.02, use_colnames=True)))
