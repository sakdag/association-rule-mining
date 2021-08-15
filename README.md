# Association Rule Mining
This repository includes following implementations related to association rule mining:

1. Implementation of candidate generation step of [Apriori algorithm](https://en.wikipedia.org/wiki/Apriori_algorithm)
2. Experiments with SON algorithm which partitions itemsets then runs Apriori algoritm on partitions and merges them.

Detailed information on each part can be found below. Pyhton 3.9 and Conda environment with dependencies as given in 
requirements.txt is used.

### 1. Candidate Generation

Pseudocode for the implemented part of Apriori algorithm can be seen below:

```
Given a set of k-item frequent itemsets I as input
    (Note that  k>1 and items within itemsets and also itemsets are already sorted in increasing order).
    C is the set of k-item Candidate Itemsets, initially empty
    
    For each itemset i in I
        For each itemset j in I
            If the initial k-1 elements of itemset i and j are the same, create a k+1-item candidate itemset c
                If c does not include any k-item non-frequent itemset
                    C = C U c

    Output C
```
- Example: 
```
Input {a,b}, {a,c}, {a,d}, {b,c}, {c,d}, {c,e}, {d,e} 
Output should be {a,b,c}, {a,c,d},{c,d,e}
```

This implementation can be found under src/apriori/apriori.py. For detailed information on the command line options 
use -h option.

### 2. Experiments with SON algorithm

Apriori function under [mlxtend library](http://rasbt.github.io/mlxtend/) is utilized for each partition. 
Implementation can be found under src/son/son.py. For detailed information on the command line options use -h option. 
For the dataset, groceries.csv under data/raw is used.

If you want to run both modes at the same time with default parameters, you can use src/main.py.

## License
[MIT](https://choosealicense.com/licenses/mit/)
