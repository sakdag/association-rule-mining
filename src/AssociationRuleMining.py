import itertools
import string
import random
import csv
import pandas as pd
from mlxtend.frequent_patterns import apriori

selected_letters = 'abcdefghijkl'


def create_itemsets(num_of_itemsets: int, num_of_item_per_itemset: int):
    itemsets = set()
    while len(itemsets) != num_of_itemsets:
        current_set = set()
        while len(current_set) != num_of_item_per_itemset:
            current_set.add(random.choice(selected_letters))
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


# k is used to represent number of elements in each itemset in itemsets
def generate_next_set_of_naive_itemsets(itemsets: set[tuple], k: int):
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


def prepare_dataset(dataset_path: string, te):
    dataset = list()
    with open(dataset_path, "r") as f:
        reader = csv.reader(f, delimiter="\n")
        for line in reader:
            current_line = list()
            for token in str(line[0]).split(";"):
                current_line.append(token)
            dataset.append(current_line)

    te_ary = te.fit(dataset).transform(dataset)
    return dataset, pd.DataFrame(te_ary, columns=te.columns_)


def calculate_apriori_with_mlxtend(dataset, dataframe, te):
    result_without_partitioning = apriori(dataframe, min_support=0.02, use_colnames=True)
    len_of_result_wo_partitioning = len(result_without_partitioning)
    print("Number of itemsets after running apriori without partitioning: ", len_of_result_wo_partitioning, "\n")

    # Divide initial dataset into 5 to 10 chunks, run apriori and compare results
    for i in range(5, 11):
        print("Tests after partitioning the dataset into: ", i)
        partitioned_datasets = list()
        number_of_elements = int(len(dataset) / i)
        number_of_elements_in_last = number_of_elements + (len(dataset) - (i * number_of_elements))

        # Partition initial dataset into chunks calculated above
        for j in range(i):
            current_dataset = list()
            for k in range(j * number_of_elements, (j + 1) * number_of_elements):
                current_dataset.append(dataset[k])
            partitioned_datasets.append(current_dataset)

        # Get remaining elements to put them into last chunk
        for j in range(number_of_elements, number_of_elements_in_last):
            partitioned_datasets[i - 1].append(dataset[(number_of_elements * (i - 1)) + j])
        total_list_of_results = list()

        # For each chunk, run apriori and add it to union
        for j in range(i):
            part_te_ary = te.fit(partitioned_datasets[j]).transform(partitioned_datasets[j])
            part_df = pd.DataFrame(part_te_ary, columns=te.columns_)
            result = apriori(part_df, min_support=0.02, use_colnames=True)
            for element in result["itemsets"].to_list():
                total_list_of_results.append(tuple(element))
        # print(len(total_list_of_results))

        # Remove duplicate elements from results
        union_of_results = set()
        for result in total_list_of_results:
            sorted_result = sorted(result)
            current_names = ""
            for element in sorted_result:
                current_names += element
            union_of_results.add(current_names)
        len_of_union_of_results = len(union_of_results)
        print("Number of elements after running apriori in all partitions and taking union of results: ",
              len_of_union_of_results)
        over_generation_ration = float(len_of_union_of_results) / float(len_of_result_wo_partitioning)
        print("Over generation ration: ", over_generation_ration, "\n")
