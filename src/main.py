from src.son import son
from src.appriori import appriori


if __name__ == "__main__":
    # Part 1 / Implementing candidate generation part of apriori algorithm
    print("-------------------------- Part 1 --------------------------")
    appriori.main()

    # Part 2 / Experimenting with SON algorithm
    print("\n-------------------------- Part 2 --------------------------")
    son.main()
