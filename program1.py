from typing import List, Tuple
import timeit
import random
#import matplotlib.pyplot as plt


def program1(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 1
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)

    """
    
    ############################
    # Add you code here
    # iteratively select the last available vault starting at the end of the list until there are no more available vaults
    max = 0
    vaultsSelected = []
    i = n-1
    while(i > -1):
        max += values[i]
        vaultsSelected.append(i+1)
        i -= k+1

    ############################
    vaultsSelected.sort()
    return max, vaultsSelected # replace with your code


"""
if __name__ == "__main__":
    input_sizes = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    repetitions = 500

    results = []

    print(f"{'n':>6} | {'avg time (s)':>15}")
    print("-" * 25)

    for n in input_sizes:
        avg_time = measure_time(n, repetitions)
        results.append(avg_time)
        print(f"{n:6d} | {avg_time:15.8e}")

    # Plot results
    # plt.figure(figsize=(8, 5))
    # plt.plot(input_sizes, results, marker='o', linestyle='-', linewidth=2)
    # plt.title("Runtime Scaling of program1")
    # plt.xlabel("Input size n")
    # plt.ylabel("Average execution time (seconds)")
    # plt.grid(True, linestyle='--', alpha=0.6)
    # plt.tight_layout()
    # plt.show()

"""


def generate_input(n: int) -> Tuple[int, int, List[int]]:
    k = random.randint(1, max(1, n-1))
    values = list()
    #generate random values in ascending order, the correct format for problem s1
    for i in range(n):
        values.append(i+1)
    return n, k, values

#measure the time it takes for the algorithm to run, run multiple times and get the average
def measure_time(n: int, repetitions: int = 500) -> float:
    n, k, values = generate_input(n)
    program1(n, k, values)

    t = timeit.timeit(
        stmt=f"program1({n}, {k}, {values})",
        setup="from __main__ import program1",
        number=repetitions
    )
    return t / repetitions


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program1(n, k, values)

    print(m)
    for i in indices:
        print(i)