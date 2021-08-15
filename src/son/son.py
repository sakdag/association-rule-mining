import csv
import os
import sys
import argparse

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

import src.config.config as conf


def prepare_dataset(dataset_path: str, te):
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
        print(len(total_list_of_results))

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


def main():
    dirname = os.path.dirname(__file__)
    dataset_file_path = os.path.join(dirname, conf.GROCERIES_DATASET_FILE_PATH)

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path',
                        default=dataset_file_path,
                        help='absolute path of the dataset you want to use, default: '
                             '{path to project}/data/raw/groceries.csv')
    parser_args = parser.parse_args()

    te = TransactionEncoder()
    dataset, dataframe = prepare_dataset(parser_args.dataset_path, te)
    print(len(dataframe))

    calculate_apriori_with_mlxtend(dataset, dataframe, te)


if __name__ == '__main__':
    main()
