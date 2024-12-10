import matplotlib.pyplot as plt
from data import get_pots
from matching_tests import matching_existence_distinct_pots, matching_existence_within_pots

def main():
    pots = get_pots()

    d = int(input("Enter a value for d: "))
    k = len(pots)

    print(f"We have a graph G = (V, E), where the vertices are partitioned into k subsets V1, ..., V_{k}.")
    print()
    print(f"We have an integer d = {d}. We want to decide if there exists a subset F of E such that every vertex has exactly {d} neighbors in each Vi.")
    print()

    if matching_existence_distinct_pots(pots, degree=d) and matching_existence_within_pots(pots, degree=d):
        print()
        print(f"There exists a subset F of E such that every vertex has exactly {d} neighbors in each Vi in the graph.")
        print()
    else:
        print(f"There does not exist a subset F of E such that every vertex has exactly {d} neighbors in each Vi in the graph.")

    return None

if __name__ == "__main__":
    main()
