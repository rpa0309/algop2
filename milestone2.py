from typing import List, Tuple
import timeit
import random
import matplotlib.pyplot as plt
import sys


def program3(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    # Naive brute-force Θ(2^n) algorithm:
    # Calculate the sum for each subset of vaults
    subset_sums = [0] * (2 ** n)
    for mask in range(1 << n):
        if mask == 0:
            subset_sums[mask] = 0
        else:
            lsb = mask & -mask
            i = (lsb.bit_length() - 1)
            subset_sums[mask] = subset_sums[mask ^ lsb] + values[i]

    best_value = 0
    best_mask = 0

    # Validate each subset within distance constraint, choose maximum value
    for mask in range(1 << n):
        valid = True
        shifted = mask
        for _ in range(k):
            shifted = shifted >> 1
            if mask & shifted:
                valid = False
                break
        if valid and subset_sums[mask] > best_value:
            best_value = subset_sums[mask]
            best_mask = mask

    # Extract chosen indices in 1-indexed format
    chosen = [i + 1 for i in range(n) if (best_mask >> i) & 1]
    return best_value, chosen

def program4A(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    DP = [-1]*n
    solution = [[] for i in range(n)]

    val, indices = chooseVault(n-1, k+1, values, DP, solution)
    indices.reverse()
    indices = [x + 1 for x in indices]

    return val, indices # replace with your code

def chooseVault(i: int, k: int, vaults:List[int], DP:List[int], solution):
    # no elements left to evaluate
    if i < 0:
        return 0, []
    
    # only one element
    if i == 0:
        return vaults[0], [0]
    
    # something already cached there
    if DP[i] != -1:
        return DP[i], solution[i]
    
    # option 1: choose the current vault, move k vaults
    current, currentIndex = chooseVault(i-k, k, vaults, DP, solution)
    current += vaults[i]
    currentIndex = [i] + currentIndex

    # option 2: ignore this vault, move to the next one
    prev, prevIndex = chooseVault(i-1, k, vaults, DP, solution)

    # choose the max value between the two, return
    maximum = max(current, prev)
    if maximum == current:
        if DP[i] == -1:
            DP[i] = maximum
            solution[i] = currentIndex
        return DP[i], solution[i]
    else:
        if DP[i-1] == -1:
            DP[i-1] = maximum
            solution[i-1] = prevIndex
        return DP[i-1], solution[i-1]
    
def program4B(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    # ref: https://www.geeksforgeeks.org/dsa/maximum-sum-subsequence-least-k-distant-elements
    
    # DP = array of sums
    DP = [0] * n
    # solution = list of indices in a sublist
    solution = [[] for i in range(n)]
    #print(solution)
    
    # base case for the upcoming loop
    DP[n-1] = values[n-1]


    # for every value in Values (excluding the last one), R->L
    for pos in range(n-2, -1, -1):
        #print()
            #print("position:", pos)
        # if this is a starting element (elements from n to n-k)
        if (pos+(k+1) >= n):
            # used to determine where to start the sum
            DP[pos] = max(values[pos], DP[pos+1])
                # print("+Comparing:", values[pos], "to", DP[pos+1])
            # choose indices
            if DP[pos] == values[pos]:
                solution[pos] = [pos]
            else:
                solution[pos] = [pos+1]
        else:
            # compare a possible sum to the current sum
            # would start a new sum or continue
            DP[pos] = max(values[pos] + DP[pos+(k+1)], DP[pos+1])
                # print("-Comparing:", values[pos], "+", DP[pos+(k+1)], "to", DP[pos+1])
            # choose indices
            if DP[pos] == DP[pos+1]:
                solution[pos] = [pos+1]
            else:
                solution[pos] = [pos] + solution[pos+(k+1)]
    # Update indices to match vaults instead of array style
    solution[0] = [x+1 for x in solution[0]]
    return DP[0], solution[0] # replace with your code

def program5(n: int, k: int, values: List[int]) -> Tuple[int, List[int]]:
    # Dynamic programming O(n) solution:
    # dp[i] = best total using the first i vaults (1-indexed)
    # dp[i] = max(dp[i-1], values[i-1] + dp[i-k-1])
    if n <= 0:
        return 0, []

    dp: List[int] = [0] * (n + 1)
    choose: List[bool] = [False] * (n + 1)

    # Build a choice array to reconstruct solution
    for i in range(1, n + 1):
        include = values[i - 1]
        prev_index = i - k - 1
        if prev_index >= 0:
            include += dp[prev_index]

        if include > dp[i - 1]:
            dp[i] = include
            choose[i] = True
        else:
            dp[i] = dp[i - 1]
            choose[i] = False

    # Reconstruct chosen indices in 1-indexed format
    indices: List[int] = []
    i = n
    while i >= 1:
        if choose[i]:
            indices.append(i)
            i -= (k + 1)
        else:
            i -= 1

    indices.reverse()
    return dp[n], indices


def generate_input(n: int) -> Tuple[int, int, List[int]]:
    k = random.randint(1, max(1, (n//2) - 1))
    temp = []
    
    # generate random values
    for i in range(n):
        temp.append(random.randint(1, max(1, n)))

    return n, k, temp

#measure the time it takes for the algorithm to run, run multiple times and get the average
def measure_time(n: int, prog: int, repetitions: int = 500) -> float:
    n, k, values = generate_input(n)
    if prog == 1:
        program3(n, k, values)
        t = timeit.timeit(
            stmt=f"program3({n}, {k}, {values})",
            setup="from __main__ import program3",
            number=repetitions
        )

    elif prog == 2:
        program4A(n, k, values)
        t = timeit.timeit(
            stmt=f"program4A({n}, {k}, {values})",
            setup="from __main__ import program4A",
            number=repetitions
        )

    elif prog == 3:
        program4B(n, k, values)
        t = timeit.timeit(
            stmt=f"program4B({n}, {k}, {values})",
            setup="from __main__ import program4B",
            number=repetitions
        )
    
    elif prog == 4:
        program5(n, k, values)
        t = timeit.timeit(
            stmt=f"program5({n}, {k}, {values})",
            setup="from __main__ import program5",
            number=repetitions
        )

    return t / repetitions

if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    # recursion depth = 1000
    input_sizes = [5, 10, 15, 20, 25]
    repetitions = 500

    results = [[] for _ in range(0, 5)]

    print(f"{'n':>6} | {'avg time (s)':>15}")
    print("-" * 25)

    for i in range(1, 5):
        for n in input_sizes:
            avg_time = measure_time(n, i, repetitions)
            results[i].append(avg_time)
            print(f"{n:6d} | {avg_time:15.8e}")

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(input_sizes, results[2], marker='o', linewidth=2, label = "3")
    plt.plot(input_sizes, results[2], marker='o', linewidth=2, label = "4A")
    plt.plot(input_sizes, results[3], marker='o', linewidth=2, label = "4B")
    plt.plot(input_sizes, results[4], marker='o', linewidth=2, label = "5")

    plt.title("Runtime Scaling of programs 4A, 4B, 5")
    plt.xlabel("Input size n")
    plt.ylabel("Average execution time (seconds)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.legend()
    plt.show()
    
