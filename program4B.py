from typing import List, Tuple
# import timeit
# import random
# import matplotlib.pyplot as plt
# import sys

def program4B(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 4B
    
    Parameters:
    n (int): number of vaults
    k (int): no two chosen vaults are within k positions of each other
    values (List[int]): the values of the vaults

    Returns:
    int:  maximal total value
    List[int]: the indices of the chosen vaults(1-indexed)
    """

    # ref: https://www.geeksforgeeks.org/dsa/maximum-sum-subsequence-least-k-distant-elements
    
    # DP = array of sums
    DP = [0] * n
    # solution = list of indices in a sublist
    solution = [[] for i in range(n)]
    #print(solution)
    
    # base case for the upcoming loop
    DP[n-1] = values[n-1]
    solution[n-1] = [n-1]

    # for every value in Values (excluding the last one), R->L
    for pos in range(n-2, -1, -1):
        #print()
            #print("position:", pos)
        # if this is a starting element (elements from n to n-k)
        if (pos+(k+1) >= n):
            # used to determine where to start the sum
            DP[pos] = max(values[pos], DP[pos+1])
            #print("+Comparing:", values[pos], "to", DP[pos+1])
            # choose indices
            if DP[pos] == values[pos]:
                solution[pos] = [pos]
            else:
                solution[pos] = [pos+1]
            #print(solution)
        else:
            # compare a possible sum to the current sum
            # would start a new sum or continue
            DP[pos] = max(values[pos] + DP[pos+(k+1)], DP[pos+1])
            #print("-Comparing:", values[pos], "+", DP[pos+(k+1)], "to", DP[pos+1])
            # choose indices
            if DP[pos] == DP[pos+1]:
                solution[pos] = solution[pos+1]
            else:
                solution[pos] = [pos] + solution[pos+(k+1)]
            #print(DP)
            # print(solution)
    # Update indices to match vaults instead of array style
    solution[0] = [x+1 for x in solution[0]]
    return DP[0], solution[0] # replace with your code


if __name__ == '__main__':
    n, k = map(int, input().split())
    values = list(map(int, input().split()))

    m, indices = program4B(n, k, values)

    print(m)
    for i in indices:
        print(i)
"""

def generate_input(n: int) -> Tuple[int, int, List[int]]:
    k = random.randint(1, max(1, (n//2) - 1))
    temp = []
    
    # generate random values
    for i in range(n):
        temp.append(random.randint(1, max(1, n)))

    return n, k, temp

#measure the time it takes for the algorithm to run, run multiple times and get the average
def measure_time(n: int, repetitions: int = 500) -> float:
    n, k, values = generate_input(n)
    program4B(n, k, values)

    t = timeit.timeit(
        stmt=f"program4B({n}, {k}, {values})",
        setup="from __main__ import program4B",
        number=repetitions
    )
    return t / repetitions

if __name__ == "__main__":
    # sys.setrecursionlimit(100000)
    # recursion depth = 1000
    input_sizes = [10, 100, 1000, 10000, 100000]
    repetitions = 500

    results = []

    print(f"{'n':>6} | {'avg time (s)':>15}")
    print("-" * 25)

    for n in input_sizes:
        avg_time = measure_time(n, repetitions)
        results.append(avg_time)
        print(f"{n:6d} | {avg_time:15.8e}")

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(input_sizes, results, marker='o', linestyle='-', linewidth=2)
    plt.title("Runtime Scaling of program4B")
    plt.xlabel("Input size n")
    plt.ylabel("Average execution time (seconds)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
    """
